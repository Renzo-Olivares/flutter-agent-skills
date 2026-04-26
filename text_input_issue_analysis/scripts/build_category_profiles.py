#!/usr/bin/env python3
"""
Generate category_profiles.md: one section per category with ownership,
reactions, priority, platform, issue-type tilt, age, recency, reproducibility,
and top-issue detail.

Input: text_input_issues.json + text_input_taxonomy.json
Output: category_profiles.md (at the repo root of the analysis folder)

Re-run any time the snapshot, taxonomy, or categorization changes.

NOTE: the report format is specified in CATEGORY_PROFILE_FORMAT.md at the
analysis-folder root. If you change the output shape here, update the spec in
the same commit.
"""
import datetime
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
ISSUES = ROOT / "text_input_issues.json"
TAXONOMY = ROOT / "text_input_taxonomy.json"
OUT = ROOT / "category_profiles.md"

NOW = datetime.datetime.now(datetime.timezone.utc)
RECENT_WINDOW_DAYS = 90
STALE_THRESHOLD_DAYS = 365 * 3

REACTION_EMOJI = {
    "THUMBS_UP": "👍",
    "THUMBS_DOWN": "👎",
    "LAUGH": "😄",
    "HOORAY": "🎉",
    "CONFUSED": "😕",
    "HEART": "❤️",
    "ROCKET": "🚀",
    "EYES": "👀",
}

# How to classify a `c: *` label into a coarse tilt bucket.
BUG_LABELS = {"c: crash", "c: fatal crash", "c: regression", "c: performance", "c: flake"}
FEATURE_LABELS = {"c: proposal", "c: new feature", "c: new widget"}


