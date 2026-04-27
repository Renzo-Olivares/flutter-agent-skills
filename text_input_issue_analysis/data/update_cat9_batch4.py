import re

file_path = 'flutter-agent-skills/text_input_issue_analysis/cleanup_reports/internationalization_bidi_and_text_layout.md'
with open(file_path, 'r') as f:
    content = f.read()

# Update counters
content = content.replace('- Processed: 25 / 44', '- Processed: 35 / 44')
content = content.replace('- Tests written: 4', '- Tests written: 5')
content = content.replace('  - Failed as expected: 3', '  - Failed as expected: 4')
content = content.replace('- Skip — feature/proposal: 8', '- Skip — feature/proposal: 14')
content = content.replace('- Skip — engine-level: 9', '- Skip — engine-level: 11')
content = content.replace('- Likely-stale (signal-based): 2', '- Likely-stale (signal-based): 3')

entries = """### #13468 — TextSelection.isDirectional is not respected, make it do something useful eg: for Mac

- **URL:** https://github.com/flutter/flutter/issues/13468
- **Created:** 2017-12-09 (~8.3 y old) · **Updated:** 2024-05-09
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `c: proposal`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** `TextSelection.isDirectional` does not currently affect behavior.

**Why skip-proposal / Test approach.** A proposal to give the property functionality or remove it. No regression surface.

**Dedup scan.** Scanned for "isDirectional". No duplicates.

### #33858 — Unicode input should be indicated.

- **URL:** https://github.com/flutter/flutter/issues/33858
- **Created:** 2019-06-04 (~6.9 y old) · **Updated:** 2024-12-13
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `platform-windows`, `platform-linux`, `a: desktop`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Flutter does not show a visual indicator (like an underlined 'u') when a user is entering a Unicode character sequence (e.g., via Ctrl+Shift+U).

**Why skip-proposal / Test approach.** Feature request for visual feedback during text input composition.

**Dedup scan.** Scanned for "Unicode input", "indicator". No duplicates.

### #38503 — TextField doesn't appear within a direction:Axis.vertical Wrap

- **URL:** https://github.com/flutter/flutter/issues/38503
- **Created:** 2019-08-14 (~6.7 y old) · **Updated:** 2024-12-11
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **write-test** → **fail-as-expected**

**Root cause.** Placing a `TextField` inside a `Wrap(direction: Axis.vertical)` throws a layout assertion error because `Wrap` does not provide an unbounded width constraint in the cross axis, and `InputDecorator` requires finite width.

**Test approach.** Drafted a simple test pumping a `TextField` inside a `Wrap(direction: Axis.vertical)`.

**Test:** [`issue_38503_textfield_vertical_wrap_test.dart`](../regression_tests/internationalization_bidi_and_text_layout/issue_38503_textfield_vertical_wrap_test.dart)

**Test outcome.** Fails as expected. Throws an `AssertionError`: `An InputDecorator, which is typically created by a TextField, cannot have an unbounded width.`

**Dedup scan.** Scanned for "vertical Wrap", "unbounded width". No duplicates.

### #54998 — Directional navigation key binding defaults should be limited to those platforms that use it.

- **URL:** https://github.com/flutter/flutter/issues/54998
- **Created:** 2020-04-16 (~6.0 y old) · **Updated:** 2024-07-22
- **Reactions:** 0
- **Labels:** `framework`, `platform-macos`, `a: desktop`, `a: devtools`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **likely-stale (signal-based)**

**Root cause.** Default directional focus key bindings were globally enabled across platforms like macOS where they might not be standard.

**Test approach.** Inactivity and stale labels, plus partial fixes mentioned in comments.

**Dedup scan.** Scanned for "Directional navigation", "key binding defaults". No duplicates.

### #75572 — Let RenderEditable use LineMetrics instead of assuming every line has the same height

- **URL:** https://github.com/flutter/flutter/issues/75572
- **Created:** 2021-02-07 (~5.2 y old) · **Updated:** 2026-03-05
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `f: material design`, `P2`, `c: tech-debt`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal**

**Root cause.** Tech debt tracking issue. `RenderEditable` logic for vertical arrow key traversal assumes uniform line height, causing caret jumps when lines differ drastically in height.

**Why skip-proposal / Test approach.** A proposal to refactor the internal mechanism using `LineMetrics`. 

**Dedup scan.** Scanned for "LineMetrics", "RenderEditable", "line height". No duplicates.

### #87536 — BIDI text painting skipped tests.

- **URL:** https://github.com/flutter/flutter/issues/87536
- **Created:** 2021-08-03 (~4.7 y old) · **Updated:** 2023-07-08
- **Reactions:** 0
- **Labels:** `a: text input`, `c: contributor-productivity`, `framework`, `a: internationalization`, `P2`, `c: tech-debt`, `team: skip-test`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** Tracking issue for `text_painter_rtl_test.dart` skipped tests.

**Why skip-proposal / Test approach.** Test suite maintenance.

**Dedup scan.** Scanned for "skipped tests". No duplicates.

### #92507 — Document "ghost run" and its interaction with `Paragraph.getBoxesForRange`

- **URL:** https://github.com/flutter/flutter/issues/92507
- **Created:** 2021-10-26 (~4.5 y old) · **Updated:** 2023-08-04
- **Reactions:** 0
- **Labels:** `a: text input`, `engine`, `d: api docs`, `a: typography`, `P2`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — feature/proposal**

**Root cause.** Engine documentation request for "ghost run" text layout behaviors.

**Why skip-proposal / Test approach.** Docs request.

**Dedup scan.** Scanned for "ghost run". No duplicates.

### #99139 — [MacOS] Trailing whitespace in multiline TextField overflows and doesn't go to newline.

- **URL:** https://github.com/flutter/flutter/issues/99139
- **Created:** 2022-02-25 (~4.2 y old) · **Updated:** 2024-06-20
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.10`, `found in release: 2.11`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Trailing whitespace in a multiline `TextField` on desktop/macOS does not automatically wrap to a new line; it overflows the container instead.

**Why skip-engine / Test approach.** Text line breaking and wrapping rules are computed by `SkParagraph` in the engine.

**Dedup scan.** Scanned for "Trailing whitespace", "multiline", "overflows". No duplicates in this exact behavior.

### #110470 —   canvas.drawLine() does not paint correctly on Samsung Galaxy Note 20 Ultra

- **URL:** https://github.com/flutter/flutter/issues/110470
- **Created:** 2022-08-29 (~3.7 y old) · **Updated:** 2024-09-26
- **Reactions:** 0
- **Labels:** `a: text input`, `e: device-specific`, `platform-android`, `framework`, `engine`, `f: material design`, `dependency: skia`, `c: rendering`, `P2`, `e: samsung`, `team-android`, `triaged-android`, `found in release: 3.19`
- **Ownership:** `team-android`
- **Decision:** **skip — engine-level**

**Root cause.** Device-specific rendering defect in `canvas.drawLine()` on certain older Samsung devices (GT-I9500, Note 20 Ultra) causing visual artifacts.

**Why skip-engine / Test approach.** Labeled `dependency: skia` and `c: rendering`. Device-specific GPU/rendering bug below the framework.

**Dedup scan.** Scanned for "Samsung", "drawLine". No duplicates.

### #113228 — Provide an API to detect if a TextPosition is located at a soft word wrap

- **URL:** https://github.com/flutter/flutter/issues/113228
- **Created:** 2022-10-10 (~3.5 y old) · **Updated:** 2024-03-06
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `platform-ios`, `framework`, `c: proposal`, `P3`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal**

**Root cause.** Request for a new API via `RenderEditable` to detect if a `TextPosition` is located at a soft word wrap (needed for toggling the iOS toolbar context menu appropriately).

**Why skip-proposal / Test approach.** API feature request.

**Dedup scan.** Scanned for "TextPosition", "soft word wrap". No duplicates.

"""

content = content.replace('## Processed issues\n', '## Processed issues\n\n' + entries)

# Add skip engine items
engine_items = """- #99139 ([MacOS] Trailing whitespace in multiline TextField overflows and doesn't go to newline.)
- #110470 (canvas.drawLine() does not paint correctly on Samsung Galaxy Note 20 Ultra)
"""
content = content.replace('## Skipped — engine-level\n', '## Skipped — engine-level\n' + engine_items)

with open(file_path, 'w') as f:
    f.write(content)

print('Updated report for next 10 issues (25 to 34).')
