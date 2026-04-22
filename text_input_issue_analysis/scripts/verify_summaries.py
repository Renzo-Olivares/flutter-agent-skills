#!/usr/bin/env python3
"""
Verify each summary file covers every issue in its batch.

Reports:
- Missing: batch has no summary file at all
- Incomplete: summary file exists but is missing keys for some issue numbers
- Malformed: summary file doesn't match expected shape
- Complete: every issue in the batch has a string or null entry

Prints a sorted list of batch IDs that still need to be (re)run.
"""
import json
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"
BATCH_DIR = DATA / "batches"
SUMMARY_DIR = DATA / "summaries"


def main():
    batches = sorted(BATCH_DIR.glob("batch_*.json"))
    needs_rerun = []
    rows = []

    # Load the gapfill summary as an extra pool of keys that count as present.
    gapfill_keys = set()
    gfp = SUMMARY_DIR / "summary_gapfill.json"
    if gfp.exists():
        try:
            gapfill_keys = set(json.loads(gfp.read_text()).get("summaries", {}).keys())
        except json.JSONDecodeError:
            pass

    for bp in batches:
        batch_id_str = bp.stem.replace("batch_", "")
        if batch_id_str == "gapfill":
            continue
        batch_id = int(batch_id_str)
        batch_data = json.loads(bp.read_text())
        expected_numbers = {str(i["number"]) for i in batch_data["issues"]}

        sp = SUMMARY_DIR / f"summary_{batch_id_str}.json"
        if not sp.exists():
            rows.append((batch_id, len(expected_numbers), "MISSING", None, None))
            needs_rerun.append(batch_id)
            continue

        try:
            s = json.loads(sp.read_text())
        except json.JSONDecodeError as e:
            rows.append((batch_id, len(expected_numbers), "MALFORMED", f"JSON error: {e}", None))
            needs_rerun.append(batch_id)
            continue

        if "summaries" not in s or not isinstance(s["summaries"], dict):
            rows.append((batch_id, len(expected_numbers), "MALFORMED", "missing/bad `summaries`", None))
            needs_rerun.append(batch_id)
            continue

        present_keys = set(s["summaries"].keys()) | gapfill_keys
        missing_keys = expected_numbers - present_keys
        extra_keys = present_keys - expected_numbers

        null_count = sum(1 for v in s["summaries"].values() if v is None)
        real_count = len(s["summaries"]) - null_count

        if missing_keys:
            rows.append(
                (
                    batch_id,
                    len(expected_numbers),
                    "INCOMPLETE",
                    f"missing {len(missing_keys)}: {sorted(missing_keys)[:5]}...",
                    (real_count, null_count),
                )
            )
            needs_rerun.append(batch_id)
        else:
            extra_note = f" (+{len(extra_keys)} extra keys)" if extra_keys else ""
            rows.append((batch_id, len(expected_numbers), "OK" + extra_note, None, (real_count, null_count)))

    # Print report
    print(f"{'batch':<6} {'issues':<7} {'status':<30} {'counts':<20} note")
    print("-" * 100)
    for bid, n_exp, status, note, counts in rows:
        counts_str = f"{counts[0]} real, {counts[1]} null" if counts else "-"
        print(f"{bid:<6d} {n_exp:<7d} {status:<30} {counts_str:<20} {note or ''}")

    print()
    print(f"Batches needing (re)run ({len(needs_rerun)}): {needs_rerun}")


if __name__ == "__main__":
    main()