def parse_iso(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


def age_days(iss):
    return (NOW - parse_iso(iss["created_at"])).days


def updated_days_ago(iss):
    return (NOW - parse_iso(iss["updated_at"])).days


def classify_tilt(labels):
    """Return (bug_count, feature_count, other_typed_count, unlabeled) for one issue."""
    c_labels = [l for l in labels if l.startswith("c: ")]
    if not c_labels:
        return (0, 0, 0, 1)
    bug = 1 if any(l in BUG_LABELS for l in c_labels) else 0
    feat = 1 if any(l in FEATURE_LABELS for l in c_labels) else 0
    # If an issue has both (rare) count as both; count "other" only if neither.
    other = 1 if (not bug and not feat) else 0
    return (bug, feat, other, 0)


def format_pct(n, total):
    return f"{100 * n / total:.0f}%" if total else "—"


def md_escape(s):
    return s.replace("|", "\\|")


def write_summary_matrix(f, issues, taxonomy):
    teams_seen = set()
    by_cat = defaultdict(lambda: defaultdict(int))
    for iss in issues:
        teams_seen.add(iss["ownership"])
        by_cat[iss["category"]][iss["ownership"]] += 1

    major = [
        "team-text-input", "team-framework", "team-design",
        "team-web", "team-ios", "team-android",
        "team-windows", "team-engine", "team-macos", "team-linux",
    ]
    rare = sorted(t for t in teams_seen if t not in major)
    cols = major + rare
    abbrev = {
        "team-text-input": "txt", "team-framework": "fmw", "team-design": "des",
        "team-web": "web", "team-ios": "ios", "team-android": "and",
        "team-windows": "win", "team-engine": "eng", "team-macos": "mac",
        "team-linux": "lin", "team-tool": "tool", "team-ecosystem": "eco",
        "team-accessibility": "a11y", "orphaned": "orp",
    }

    f.write("## Ownership matrix (issue counts)\n\n")
    f.write(
        "One row per category (taxonomy order). Columns are `team-*` "
        "abbreviations; the final **Total** row sums each team column across "
        "all categories (and matches that team's total issue ownership "
        "corpus-wide). Abbreviations:\n"
    )
    f.write(", ".join(f"`{abbrev.get(t, t)}` = {t}" for t in cols) + ".\n\n")
    header = ["#", "n", "category"] + [abbrev.get(t, t) for t in cols]
    f.write("| " + " | ".join(header) + " |\n")
    f.write("|" + "|".join(["---"] * len(header)) + "|\n")
    for i, cat in enumerate(taxonomy["categories"], 1):
        counts = by_cat[cat["name"]]
        row = [str(i), str(cat["count"]), md_escape(cat["name"])]
        for t in cols:
            v = counts.get(t, 0)
            row.append(str(v) if v else "·")
        f.write("| " + " | ".join(row) + " |\n")
    # Per-team totals row (sum of each team column).
    col_totals = {t: sum(by_cat[c["name"]].get(t, 0) for c in taxonomy["categories"]) for t in cols}
    grand_total = sum(col_totals.values())
    totals_row = ["—", f"**{grand_total}**", "**Total**"]
    for t in cols:
        v = col_totals[t]
        totals_row.append(f"**{v}**" if v else "·")
    f.write("| " + " | ".join(totals_row) + " |\n")
    f.write("\n")


def write_reaction_leaderboard(f, issues, taxonomy):
    rtotal = defaultdict(int)
    for iss in issues:
        rtotal[iss["category"]] += iss["reactions"]["total"]
    f.write("## Reaction-weighted ranking\n\n")
    f.write("Categories ranked by reaction total and average per issue.\n\n")
    f.write("| # | category | issues | reactions | avg |\n")
    f.write("|---|---|---|---|---|\n")
    ranked = sorted(taxonomy["categories"], key=lambda c: -rtotal[c["name"]])
    for i, cat in enumerate(ranked, 1):
        r = rtotal[cat["name"]]
        avg = r / cat["count"] if cat["count"] else 0
        f.write(f"| {i} | {md_escape(cat['name'])} | {cat['count']} | {r} | {avg:.1f} |\n")
    f.write("\n")


def write_category(f, cat, issues_in_cat):
    total = len(issues_in_cat)
    f.write(f"### {cat['name']}\n\n")
    f.write(f"*{cat['description']}*\n\n")
    f.write(f"**Size:** {total} issues")

    # Reactions.
    rtotal = sum(i["reactions"]["total"] for i in issues_in_cat)
    rbucket = Counter()
    for i in issues_in_cat:
        for k, v in i["reactions"]["by_type"].items():
            rbucket[k] += v
    f.write(f" · **Reactions:** {rtotal} total (avg {rtotal/total:.1f}/issue)")
    if rbucket:
        pieces = [f"{REACTION_EMOJI.get(k, k)} {v}" for k, v in rbucket.most_common()]
        f.write(" — " + " · ".join(pieces))
    f.write("\n\n")

    # Ownership (by count desc, tie-broken by reactions desc).
    ownership = defaultdict(lambda: [0, 0])  # owner -> [count, reactions]
    for i in issues_in_cat:
        ownership[i["ownership"]][0] += 1
        ownership[i["ownership"]][1] += i["reactions"]["total"]
    owners_sorted = sorted(ownership.items(), key=lambda kv: (-kv[1][0], -kv[1][1]))
    f.write("**Ownership:**\n\n")
    f.write("| team | issues | % | reactions |\n|---|---|---|---|\n")
    for owner, (n, r) in owners_sorted:
        f.write(f"| `{owner}` | {n} | {format_pct(n, total)} | {r} |\n")
    f.write("\n")

    # Priority.
    prio = Counter()
    for i in issues_in_cat:
        for l in i["labels"]:
            if l in ("P0", "P1", "P2", "P3"):
                prio[l] += 1
    no_prio = total - sum(prio.values())
    f.write("**Priority:** ")
    prio_parts = [f"P1: {prio['P1']}", f"P2: {prio['P2']}", f"P3: {prio['P3']}"]
    if prio["P0"]:
        prio_parts.insert(0, f"P0: {prio['P0']}")
    if no_prio:
        prio_parts.append(f"unlabeled: {no_prio}")
    f.write(" · ".join(prio_parts))
    f.write("\n\n")

    # Platform labels.
    plat = Counter()
    for i in issues_in_cat:
        for l in i["labels"]:
            if l.startswith("platform-"):
                plat[l] += 1
    with_plat = sum(1 for i in issues_in_cat if any(l.startswith("platform-") for l in i["labels"]))
    f.write(f"**Platform labels:** {with_plat}/{total} ({format_pct(with_plat, total)}) have a `platform-*` label")
    if plat:
        top = plat.most_common()
        pieces = [f"{l.removeprefix('platform-')}: {n}" for l, n in top]
        f.write(" — " + ", ".join(pieces))
    f.write("\n\n")

    # Issue-type tilt.
    tilt = [0, 0, 0, 0]  # bug, feature, other-c, unlabeled
    c_counter = Counter()
    for i in issues_in_cat:
        b, feat, other, un = classify_tilt(i["labels"])
        tilt[0] += b; tilt[1] += feat; tilt[2] += other; tilt[3] += un
        for l in i["labels"]:
            if l.startswith("c: "):
                c_counter[l] += 1
    f.write(
        f"**Issue-type tilt:** "
        f"bug ({tilt[0]}) · feature ({tilt[1]}) · other-c-label ({tilt[2]}) · no `c:` label ({tilt[3]})"
    )
    if c_counter:
        top = ", ".join(f"`{l}` ({n})" for l, n in c_counter.most_common(5))
        f.write(f" — top: {top}")
    f.write("\n\n")

    # Age.
    ages = sorted(age_days(i) for i in issues_in_cat)
    median = ages[len(ages) // 2]
    stale = sum(1 for a in ages if a > STALE_THRESHOLD_DAYS)
    oldest_year = parse_iso(
        min(i["created_at"] for i in issues_in_cat)
    ).year
    f.write(
        f"**Age:** median {median}d (~{median/365:.1f}y) · "
        f"oldest opened {oldest_year} · "
        f">3y old: {stale} ({format_pct(stale, total)})"
    )
    f.write("\n\n")

    # Recency.
    recent = sum(1 for i in issues_in_cat if updated_days_ago(i) <= RECENT_WINDOW_DAYS)
    f.write(
        f"**Recency:** {recent} issues ({format_pct(recent, total)}) "
        f"updated in the last {RECENT_WINDOW_DAYS} days"
    )
    f.write("\n\n")

    # Reproducibility.
    repro = sum(1 for i in issues_in_cat if "has reproducible steps" in i["labels"])
    f.write(f"**Reproducibility:** {repro}/{total} ({format_pct(repro, total)}) "
            f"have `has reproducible steps`\n\n")

    # Found in release (top 3).
    found = Counter()
    for i in issues_in_cat:
        for l in i["labels"]:
            if l.startswith("found in release: "):
                found[l.removeprefix("found in release: ")] += 1
    if found:
        top = ", ".join(f"{k} ({n})" for k, n in found.most_common(3))
        f.write(f"**Found in release (top 3):** {top}\n\n")
    else:
        f.write("**Found in release:** —\n\n")

    # Top 5 by reactions.
    top5 = sorted(issues_in_cat, key=lambda i: -i["reactions"]["total"])[:5]
    f.write("**Top 5 issues by reactions:**\n\n")
    for i in top5:
        r = i["reactions"]["total"]
        title = i["title"].strip()
        if len(title) > 100:
            title = title[:97] + "..."
        f.write(f"- [#{i['number']} — {md_escape(title)}]({i['url']}) — **{r}** reactions\n")
    f.write("\n")


def main():
    issues_payload = json.loads(ISSUES.read_text())
    issues = issues_payload["issues"]
    taxonomy = json.loads(TAXONOMY.read_text())
    snapshot = issues_payload.get("last_refreshed", "unknown")

    by_cat = defaultdict(list)
    for iss in issues:
        by_cat[iss["category"]].append(iss)

    with OUT.open("w") as f:
        f.write("# Flutter Text Input — Category Profiles\n\n")
        f.write(
            "Per-category profiles of the 31-category discovered taxonomy "
            "(see `text_input_taxonomy.json`). Generated by "
            "`scripts/build_category_profiles.py` from `text_input_issues.json` "
            "+ `text_input_taxonomy.json`. Format spec: "
            "[`CATEGORY_PROFILE_FORMAT.md`](CATEGORY_PROFILE_FORMAT.md).\n\n"
        )
        f.write(
            f"- Snapshot: `{snapshot}`\n"
            f"- Generated: `{NOW.isoformat(timespec='seconds').replace('+00:00', 'Z')}`\n"
            f"- Total issues: {len(issues)}\n"
            f"- Categories: {len(taxonomy['categories'])}\n\n"
        )

        f.write("## How to read this file\n\n")
        f.write(
            "Each category section reports a fixed set of stats. Definitions:\n\n"
            "- **Size** — number of issues assigned to the category (counts match `text_input_taxonomy.json`).\n"
            "- **Reactions** — sum and per-type breakdown of GitHub reactions across the category's issues.\n"
            "- **Ownership** — `team-*` label distribution, issue-count descending; reactions shown as a secondary column. `orphaned` = no `team-*` label.\n"
            "- **Priority** — counts of `P0`/`P1`/`P2`/`P3`; `unlabeled` = issue has no priority label.\n"
            f"- **Platform labels** — distribution of `platform-*` labels; these are orthogonal to `team-*` ownership, and only ~61% of issues carry one.\n"
            "- **Issue-type tilt** — bucketed `c: *` labels. `bug` = `crash`/`fatal crash`/`regression`/`performance`/`flake`. `feature` = `proposal`/`new feature`/`new widget`. `other-c-label` = any other `c: *`. `no c: label` = issue has none.\n"
            f"- **Age** — days since `created_at`, measured against the script-run time. `>3y old` uses a {STALE_THRESHOLD_DAYS}-day threshold.\n"
            f"- **Recency** — issues whose `updated_at` is within the last {RECENT_WINDOW_DAYS} days.\n"
            "- **Reproducibility** — share of issues with the `has reproducible steps` label (corpus-wide: ~52%).\n"
            "- **Found in release (top 3)** — most-cited `found in release: X.Y` labels.\n"
            "- **Top 5 issues by reactions** — hyperlinked examples, reaction-total descending.\n\n"
        )

        write_summary_matrix(f, issues, taxonomy)
        write_reaction_leaderboard(f, issues, taxonomy)

        f.write("## Per-category profiles\n\n")
        f.write("Categories listed in taxonomy order (issue count, descending).\n\n")
        for cat in taxonomy["categories"]:
            write_category(f, cat, by_cat[cat["name"]])

    size_kb = OUT.stat().st_size / 1024
    print(f"Wrote {OUT} ({size_kb:.1f} KB, {sum(1 for _ in OUT.open())} lines)")


if __name__ == "__main__":
    main()
