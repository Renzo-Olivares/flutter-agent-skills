#!/usr/bin/env python3
"""
Build a mini-batch containing only the issue numbers missing from their summaries.
Writes it to batches/batch_gapfill.json and reports the list.
"""
import json
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"
BATCH_DIR = DATA / "batches"
SUMMARY_DIR = DATA / "summaries"
OUT = BATCH_DIR / "batch_gapfill.json"

targets = []
for bp in sorted(BATCH_DIR.glob("batch_*.json")):
    if "gapfill" in bp.name:
        continue
    batch_id_str = bp.stem.replace("batch_", "")
    sp = SUMMARY_DIR / f"summary_{batch_id_str}.json"
    batch_data = json.loads(bp.read_text())
    if not sp.exists():
        continue
    try:
        s = json.loads(sp.read_text())
    except json.JSONDecodeError:
        continue
    present = set(s.get("summaries", {}).keys())
    for iss in batch_data["issues"]:
        if str(iss["number"]) not in present:
            targets.append((int(batch_id_str), iss))

print(f"Gap: {len(targets)} issues needing summaries")
for batch_id, iss in targets:
    print(f"  batch {batch_id:03d} → #{iss['number']}: {iss['title'][:70]}")

OUT.write_text(
    json.dumps(
        {
            "batch_id": "gapfill",
            "issues": [iss for _, iss in targets],
            "source_batches": sorted({b for b, _ in targets}),
        },
        indent=2,
    )
)
print(f"Wrote {OUT}")
