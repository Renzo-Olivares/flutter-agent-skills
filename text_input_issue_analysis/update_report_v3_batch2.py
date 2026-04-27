import re

report_path = 'cleanup_reports/internationalization_bidi_and_text_layout_v3.md'
with open(report_path, 'r') as f:
    content = f.read()

entries = """
### #71083 — TextFormField (and TextField) widgets do not wrap text correctly

- **URL:** https://github.com/flutter/flutter/issues/71083
- **Created:** 2020-11-23 (~5.4 y old) · **Updated:** 2024-03-06
- **Reactions:** 5 (👍 5)
- **Labels:** `a: text input`, `framework`, `f: material design`, `dependency: skia`, `a: typography`, `P2`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause.** Long strings without spaces (like URLs) break at the last available word boundary or overflow, instead of breaking mid-word (like `break-all` in CSS). This behavior is driven by the engine's text layout engine (Skia/LibTxt).

**Why skip-engine.** Text wrapping algorithms and break rules are implemented natively in the engine. There is no framework-level test that can control or assert on arbitrary word-break policies that the engine does not yet expose.

**Dedup scan.**
  - **Terms / scope:** "wrap", "break", "URL"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #91738 — [Proposal] Add support for automatically switching text input to `RTL` or `LTR` based on first character typed

- **URL:** https://github.com/flutter/flutter/issues/91738
- **Created:** 2021-10-13 (~4.5 y old) · **Updated:** 2023-09-15
- **Reactions:** 5 (👍 4, ❤️ 1)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `a: internationalization`, `c: proposal`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** A proposal to automatically detect text direction based on the first typed character, akin to HTML's `dir="auto"`.

**Why skip-proposal.** This requests a new layout capability and API. It is not a bug with a regression surface.

**Dedup scan.**
  - **Terms / scope:** "auto", "automatically switching", "first character"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #91010 — `dart:ui.LineMetrics` should include the line boundaries 

- **URL:** https://github.com/flutter/flutter/issues/91010
- **Created:** 2021-09-30 (~4.5 y old) · **Updated:** 2023-09-19
- **Reactions:** 4 (👍 3, 👀 1)
- **Labels:** `a: text input`, `engine`, `a: typography`, `c: proposal`, `P3`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — feature/proposal**

**Root cause.** A feature request to expose `TextRange` on `LineMetrics` in the `dart:ui` API, avoiding the need to manually compute line boundaries.

**Why skip-proposal.** Requests an API addition to the engine's `dart:ui` library.

**Dedup scan.**
  - **Terms / scope:** "LineMetrics", "boundaries", "TextRange"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #41324 — TextField/TextFormField labelText and hintText should be right-aligned with TextDirection.rtl

- **URL:** https://github.com/flutter/flutter/issues/41324
- **Created:** 2019-09-25 (~6.5 y old) · **Updated:** 2026-02-16
- **Reactions:** 3 (👍 3)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `a: internationalization`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **write-test** [→ **pass-green, exercises bug path**]

**Root cause.** A bug report from 2019 stating `labelText` inside `InputDecoration` fails to respect `TextDirection.rtl`.

**Test approach.** 
  - Render a `TextField` with `TextDirection.rtl` and a `labelText`.
  - Extract the global layout offset of the label and the field itself.
  - Assert that the label is visually closer to the right edge than the left edge.

**Test:** [`issue_41324_label_rtl_test.dart`](../../regression_tests/internationalization_bidi_and_text_layout_v3/issue_41324_label_rtl_test.dart)

**Test outcome.** 
  - `pass-green, exercises bug path`. The label renders on the right edge properly. Given recent framework commits likely fixed `InputDecoration` alignment, this old issue is stale.

**Dedup scan.**
  - **Terms / scope:** "labelText", "hintText", "right-aligned"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #93934 — [Desktop] TextField with pasted CRLF endings has invisible CR char

- **URL:** https://github.com/flutter/flutter/issues/93934
- **Created:** 2021-11-19 (~4.4 y old) · **Updated:** 2024-06-07
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `framework`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.5`, `found in release: 2.6`, `found in release: 2.8`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **skip — engine-level**

**Root cause.** On Desktop platforms, pasting text with `\r\n` leaves an invisible `\r` character. The engine/Skia renders it as a zero-width space, causing the cursor to "stick" or require two arrow presses to cross the line ending.

**Why skip-engine.** While the framework handles the text string, the core issue is the low-level rendering logic making `\r` zero-width but still physically present in the layout nodes. This requires engine/embedder fixes.

**Dedup scan.**
  - **Terms / scope:** "CRLF", "CR char", "invisible", "\\r"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #117139 — Incorrect selection area in RTL TextField.

- **URL:** https://github.com/flutter/flutter/issues/117139
- **Created:** 2022-12-15 (~3.3 y old) · **Updated:** 2023-07-08
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause.** Selection rects for RTL text ending with a dot/newline are mismatched. This is a known Skia SkParagraph `getRectsForRange` API bug (tracked upstream as chromium/14035).

**Why skip-engine.** The selection boxes are supplied by `getRectsForRange` from the engine. The framework merely paints them; it cannot be fixed here.

**Dedup scan.**
  - **Terms / scope:** "Incorrect selection area", "selection", "RTL"
  - **Hits, classified:** 
    - **adjacent-different:** #39755 (Inaccurate selection for justified non-Latin). Distinct root causes (justification offset vs newline handling).
  - **Cluster decision:** none

### #181759 — RTL TextField breaks when inserting emojis between existing emojis

- **URL:** https://github.com/flutter/flutter/issues/181759
- **Created:** 2026-01-31 (~0.2 y old) · **Updated:** 2026-03-06
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `platform-android`, `framework`, `f: material design`, `platform-macos`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Changing `textDirection` dynamically during active IME composition causes a `wstring_convert::to_bytes` exception in the macOS/Linux engine pipeline.

**Why skip-engine.** The crash happens inside the engine's `PlatformViewEmbedder` / `FlutterMacOS` layers due to C++ unhandled exceptions (`-fno-exceptions`).

**Dedup scan.**
  - **Terms / scope:** "emoji", "breaks", "inserting", "crash"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #41641 — [web] Support line height + word spacing in text fields

- **URL:** https://github.com/flutter/flutter/issues/41641
- **Created:** 2019-09-30 (~6.5 y old) · **Updated:** 2024-03-06
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `platform-web`, `P3`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — feature/proposal**

**Root cause.** The web engine's `TextInput.setStyle` lacks support for propagating line height and word spacing to the DOM.

**Why skip-proposal.** Requests a feature parity addition to the engine-to-platform communication channel.

**Dedup scan.**
  - **Terms / scope:** "line height", "word spacing", "setStyle"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #71318 — TextField RTL input problem with LTR letters/numbers while obscureText is true

- **URL:** https://github.com/flutter/flutter/issues/71318
- **Created:** 2020-11-27 (~5.4 y old) · **Updated:** 2024-07-11
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `engine`, `f: material design`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **write-test** [→ **fail-as-expected**]

**Root cause.** When `obscureText` is true in an RTL field, typed LTR characters are converted to neutral bullets (`•`). The text layout treats these neutral bullets as RTL based on the field's directionality, rendering them right-to-left. Thus, typing "ab" makes the caret visually move to the left instead of the right.

**Test approach.** 
  - Render an RTL `TextField` with `obscureText: true`.
  - Type "ab" (LTR letters).
  - Extract the visual offsets of the selection endpoints for offset 1 and offset 2.
  - Assert that the caret moves to the right visually (`dx` of offset 2 > `dx` of offset 1).

**Test:** [`issue_71318_obscure_rtl_test.dart`](../../regression_tests/internationalization_bidi_and_text_layout_v3/issue_71318_obscure_rtl_test.dart)

**Test outcome.** 
  - `fail-as-expected`. The test fails because `caretOffset.dx` (762.25) is NOT greater than `caretOffset1.dx` (778.75). The caret moved left instead of right.

**Dedup scan.**
  - **Terms / scope:** "obscureText", "LTR letters", "cursor", "typing"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #78864 — Text does not draw correctly based on text direction

- **URL:** https://github.com/flutter/flutter/issues/78864
- **Created:** 2021-03-23 (~5.1 y old) · **Updated:** 2025-07-22
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 2.1`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause.** BiDi rendering logic outputs `PM 06` instead of `06 PM` when the text direction is forced to RTL for a mixed string. The underlying layout formatting for neutral/weak characters fails.

**Why skip-engine.** This is another artifact of the underlying BiDi algorithm in Skia/SkParagraph misinterpreting formatting boundaries.

**Dedup scan.**
  - **Terms / scope:** "draw correctly", "text direction", "rendered wrongly"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

"""

