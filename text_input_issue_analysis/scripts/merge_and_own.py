#!/usr/bin/env python3
"""
Merge team-text-input + a: text input (old/new) fetch results.

- Deduplicate by issue number
- Derive ownership from team-* labels:
    exactly one team-* label => that team name
    multiple team-* labels   => "undetermined"
    no team-* labels         => "orphaned"
- Keep comments_raw and comment_count for the summarization step
- Emit stats for sanity-check

Output: merged_raw.json (still missing comment_summary and category)
"""
import json
from collections import Counter
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"
SOURCES = [
    DATA / "raw" / "team_text_input.json",
    DATA / "raw" / "a_text_input_old.json",
    DATA / "raw" / "a_text_input_new.json",
]
OUT = DATA / "merged_raw.json"


def derive_ownership(labels):
    teams = [l for l in labels if l.startswith("team-")]
    if len(teams) == 1:
        return teams[0]
    if len(teams) > 1:
        return "undetermined"
    return "orphaned"


def main():
    by_number = {}
    seen_in = {}
    for src in SOURCES:
        state = json.loads(src.read_text())
        for iss in state["issues"]:
            seen_in.setdefault(iss["number"], set()).add(src.stem)
            # Later sources won't overwrite earlier — pick first non-None body/comments.
            existing = by_number.get(iss["number"])
            if existing is None:
                by_number[iss["number"]] = iss
            # If same number appears in multiple sources, merge label sets defensively
            # (GitHub returns label lists at snapshot time; they should agree, but guard anyway).
            else:
                existing_labels = set(existing["labels"])
                new_labels = set(iss["labels"])
                if existing_labels != new_labels:
                    merged = sorted(existing_labels | new_labels)
                    print(f"  label mismatch on #{iss['number']}; merged -> {len(merged)}")
                    existing["labels"] = merged

    # Derive ownership and assemble final list.
    issues = []
    ownership_counter = Counter()
    for iss in by_number.values():
        iss["ownership"] = derive_ownership(iss["labels"])
        ownership_counter[iss["ownership"]] += 1
        issues.append(iss)

    # Sort by issue number for stable output.
    issues.sort(key=lambda x: x["number"])

    # Comment distribution stats.
    counts = [i["comment_count"] for i in issues]
    counts_sorted = sorted(counts)
    total_comments = sum(counts)
    zero = sum(1 for c in counts if c == 0)
    small = sum(1 for c in counts if 1 <= c <= 5)
    large = sum(1 for c in counts if c >= 50)
    median = counts_sorted[len(counts_sorted) // 2] if counts else 0
    mean = total_comments / len(counts) if counts else 0
    max_c = max(counts) if counts else 0

    # Raw source tallies (for sanity).
    by_source = Counter()
    multiple_sources = 0
    for n, srcs in seen_in.items():
        for s in srcs:
            by_source[s] += 1
        if len(srcs) > 1:
            multiple_sources += 1

    print(f"Total unique issues: {len(issues)}")
    print(f"By source (with duplicates): {dict(by_source)}")
    print(f"Issues appearing in more than one source (team + a: text input): {multiple_sources}")
    print(f"Ownership breakdown: {dict(ownership_counter)}")
    print(
        f"Comments: total={total_comments} zero={zero} 1-5={small} >=50={large} "
        f"median={median} mean={mean:.2f} max={max_c}"
    )

    out_payload = {
        "sources": [s.name for s in SOURCES],
        "issues": issues,
    }
    OUT.write_text(json.dumps(out_payload, indent=2))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
