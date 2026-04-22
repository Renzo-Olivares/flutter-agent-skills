#!/usr/bin/env python3
"""
Build a compact per-issue dataset for the categorization agent.

Per issue:
- number
- title
- url
- ownership
- labels (only the a:/p:/team- labels, skip bot labels)
- body (truncated to ~1000 chars, with suffix markers when truncated)
- comment_summary

Output: compact_issues.json — an array of issue objects.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
SRC = ROOT / "text_input_issues.json"
OUT = ROOT / "data" / "compact_issues.json"

BODY_MAX_CHARS = 1000
LABEL_PREFIXES = ("a:", "p:", "team-", "f:", "P")  # keep signal labels


def compact_labels(labels):
    keep = [
        l for l in labels
        if any(l.startswith(p) for p in LABEL_PREFIXES)
        or l in ("has reproducible steps", "proposal")
    ]
    return sorted(keep)


def truncate_body(body):
    if not body:
        return ""
    body = body.strip()
    if len(body) <= BODY_MAX_CHARS:
        return body
    return body[:BODY_MAX_CHARS] + "\n...[truncated]"


def main():
    data = json.loads(SRC.read_text())
    out = []
    total_chars = 0
    for iss in data["issues"]:
        compact = {
            "number": iss["number"],
            "title": iss["title"],
            "url": iss["url"],
            "ownership": iss["ownership"],
            "labels": compact_labels(iss["labels"]),
            "body": truncate_body(iss.get("body") or ""),
            "comment_summary": iss.get("comment_summary"),
        }
        total_chars += (
            len(compact["title"])
            + len(compact["body"])
            + len(compact["comment_summary"] or "")
        )
        out.append(compact)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    size_mb = OUT.stat().st_size / (1024 * 1024)
    print(f"Wrote {OUT}")
    print(f"  issues: {len(out)}")
    print(f"  total chars (title+body+summary): {total_chars:,} (~{total_chars//4:,} tokens)")
    print(f"  file size: {size_mb:.2f} MB")


if __name__ == "__main__":
    main()
