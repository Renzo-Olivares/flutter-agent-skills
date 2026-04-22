#!/usr/bin/env python3
"""
Split merged_raw.json into token-bounded batches for subagent summarization.

Strategy:
- Skip issues with zero comments (comment_summary stays None).
- Oversized issues (estimated > SOLO_THRESHOLD tokens) each get their own batch.
- Pack remaining issues greedily into batches targeting BATCH_TOKEN_TARGET.

Each batch file contains:
{
  "batch_id": 7,
  "issues": [
     {"number": 123, "title": "...", "body": "...", "labels": [...], "comments": ["...", ...]},
     ...
  ]
}
"""
import json
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"
SRC = DATA / "merged_raw.json"
BATCH_DIR = DATA / "batches"
BATCH_DIR.mkdir(exist_ok=True)

# Tokens are approximated as chars/4.
CHARS_PER_TOKEN = 4
BATCH_TOKEN_TARGET = 90_000  # input tokens per batch
SOLO_THRESHOLD = 30_000  # issues above this go solo


def est_tokens_for(issue):
    c = len(issue.get("title") or "")
    c += len(issue.get("body") or "")
    c += sum(len(b) for b in issue["comments_raw"])
    return c // CHARS_PER_TOKEN


def issue_to_batch_form(issue):
    return {
        "number": issue["number"],
        "title": issue["title"],
        "body": issue["body"],
        "labels": issue["labels"],
        "comments": issue["comments_raw"],
    }


def main():
    data = json.loads(SRC.read_text())
    issues = data["issues"]
    commented = [i for i in issues if i["comment_count"] > 0]
    print(f"Total issues: {len(issues)}, with comments: {len(commented)}")

    # Sort by size descending so oversized land in their own batches first.
    commented.sort(key=est_tokens_for, reverse=True)

    batches = []
    current = []
    current_tokens = 0
    solo_count = 0

    for iss in commented:
        tok = est_tokens_for(iss)
        if tok >= SOLO_THRESHOLD:
            batches.append([iss])
            solo_count += 1
            continue
        if current and current_tokens + tok > BATCH_TOKEN_TARGET:
            batches.append(current)
            current = []
            current_tokens = 0
        current.append(iss)
        current_tokens += tok

    if current:
        batches.append(current)

    # Wipe and rewrite batch dir.
    for old in BATCH_DIR.glob("batch_*.json"):
        old.unlink()

    manifest = []
    for i, b in enumerate(batches):
        path = BATCH_DIR / f"batch_{i:03d}.json"
        tok_total = sum(est_tokens_for(x) for x in b)
        path.write_text(
            json.dumps(
                {
                    "batch_id": i,
                    "est_tokens": tok_total,
                    "issues": [issue_to_batch_form(x) for x in b],
                },
                indent=2,
            )
        )
        manifest.append(
            {
                "batch_id": i,
                "path": str(path),
                "issue_count": len(b),
                "est_tokens": tok_total,
                "issue_numbers": [x["number"] for x in b],
            }
        )

    (DATA / "batch_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"Wrote {len(batches)} batches; {solo_count} solo. Tokens: {sum(m['est_tokens'] for m in manifest):,}")
    print("Per-batch sizes:")
    for m in manifest:
        print(f"  batch {m['batch_id']:03d}: {m['issue_count']:4d} issues, ~{m['est_tokens']:>7,} tokens")


if __name__ == "__main__":
    main()