# update counters
content = re.sub(r'Processed: 9 \/ 44', 'Processed: 19 / 44', content)
content = re.sub(r'Tests written: 1', 'Tests written: 3', content)
content = re.sub(r'Failed as expected: 1', 'Failed as expected: 2', content)
content = re.sub(r'Pass-green, exercises bug path: 0', 'Pass-green, exercises bug path: 1', content)

# update process issues
content = content.replace('## Duplicate clusters\n', entries + '\n## Duplicate clusters\n')

# add to likely stale
stale = """
- #41324 — `labelText` alignment passes green framework regression test; highly likely fixed in recent `InputDecoration` refactors.
"""
content = content.replace('## Likely-stale candidates for closure review\n', '## Likely-stale candidates for closure review\n' + stale)

# add to skip engine
skip_engine = """- #71083 — Skia/LibTxt word-breaking constraints
- #93934 — Skia zero-width rendering of pasted \\r
- #117139 — SkParagraph getRectsForRange newline bug
- #181759 — macOS/Linux embedder text-input crash (wstring_convert)
- #78864 — SkParagraph BiDi rendering of weak boundaries
"""
content = content.replace('## Skipped — engine-level\n', '## Skipped — engine-level\n' + skip_engine)

with open(report_path, 'w') as f:
    f.write(content)
