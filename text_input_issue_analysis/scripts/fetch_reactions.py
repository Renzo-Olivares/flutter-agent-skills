#!/usr/bin/env python3
"""
Fetch per-issue reaction counts for the known text-input issue set.

Supplementary to fetch_issues.py: the main fetch now captures reactions too,
but this script exists for (a) the one-time backfill onto a pre-existing
text_input_issues.json and (b) a cheap way to refresh reactions without
re-running the full comment pull.

Strategy:
- Read the existing text_input_issues.json for the canonical issue-number list
  (falls back to data/merged_raw.json).
- Batch numbers into aliased GraphQL queries (BATCH_SIZE aliases per query).
  ~23 queries for 1,122 issues at BATCH_SIZE=50.
- Write data/reactions.json keyed by issue-number string:
    {"<n>": {"total": int, "by_type": {"THUMBS_UP": n, ...}}}  (zero-count types elided)
- Resume-safe: re-running skips issues already present in the output unless
  --refresh is passed.

Usage:
  fetch_reactions.py [--batch-size 50] [--refresh]
"""
import argparse
import datetime
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
FINAL = ROOT / "text_input_issues.json"
MERGED = DATA / "merged_raw.json"
OUT = DATA / "reactions.json"

BATCH_FRAGMENT = "fragment R on Issue { reactionGroups { content reactors { totalCount } } }"


def gh_graphql(query):
    result = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={query}"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"gh api graphql failed: rc={result.returncode}\nSTDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout[:400]}"
        )
    data = json.loads(result.stdout)
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {json.dumps(data['errors'], indent=2)}")
    return data["data"]


def flatten_reactions(groups):
    by_type = {}
    total = 0
    for g in groups or []:
        n = g["reactors"]["totalCount"]
        if n:
            by_type[g["content"]] = n
            total += n
    return {"total": total, "by_type": by_type}


def build_query(numbers):
    lines = [f'  i{n}: issue(number: {n}) {{ ...R }}' for n in numbers]
    return (
        BATCH_FRAGMENT
        + "\nquery {\n"
        + '  repository(owner: "flutter", name: "flutter") {\n'
        + "\n".join(lines)
        + "\n  }\n  rateLimit { remaining cost }\n}\n"
    )


def load_issue_numbers():
    if FINAL.exists():
        src = json.loads(FINAL.read_text())
        return [iss["number"] for iss in src["issues"]], FINAL.name
    if MERGED.exists():
        src = json.loads(MERGED.read_text())
        return [iss["number"] for iss in src["issues"]], MERGED.name
    raise FileNotFoundError(
        f"Neither {FINAL} nor {MERGED} exists — nothing to fetch reactions for."
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch-size", type=int, default=50)
    ap.add_argument(
        "--refresh", action="store_true",
        help="Re-fetch reactions for every issue, ignoring existing entries.",
    )
    args = ap.parse_args()

    numbers, src_name = load_issue_numbers()
    numbers = sorted(set(numbers))
    print(f"Source: {src_name} — {len(numbers)} issues")

    existing = {}
    if OUT.exists() and not args.refresh:
        prev = json.loads(OUT.read_text())
        existing = prev.get("reactions", {})
        print(f"Resuming: {len(existing)} issues already have reactions")

    todo = [n for n in numbers if str(n) not in existing]
    if not todo:
        print("All issues already have reactions. Use --refresh to re-fetch.")
        return

    print(f"Fetching reactions for {len(todo)} issues in batches of {args.batch_size}")
    t_start = time.time()
    pages = 0
    for i in range(0, len(todo), args.batch_size):
        batch = todo[i : i + args.batch_size]
        query = build_query(batch)
        t0 = time.time()
        data = gh_graphql(query)
        repo = data["repository"]
        rl = data.get("rateLimit") or {}
        found = 0
        missing = 0
        for n in batch:
            node = repo.get(f"i{n}")
            if node is None:
                missing += 1
                existing[str(n)] = {"total": 0, "by_type": {}, "missing": True}
            else:
                existing[str(n)] = flatten_reactions(node.get("reactionGroups"))
                found += 1
        pages += 1

        # Checkpoint after each batch.
        OUT.write_text(json.dumps({
            "fetched_at": datetime.datetime.now(datetime.timezone.utc)
                .isoformat().replace("+00:00", "Z"),
            "source": src_name,
            "reactions": existing,
        }, indent=2))

        print(
            f"  batch {pages}: +{found} ok, {missing} missing  "
            f"total_have={len(existing)}/{len(numbers)}  "
            f"rl_remaining={rl.get('remaining')} cost={rl.get('cost')}  "
            f"{time.time() - t0:.1f}s"
        )

    # Stats.
    totals = [r["total"] for r in existing.values()]
    totals.sort(reverse=True)
    nonzero = sum(1 for t in totals if t)
    grand = sum(totals)
    missing_total = sum(1 for r in existing.values() if r.get("missing"))
    print(
        f"\nDone in {time.time() - t_start:.1f}s. "
        f"{len(existing)} issues; {nonzero} with >=1 reaction; "
        f"{grand} reactions in total; "
        f"top-10 totals: {totals[:10]}; "
        f"missing-from-API: {missing_total}"
    )


if __name__ == "__main__":
    main()
