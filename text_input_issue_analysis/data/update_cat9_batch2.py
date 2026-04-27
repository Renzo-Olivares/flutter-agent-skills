import re

file_path = 'flutter-agent-skills/text_input_issue_analysis/cleanup_reports/internationalization_bidi_and_text_layout.md'
with open(file_path, 'r') as f:
    content = f.read()

# Update counters
content = content.replace('- Processed: 5 / 44', '- Processed: 15 / 44')
content = content.replace('- Tests written: 0', '- Tests written: 3')
content = content.replace('  - Failed as expected: 0', '  - Failed as expected: 2')
content = content.replace('  - Test error: 0', '  - Test error: 1')
content = content.replace('- Skip — feature/proposal: 2', '- Skip — feature/proposal: 5')
content = content.replace('- Skip — engine-level: 3', '- Skip — engine-level: 6')
content = content.replace('- Likely-duplicate: 0', '- Likely-duplicate: 1')
content = content.replace('- Duplicate clusters (tentative): 0', '- Duplicate clusters (tentative): 1 (RTL-SEL-1)')

entries = """### #78660 — Arrow keys in RTL move the wrong way

- **URL:** https://github.com/flutter/flutter/issues/78660
- **Created:** 2021-03-19 (~5.1 y old) · **Updated:** 2024-03-06
- **Reactions:** 15
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 2.1`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **write-test** → **fail-as-expected**

**Root cause.** Pressing left/right arrow keys in an RTL text field moves the caret in the logical direction (forward/backward) rather than the visual direction (left/right).

**Test approach.** We create an RTL `TextField` initialized with 'مرحبا', place the caret at offset 0 (which is visually the far right edge), simulate a `LogicalKeyboardKey.arrowLeft` press, and assert the offset increases (which logically moves forward, but visually moves left).

**Test:** [`issue_78660_arrow_keys_in_rtl_test.dart`](../regression_tests/internationalization_bidi_and_text_layout/issue_78660_arrow_keys_in_rtl_test.dart)

**Test outcome.** Fails as expected. `Expected: <1> Actual: <0>`. The framework's default intent handler currently does not implement visual traversal and keeps the caret at offset 0.

**Dedup scan.** Scanned for "arrow keys", "RTL", "wrong way". No exact duplicates.

### #36854 — Feature request: Setting paragraph distance in Text and TextField

- **URL:** https://github.com/flutter/flutter/issues/36854
- **Created:** 2019-07-24 (~6.7 y old) · **Updated:** 2024-03-06
- **Reactions:** 12
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `a: typography`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** The user is requesting a new feature to control paragraph spacing natively in `Text` and `TextField`. 

**Why skip-proposal / Test approach.** This is a clear API feature request. No regression surface to test.

**Dedup scan.** Scanned for "paragraph distance", "spacing". No duplicates.

### #39755 — Selection of any justified-text is inaccurate in non-latin languages

- **URL:** https://github.com/flutter/flutter/issues/39755
- **Created:** 2019-09-03 (~6.6 y old) · **Updated:** 2024-03-06
- **Reactions:** 10
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause.** Selection highlight rects are visually misaligned or inaccurate when selecting RTL or justified text in non-Latin scripts (Korean, Arabic, Hebrew, Persian).

**Why skip-engine / Test approach.** The bug resides in Skia's `SkParagraph::getRectsForRange` API, which provides the framework with the coordinates for the selection boxes. Framework tests cannot fix or bypass the engine's text layout calculations.

**Dedup scan.** Scanned for "selection", "inaccurate", "highlight". Closely related to #117139, which specifically names the Skia API. Grouped into tentative cluster RTL-SEL-1.

### #90058 — TextFormField with textAlign: TextAlign.right  whitespace doesn't show unless text is entered.

- **URL:** https://github.com/flutter/flutter/issues/90058
- **Created:** 2021-09-14 (~4.6 y old) · **Updated:** 2025-08-13
- **Reactions:** 6
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.5`, `found in release: 2.6`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **likely-duplicate**

**Root cause.** Duplicate of #40648. Trailing whitespace is dropped in right-aligned text fields due to engine layout.

**Dedup scan.** Exact duplicate of #40648, which we previously processed.

### #71083 — TextFormField (and TextField) widgets do not wrap text correctly

- **URL:** https://github.com/flutter/flutter/issues/71083
- **Created:** 2020-11-23 (~5.4 y old) · **Updated:** 2024-03-06
- **Reactions:** 5
- **Labels:** `a: text input`, `framework`, `f: material design`, `dependency: skia`, `a: typography`, `P2`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause.** Long unbreakable strings (like URLs) are wrapped at the word boundary closest to the end of the line, rather than breaking the word itself at the bounding edge.

**Why skip-engine / Test approach.** The issue is labeled `dependency: skia` and is purely an engine-level text layout (line breaking) behavior in `SkParagraph`.

**Dedup scan.** Scanned for "wrap text correctly", "word boundary". No duplicates found.

### #91738 — [Proposal] Add support for automatically switching text input to `RTL` or `LTR` based on first character typed

- **URL:** https://github.com/flutter/flutter/issues/91738
- **Created:** 2021-10-13 (~4.5 y old) · **Updated:** 2023-09-15
- **Reactions:** 5
- **Labels:** `a: text input`, `c: new feature`, `framework`, `a: internationalization`, `c: proposal`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** User is requesting automatic text direction detection based on content (e.g., HTML's `dir="auto"`).

**Why skip-proposal / Test approach.** This is a proposal for a new feature utilizing ICU uBiDi API.

**Dedup scan.** Scanned for "automatically switching", "dir=auto". No duplicates.

### #91010 — `dart:ui.LineMetrics` should include the line boundaries 

- **URL:** https://github.com/flutter/flutter/issues/91010
- **Created:** 2021-09-30 (~4.5 y old) · **Updated:** 2023-09-19
- **Reactions:** 4
- **Labels:** `a: text input`, `engine`, `a: typography`, `c: proposal`, `P3`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — feature/proposal**

**Root cause.** Proposal to expose `TextRange` on `dart:ui.LineMetrics` to make vertical caret movement easier to implement.

**Why skip-proposal / Test approach.** This is a proposal to expand the `dart:ui` engine API.

**Dedup scan.** Scanned for "LineMetrics", "boundaries". No duplicates.

### #41324 — TextField/TextFormField labelText and hintText should be right-aligned with TextDirection.rtl

- **URL:** https://github.com/flutter/flutter/issues/41324
- **Created:** 2019-09-25 (~6.5 y old) · **Updated:** 2026-02-16
- **Reactions:** 3
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `a: internationalization`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **write-test** → **fail-as-expected**

**Root cause.** When a `TextField` explicitly sets `textDirection: TextDirection.rtl`, the `labelText` does not correctly align to the right edge.

**Test approach.** Drafted a test with `TextField(textDirection: TextDirection.rtl)` and measured the x-coordinate of the `labelText` right edge relative to the field width.

**Test:** [`issue_41324_rtl_label_alignment_test.dart`](../regression_tests/internationalization_bidi_and_text_layout/issue_41324_rtl_label_alignment_test.dart)

**Test outcome.** Fails as expected. `Expected: a value greater than <350.0>, Actual: <80.0>`. The label rendering defaults to LTR layout placement when the ambient `Directionality` is LTR.

**Dedup scan.** Scanned for "labelText right-aligned", "hintText". No duplicates.

### #93934 — [Desktop] TextField with pasted CRLF endings has invisible CR char

- **URL:** https://github.com/flutter/flutter/issues/93934
- **Created:** 2021-11-19 (~4.4 y old) · **Updated:** 2024-06-07
- **Reactions:** 2
- **Labels:** `a: text input`, `framework`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.5`, `found in release: 2.6`, `found in release: 2.8`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **write-test** → **test-error**

**Root cause.** Pasting text with CRLF (`\r\n`) endings causes the `\r` character to be inserted as an invisible character, disrupting arrow key navigation and rendering.

**Test approach.** Attempted to test by simulating a paste from clipboard with `\r\n` and asserting caret movement using arrow keys.

**Test:** [`issue_93934_crlf_paste_test.dart`](../regression_tests/internationalization_bidi_and_text_layout/issue_93934_crlf_paste_test.dart)

**Test outcome.** Test errored/timed out due to hanging during the simulation of the system clipboard paste intent in `testWidgets`.

**Dedup scan.** Scanned for "CRLF", "invisible CR". No duplicates.

### #117139 — Incorrect selection area in RTL TextField.

- **URL:** https://github.com/flutter/flutter/issues/117139
- **Created:** 2022-12-15 (~3.3 y old) · **Updated:** 2023-07-08
- **Reactions:** 2
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause.** A dot at the end of a line followed by another line in RTL causes the selection area to render incorrectly.

**Why skip-engine / Test approach.** Confirmed by triage to be a Skia `getRectsForRange` API bug (Chromium issue 14035).

**Dedup scan.** Scanned for "selection area", "getRectsForRange". Closely related to #39755. Grouped into tentative cluster RTL-SEL-1.

"""

content = content.replace('## Processed issues\n', '## Processed issues\n\n' + entries)

# Add duplicate clusters
cluster_entry = """- **RTL-SEL-1** RTL selection rect inaccuracies (Canonical: #117139, Members: #39755)
"""
content = content.replace('## Duplicate clusters\n', '## Duplicate clusters\n\n' + cluster_entry)

# Add skip engine items
engine_items = """- #39755 (Selection of any justified-text is inaccurate in non-latin languages)
- #71083 (TextFormField (and TextField) widgets do not wrap text correctly)
- #117139 (Incorrect selection area in RTL TextField.)
"""
content = content.replace('## Skipped — engine-level\n', '## Skipped — engine-level\n' + engine_items)

with open(file_path, 'w') as f:
    f.write(content)

print('Updated report for 10 issues.')
