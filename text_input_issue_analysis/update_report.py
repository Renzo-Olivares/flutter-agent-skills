import re

file_path = "flutter-agent-skills/text_input_issue_analysis/cleanup_reports/internationalization_bidi_text_layout_v4.md"

with open(file_path, "r") as f:
    content = f.read()

# Update counters
content = re.sub(r"Processed: 10 / 44", "Processed: 20 / 44", content)
content = re.sub(r"Tests written: 1", "Tests written: 2", content)
content = re.sub(r"Failed as expected: 1", "Failed as expected: 2", content)
content = re.sub(r"Skip — feature/proposal: 3", "Skip — feature/proposal: 7", content)
content = re.sub(r"Skip — engine-level: 5", "Skip — engine-level: 10", content)

new_issues = """
### #91738 — [Proposal] Add support for automatically switching text input to `RTL` or `LTR` based on first character typed

- **URL:** https://github.com/flutter/flutter/issues/91738
- **Created:** 2021-10-13 (~4.5 y old) · **Updated:** 2023-09-15
- **Reactions:** 5 (THUMBS_UP 4, HEART 1)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `a: internationalization`, `c: proposal`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** Users want automatic directionality detection (RTL/LTR) for `TextField` based on the first character typed, overriding the ambient `Directionality`.

**Why skip-proposal.** This is an API/feature request for automatic direction detection at the framework level.

**Dedup scan.** No duplicates in this batch.


### #91010 — `dart:ui.LineMetrics` should include the line boundaries 

- **URL:** https://github.com/flutter/flutter/issues/91010
- **Created:** 2021-09-30 (~4.5 y old) · **Updated:** 2023-09-19
- **Reactions:** 4 (THUMBS_UP 3, EYES 1)
- **Labels:** `a: text input`, `engine`, `a: typography`, `c: proposal`, `P3`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — feature/proposal**

**Root cause.** `LineMetrics` API currently strips line boundary text ranges (indices) which exist in SkParagraph. Adding this information would avoid workarounds when implementing vertical caret movement.

**Why skip-proposal.** The request is to expose an existing underlying Skia text metric (line boundary ranges) to Dart API via `dart:ui`.

**Dedup scan.** No duplicates in this batch.


### #41324 — TextField/TextFormField labelText and hintText should be right-aligned with TextDirection.rtl

- **URL:** https://github.com/flutter/flutter/issues/41324
- **Created:** 2019-09-25 (~6.6 y old) · **Updated:** 2026-02-16
- **Reactions:** 3 (THUMBS_UP 3)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `a: internationalization`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **write-test** [→ **fail-as-expected**]

**Root cause.** The `labelText` in a `TextField`'s `InputDecoration` fails to align to the right edge when `textDirection: TextDirection.rtl` is applied, acting as if it's LTR.

**Test approach.**
- Render a `TextField` with `textDirection: TextDirection.rtl` and a `labelText`.
- Find the `RenderBox` for both the label and the `TextField`.
- Assert that the right global edge of the label is close to the right global edge of the `TextField`.

**Test:** [`../regression_tests/internationalization_bidi_text_layout_v4/issue_41324_rtl_label_text_alignment_test.dart`](../regression_tests/internationalization_bidi_text_layout_v4/issue_41324_rtl_label_text_alignment_test.dart)

**Test outcome.** Test failed as expected (`Expected: a numeric value within <20.0> of <770.0> Actual: <211.5>`). The label is incorrectly aligned on the left.

**Dedup scan.** No duplicates in this batch.


### #93934 — [Desktop] TextField with pasted CRLF endings has invisible CR char

- **URL:** https://github.com/flutter/flutter/issues/93934
- **Created:** 2021-11-19 (~4.4 y old) · **Updated:** 2024-06-07
- **Reactions:** 2 (THUMBS_UP 2)
- **Labels:** `a: text input`, `framework`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.5`, `found in release: 2.6`, `found in release: 2.8`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **skip — engine-level**

**Root cause.** Pasting text with CRLF (`\\r\\n`) endings causes the `\\r` character to become an invisible, interactable character boundary that traps or skips caret movement differently on Desktop (Windows/macOS).

**Why skip-engine.** How SkParagraph handles `\\r` and determines caret boundary stops at line breaks is an engine text layout issue. Framework just iterates `getWordBoundary` or uses `TextPosition` from the engine.

**Dedup scan.** No duplicates in this batch.


### #117139 — Incorrect selection area in RTL TextField.

- **URL:** https://github.com/flutter/flutter/issues/117139
- **Created:** 2022-12-15 (~3.4 y old) · **Updated:** 2023-07-08
- **Reactions:** 2 (THUMBS_UP 2)
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause.** Selection highlight rects are misaligned when selecting a word followed by a dot at the end of a line in RTL multiline text. Triage confirmed this is a Skia bug (issue 14035) with `getRectsForRange`.

**Why skip-engine.** Text selection boxes are provided by `Paragraph.getBoxesForRange()`, which delegates to SkParagraph.

**Dedup scan.** No duplicates in this batch.


### #181759 — RTL TextField breaks when inserting emojis between existing emojis

- **URL:** https://github.com/flutter/flutter/issues/181759
- **Created:** 2026-01-31 (~0.2 y old) · **Updated:** 2026-03-06
- **Reactions:** 2 (THUMBS_UP 2)
- **Labels:** `a: text input`, `platform-android`, `framework`, `f: material design`, `platform-macos`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Inserting emojis between emojis in RTL fields causes `?` characters or engine aborts due to surrogate pair misinterpretation during IME composition dynamically shifting directionality.

**Why skip-engine.** This is an embedder/engine decoding issue for surrogate pairs or a C++ exception inside `wstring_convert::to_bytes` in the platform channels.

**Dedup scan.** No duplicates in this batch.


### #41641 — [web] Support line height + word spacing in text fields

- **URL:** https://github.com/flutter/flutter/issues/41641
- **Created:** 2019-09-30 (~6.6 y old) · **Updated:** 2024-03-06
- **Reactions:** 1 (THUMBS_UP 1)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `platform-web`, `P3`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — feature/proposal**

**Root cause.** Web engine `TextInput.setStyle` does not support `lineHeight` or `wordSpacing` for native DOM text input integration.

**Why skip-proposal.** Feature request to expand the engine's platform channel interface to DOM elements.

**Dedup scan.** No duplicates in this batch.


### #71318 — TextField RTL input problem with LTR letters/numbers while obscureText is true

- **URL:** https://github.com/flutter/flutter/issues/71318
- **Created:** 2020-11-27 (~5.4 y old) · **Updated:** 2024-07-11
- **Reactions:** 1 (THUMBS_UP 1)
- **Labels:** `a: text input`, `framework`, `engine`, `f: material design`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause.** In RTL obscureText fields, typing LTR characters (like English letters) causes the cursor to incorrectly appear on the left of the dots instead of the right while typing, even though the final text value is correct.

**Why skip-engine.** When `obscureText` is true, the framework replaces all characters with a single dot character. The bidirectional layout algorithm (SkParagraph) then decides the visual order of these dots. Since dots are neutral, typing LTR characters might affect the layout directionality incorrectly in the engine's text shaping.

**Dedup scan.** No duplicates in this batch.


### #78864 — Text does not draw correctly based on text direction

- **URL:** https://github.com/flutter/flutter/issues/78864
- **Created:** 2021-03-23 (~5.1 y old) · **Updated:** 2025-07-22
- **Reactions:** 1 (THUMBS_UP 1)
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 2.1`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause.** Text direction is not properly respected when rendering English or Hebrew formatted times (e.g. `PM 06` vs `06 PM`), producing the same visual output regardless of locale direction.

**Why skip-engine.** This is a text shaping and bidirectional layout algorithm issue happening at the SkParagraph level.

**Dedup scan.** No duplicates in this batch.


### #84317 — Share code between RenderParagraph and RenderEditable

- **URL:** https://github.com/flutter/flutter/issues/84317
- **Created:** 2021-06-10 (~4.9 y old) · **Updated:** 2023-07-08
- **Reactions:** 1 (THUMBS_UP 1)
- **Labels:** `a: text input`, `framework`, `a: typography`, `P2`, `c: tech-debt`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** `RenderParagraph` and `RenderEditable` duplicate a lot of logic (like `WidgetSpan` handling), and the proposal is to refactor them using a mixin or common parent.

**Why skip-proposal.** This is a framework architectural tech-debt refactor request, not a user-facing bug to be tested.

**Dedup scan.** No duplicates in this batch.

## Duplicate clusters"""

# Append before the Duplicate clusters section
content = content.replace("## Duplicate clusters", new_issues)

with open(file_path, "w") as f:
    f.write(content)

print("Updated report successfully.")
