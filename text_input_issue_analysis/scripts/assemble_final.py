#!/usr/bin/env python3
"""
Assemble the final text_input_issues.json snapshot.

Steps:
1. Load merged_raw.json (every issue with ownership already derived).
2. Load every summaries/summary_*.json (including the gapfill) and build a single
   lookup number -> summary.
3. Load categorization.json (if present) and apply the discovered category per issue.
4. Populate comment_summary and category on each issue. Strip comments_raw /
   comment_count fields from the final output.
5. Write the final snapshot with the plan's wrapper schema.
"""
import datetime
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
MERGED = DATA / "merged_raw.json"
SUMMARY_DIR = DATA / "summaries"
CATEGORIZATION = DATA / "categorization.json"
OUT = ROOT / "text_input_issues.json"

QUERY = 'repo:flutter/flutter is:issue is:open (label:team-text-input OR label:"a: text input")'

FIELDS = [
    "number",
    "title",
    "url",
    "state",
    "labels",
    "assignees",
    "ownership",
    "created_at",
    "updated_at",
    "body",
    "comment_summary",
    "category",
]


def main():
    merged = json.loads(MERGED.read_text())
    issues = merged["issues"]

    # Load all summaries into a single lookup.
    summary_lookup = {}  # issue_number_str -> summary (str or None)
    for sp in sorted(SUMMARY_DIR.glob("summary_*.json")):
        data = json.loads(sp.read_text())
        for k, v in data.get("summaries", {}).items():
            if k in summary_lookup and summary_lookup[k] is not None and v is None:
                # Prefer non-null if a duplicate exists.
                continue
            summary_lookup[k] = v

    # Populate comment_summary. Issues with zero comments stay None.
    no_comments = 0
    with_summary = 0
    null_summary = 0
    unexpected_missing = []
    for iss in issues:
        n = str(iss["number"])
        if iss["comment_count"] == 0:
            iss["comment_summary"] = None
            no_comments += 1
        else:
            if n not in summary_lookup:
                unexpected_missing.append(iss["number"])
                iss["comment_summary"] = None
            else:
                iss["comment_summary"] = summary_lookup[n]
                if iss["comment_summary"] is None:
                    null_summary += 1
                else:
                    with_summary += 1

    if unexpected_missing:
        print(f"WARNING: {len(unexpected_missing)} commented issues have no summary entry: {unexpected_missing[:20]}")

    # Apply categorization if available. Issues without an entry keep category=None.
    category_lookup = {}
    if CATEGORIZATION.exists():
        category_lookup = json.loads(CATEGORIZATION.read_text())
    uncategorized = 0
    for iss in issues:
        n = str(iss["number"])
        iss["category"] = category_lookup.get(n)
        if iss["category"] is None:
            uncategorized += 1

    # Strip internal fields, keep only schema fields.
    final_issues = []
    for iss in issues:
        final_issues.append({k: iss.get(k) for k in FIELDS})
    final_issues.sort(key=lambda x: x["number"])

    payload = {
        "last_refreshed": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        "query": QUERY,
        "total_count": len(final_issues),
        "issues": final_issues,
    }

    OUT.write_text(json.dumps(payload, indent=2))
    size_mb = OUT.stat().st_size / (1024 * 1024)
    print(f"Wrote {OUT} ({size_mb:.2f} MB)")
    print(f"Total issues: {len(final_issues)}")
    print(f"  with real summary: {with_summary}")
    print(f"  summary=null (noise): {null_summary}")
    print(f"  no comments: {no_comments}")
    print(f"  uncategorized: {uncategorized}")
    if unexpected_missing:
        print(f"  unexpected missing summaries: {len(unexpected_missing)}")


if __name__ == "__main__":
    main()
