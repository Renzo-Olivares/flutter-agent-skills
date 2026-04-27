import re

file_path = 'flutter-agent-skills/text_input_issue_analysis/cleanup_reports/internationalization_bidi_and_text_layout.md'
with open(file_path, 'r') as f:
    content = f.read()

# Update counters
content = content.replace('- Processed: 15 / 44', '- Processed: 25 / 44')
content = content.replace('- Tests written: 3', '- Tests written: 4')
content = content.replace('  - Failed as expected: 2', '  - Failed as expected: 3')
content = content.replace('- Skip — feature/proposal: 5', '- Skip — feature/proposal: 8')
content = content.replace('- Skip — engine-level: 6', '- Skip — engine-level: 9')
content = content.replace('- Likely-stale (signal-based): 0', '- Likely-stale (signal-based): 2')
content = content.replace('- Likely-duplicate: 1', '- Likely-duplicate: 2')

entries = """### #181759 — RTL TextField breaks when inserting emojis between existing emojis

- **URL:** https://github.com/flutter/flutter/issues/181759
- **Created:** 2026-01-31 (~0.2 y old) · **Updated:** 2026-03-06
- **Reactions:** 2
- **Labels:** `a: text input`, `platform-android`, `framework`, `f: material design`, `platform-macos`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Dynamically changing `textDirection` during IME composition in RTL fields with emojis triggers an engine abort/crash due to invalid JSON surrogate pair decoding.

**Why skip-engine / Test approach.** As noted by comments, the fix requires embedder-level C++ fixes in macOS/Linux and Android IME state handling, not framework changes.

**Dedup scan.** Scanned for "emoji", "RTL", "inserting". No duplicates found.

### #41641 — [web] Support line height + word spacing in text fields

- **URL:** https://github.com/flutter/flutter/issues/41641
- **Created:** 2019-09-30 (~6.5 y old) · **Updated:** 2024-03-06
- **Reactions:** 1
- **Labels:** `a: text input`, `c: new feature`, `framework`, `platform-web`, `P3`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — feature/proposal**

**Root cause.** Missing engine API for `TextInput.setStyle` to support line height and word spacing on web text fields.

**Why skip-proposal / Test approach.** API feature request.

**Dedup scan.** Scanned for "line height", "word spacing". No duplicates.

### #71318 — TextField RTL input problem with LTR letters/numbers while obscureText is true

- **URL:** https://github.com/flutter/flutter/issues/71318
- **Created:** 2020-11-27 (~5.4 y old) · **Updated:** 2024-07-11
- **Reactions:** 1
- **Labels:** `a: text input`, `framework`, `engine`, `f: material design`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause.** Characters are rendered in the wrong visual direction while typing LTR characters in an RTL `TextField` when `obscureText` is true. The cursor and bullets appear on the wrong side.

**Why skip-engine / Test approach.** Labeled as an engine typography issue. Visual reordering and cursor placement of BiDi text (especially when obscured) is driven by `SkParagraph`'s layout algorithm.

**Dedup scan.** Scanned for "obscureText", "RTL", "LTR". No exact duplicates.

### #78864 — Text does not draw correctly based on text direction

- **URL:** https://github.com/flutter/flutter/issues/78864
- **Created:** 2021-03-23 (~5.1 y old) · **Updated:** 2025-07-22
- **Reactions:** 1
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 2.1`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **likely-stale (signal-based)**

**Root cause.** Vague report that text "rendered wrongly" when directionality is set to RTL.

**Test approach.** Inactivity since 2021, only 1 reaction, and lack of clear root cause or reproduction details suggests this is stale.

**Dedup scan.** Scanned for "rendered wrongly", "draw correctly". No duplicates.

### #84317 — Share code between RenderParagraph and RenderEditable

- **URL:** https://github.com/flutter/flutter/issues/84317
- **Created:** 2021-06-10 (~4.9 y old) · **Updated:** 2023-07-08
- **Reactions:** 1
- **Labels:** `a: text input`, `framework`, `a: typography`, `P2`, `c: tech-debt`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** Tech debt tracking issue proposing to share code between `RenderParagraph` and `RenderEditable`.

**Why skip-proposal / Test approach.** Internal refactoring proposal, no user-facing regression surface.

**Dedup scan.** Scanned for "RenderParagraph", "RenderEditable", "Share code". No duplicates.

### #86668 — TextField doesn't handle trailing space as characters if textAlign is TextAlign.right/TextAlign.center

- **URL:** https://github.com/flutter/flutter/issues/86668
- **Created:** 2021-07-19 (~4.8 y old) · **Updated:** 2024-09-26
- **Reactions:** 1
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.2`, `found in release: 2.4`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **likely-duplicate**

**Root cause.** Trailing spaces are not treated as characters for layout when `textAlign` is right/center.

**Dedup scan.** This is an exact duplicate of #40648 (which also already had duplicate #90058).

### #103705 — letterSpacing in TextField with monospace font is only applied to right side of the first character until a second character is entered, then letterSpacing is applied correctly to both sides

- **URL:** https://github.com/flutter/flutter/issues/103705
- **Created:** 2022-05-13 (~3.9 y old) · **Updated:** 2023-07-08
- **Reactions:** 1
- **Labels:** `a: text input`, `engine`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.0`, `found in release: 3.1`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **likely-stale (signal-based)**

**Root cause.** Letter spacing was applied incorrectly in Skia for monospace fonts on the first character.

**Test approach.** The comments confirm a fix was merged into Skia and fixes the issue on Flutter 3.3+. The issue remains open likely waiting for closure. It is stale/resolved.

**Dedup scan.** Scanned for "letterSpacing". No duplicates.

### #133930 — No good way to get line metrics for `Text`/`TextField` based widgets.

- **URL:** https://github.com/flutter/flutter/issues/133930
- **Created:** 2023-09-03 (~2.6 y old) · **Updated:** 2024-08-23
- **Reactions:** 1
- **Labels:** `framework`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.13`, `found in release: 3.14`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** The developer requests a framework-level API to retrieve text layout metrics from a `TextField` without manually re-resolving `TextStyle` from the Material theme.

**Why skip-proposal / Test approach.** API feature request for a layout metrics callback.

**Dedup scan.** Scanned for "line metrics". Issue #91010 also requests line metrics boundaries, but targets the engine `dart:ui.LineMetrics` API.

### #174689 — App highlights / selects trailing whitespaces in a multi-line textfield.

- **URL:** https://github.com/flutter/flutter/issues/174689
- **Created:** 2025-08-29 (~0.7 y old) · **Updated:** 2025-09-18
- **Reactions:** 1
- **Labels:** `a: text input`, `platform-android`, `platform-ios`, `a: desktop`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.35`, `found in release: 3.36`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Selecting the first line of a multi-line textfield also highlights the trailing whitespace in accordance to the next line's length.

**Why skip-engine / Test approach.** Selection rectangles are provided by Skia (`SkParagraph::getRectsForRange`). Highlighting anomalies for trailing whitespace are engine-level layout concerns.

**Dedup scan.** Scanned for "highlights", "trailing whitespaces", "selects". No exact duplicates.

### #184240 — Vertical baseline alignment mismatch between Text and collapsed TextField when changing TextLeadingDistribution

- **URL:** https://github.com/flutter/flutter/issues/184240
- **Created:** 2026-03-27 (~0.1 y old) · **Updated:** 2026-04-02
- **Reactions:** 1
- **Labels:** `framework`, `f: material design`, `has reproducible steps`, `team-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **write-test** → **fail-as-expected**

**Root cause.** A `TextField` with `InputDecoration.collapsed` does not align its vertical baseline correctly with a `Text` widget when `TextLeadingDistribution.even` is used in a `Row` with `CrossAxisAlignment.baseline`.

**Test approach.** Wrapped a `Text` and a collapsed `TextField` inside a `Row(crossAxisAlignment: CrossAxisAlignment.baseline)` and verified their actual top-left `dy` offsets. Due to the baseline mismatch, the `Row` offsets one vertically compared to the other.

**Test:** [`issue_184240_baseline_alignment_test.dart`](../regression_tests/internationalization_bidi_and_text_layout/issue_184240_baseline_alignment_test.dart)

**Test outcome.** Fails as expected. `Expected: a numeric value within <0.1> of <0.0>, Actual: <0.7000007629394531>`.

**Dedup scan.** Scanned for "Vertical baseline", "TextLeadingDistribution". No duplicates.

"""

content = content.replace('## Processed issues\n', '## Processed issues\n\n' + entries)

# Add skip engine items
engine_items = """- #181759 (RTL TextField breaks when inserting emojis between existing emojis)
- #71318 (TextField RTL input problem with LTR letters/numbers while obscureText is true)
- #174689 (App highlights / selects trailing whitespaces in a multi-line textfield.)
"""
content = content.replace('## Skipped — engine-level\n', '## Skipped — engine-level\n' + engine_items)

with open(file_path, 'w') as f:
    f.write(content)

print('Updated report for next 10 issues.')
