# Internationalization, BiDi, and text layout Cleanup Report (v3)

This report covers the "Internationalization, BiDi, and text layout" category from the `2026-04-17` snapshot.
Workflow per [`CLEANUP_REPORT_FORMAT.md`](../CLEANUP_REPORT_FORMAT.md).
Note: This is a v3 audit, run independently from previous reports.

## Running summary

- Processed: 44 / 44
- Tests written: 7
  - Failed as expected: 4
  - Pass-green, exercises bug path: 3
  - Pass-green, does not exercise bug path: 0
  - Test error: 0
- Duplicate clusters (tentative): 1 (TRL-SPC-1)
- Cross-category sibling/split-issue links: 0

## Decision types
- `write-test`
- `skip — feature/proposal`
- `skip — engine-level`
- `skip — needs native-platform verification`
- `likely-stale (signal-based)`
- `likely-duplicate`

## Processed issues

### #61069 — [proposal] ability to change text overflow on the TextField

- **URL:** https://github.com/flutter/flutter/issues/61069
- **Created:** 2020-07-08 (~5.8 y old) · **Updated:** 2025-07-18
- **Reactions:** 65 (👍 65)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `c: proposal`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** This is a feature request to add an `overflow` parameter to `TextField` and `TextFormField` to allow showing an ellipsis when text exceeds the available space.

**Why skip-proposal.** The issue requests a new API surface (`overflow`) on the `TextField` widget. There is no regression surface to test as it is a missing feature, not a bug.

**Dedup scan.**
  - **Terms / scope:** "overflow", "ellipsis", "auto_size_text_field"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #51258 — Need to find how much of a long word could fit in one line before an unnatural line break

- **URL:** https://github.com/flutter/flutter/issues/51258
- **Created:** 2020-02-22 (~6.2 y old) · **Updated:** 2023-07-08
- **Reactions:** 28 (👍 24, 👀 4)
- **Labels:** `a: text input`, `framework`, `a: typography`, `c: proposal`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** This is a feature request for a word/line breaker API to allow measuring how much of a long word fits on a line before wrapping, to assist with custom text layout.

**Why skip-proposal.** The issue asks for a new layout measurement API. There is no existing buggy behavior to write a regression test for.

**Dedup scan.**
  - **Terms / scope:** "line break", "measure", "word break"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #77023 — [Web] [CanvasKit][Feature Request]: Load fonts as soon as detecting browser locale

- **URL:** https://github.com/flutter/flutter/issues/77023
- **Created:** 2021-03-02 (~5.1 y old) · **Updated:** 2025-10-30
- **Reactions:** 21 (👍 17, 👀 4)
- **Labels:** `a: text input`, `c: new feature`, `a: internationalization`, `a: typography`, `platform-web`, `c: proposal`, `c: rendering`, `e: web_canvaskit`, `P2`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level**

**Root cause.** When using the CanvasKit renderer on web, typing non-Latin characters (like Chinese) initially shows tofu/gibberish boxes until the font is dynamically loaded. The HTML renderer does not have this issue.

**Why skip-engine.** The issue is rooted in how the CanvasKit web engine handles dynamic font loading and caching upon encountering unknown glyphs. There is no framework-level test that can simulate or catch this web-engine font loading sequence.

**Dedup scan.**
  - **Terms / scope:** "CanvasKit", "font", "locale", "tofu", "gibberish"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #34610 — Mixing RTL and LTR text bugs

- **URL:** https://github.com/flutter/flutter/issues/34610
- **Created:** 2019-06-17 (~6.8 y old) · **Updated:** 2024-03-06
- **Reactions:** 18 (👍 14, 🚀 1, 👀 3)
- **Labels:** `a: text input`, `framework`, `engine`, `a: typography`, `customer: crowd`, `P2`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — engine-level**

**Root cause.** Mixed LTR/RTL text exhibits strange behavior (deletion, emoji placement, spaces). A core contributor identified the root cause as the engine's `ParagraphStyle` directionality remaining LTR for mixed text, causing spaces to be inserted incorrectly at the engine level. Fixes require SkParagraph updates.

**Why skip-engine.** The text layout and deletion order for mixed directionality are calculated in the Skia/SkParagraph engine layers. Framework tests lack the primitives to reliably assert on these low-level text engine artifacts.

**Dedup scan.**
  - **Terms / scope:** "Mixing RTL and LTR", "directionality", "SkParagraph"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #40648 — Trailing space doesn't work with TextField with TextAlign.right 

- **URL:** https://github.com/flutter/flutter/issues/40648
- **Created:** 2019-09-17 (~6.6 y old) · **Updated:** 2025-01-29
- **Reactions:** 16 (👍 16)
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.5`, `found in release: 2.6`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause.** When `textAlign` is `TextAlign.right`, trailing spaces are not rendered. The comments link this to a Skia bug (issue 11933) where `SkParagraph` treats trailing whitespace incorrectly or trims it during alignment.

**Why skip-engine.** The text alignment and whitespace rendering are computed by the Skia engine. A framework-level test cannot easily measure the rendered width of the trailing space without resorting to flaky image/golden tests, and the underlying fix is in Skia.

**Dedup scan.**
  - **Terms / scope:** "TextAlign.right", "trailing space", "whitespace doesn't show"
  - **Hits, classified:** 
    - **duplicate:** #90058 (TextFormField with textAlign: TextAlign.right whitespace doesn't show unless text is entered)
  - **Cluster decision:** start `TRL-SPC-1`

### #78660 — Arrow keys in RTL move the wrong way

- **URL:** https://github.com/flutter/flutter/issues/78660
- **Created:** 2021-03-19 (~5.1 y old) · **Updated:** 2024-03-06
- **Reactions:** 15 (👍 15)
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 2.1`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **write-test** [→ **fail-as-expected**]

**Root cause.** In RTL text, the left/right arrow keys move the caret in the wrong logical/visual direction. The framework's traversal actions use a `forward` boolean rather than strictly respecting visual order based on text direction.

**Test approach.** 
  - Create a `TextField` with `TextDirection.rtl`.
  - Set the initial caret offset to 0.
  - Send `LogicalKeyboardKey.arrowLeft` event.
  - Assert that the caret's `baseOffset` increases, meaning it moved left visually.

**Test:** [`issue_78660_arrow_keys_rtl_test.dart`](../../regression_tests/internationalization_bidi_and_text_layout_v3/issue_78660_arrow_keys_rtl_test.dart)

**Test outcome.** 
  - `fail-as-expected`. The test expects the offset to move to 1, but it stays at 0 because the framework processes the left arrow as moving logically left (which for RTL means moving to the start of the string, which is already 0), failing the test assertion.

**Dedup scan.**
  - **Terms / scope:** "Arrow keys", "RTL", "wrong way", "caret left"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #36854 — Feature request: Setting paragraph distance in Text and TextField

- **URL:** https://github.com/flutter/flutter/issues/36854
- **Created:** 2019-07-24 (~6.8 y old) · **Updated:** 2024-03-06
- **Reactions:** 12 (👍 12)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `a: typography`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** A feature request to add control over paragraph spacing (distance between paragraphs) in `Text` and `TextField` widgets.

**Why skip-proposal.** Requests a new styling API. There is no bug to write a regression test for.

**Dedup scan.**
  - **Terms / scope:** "paragraph distance", "paragraph spacing"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #39755 — Selection of any justified-text is inaccurate in non-latin languages

- **URL:** https://github.com/flutter/flutter/issues/39755
- **Created:** 2019-09-03 (~6.7 y old) · **Updated:** 2024-03-06
- **Reactions:** 10 (👍 9, 👀 1)
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause.** Selection highlight boxes are inaccurate in non-Latin scripts (Arabic, Hebrew, Korean), particularly when text is mixed direction. A maintainer noted that the `justification_x_offset` is likely missing or misapplied in `LibTxt` / the text layout engine.

**Why skip-engine.** The selection rect measurements are provided by the low-level text engine (`LibTxt` / `SkParagraph`). The framework merely paints the rects it receives. This cannot be meaningfully tested purely at the framework level without reproducing the engine's internal offset logic.

**Dedup scan.**
  - **Terms / scope:** "justified-text", "inaccurate selection", "selection highlight"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #90058 — TextFormField with textAlign: TextAlign.right whitespace doesn't show unless text is entered.

- **URL:** https://github.com/flutter/flutter/issues/90058
- **Created:** 2021-09-14 (~4.6 y old) · **Updated:** 2025-08-13
- **Reactions:** 6 (👍 6)
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.5`, `found in release: 2.6`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **likely-duplicate**

**Root cause.** Trailing spaces are not rendered when `textAlign` is `TextAlign.right`. This is the exact same underlying Skia issue as #40648.

**Dedup scan.**
  - **Terms / scope:** "textAlign", "TextAlign.right", "whitespace doesn't show"
  - **Hits, classified:** 
    - **duplicate:** #40648
  - **Cluster decision:** join `TRL-SPC-1`



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

**Root cause.** On Desktop platforms, pasting text with `
` leaves an invisible `
` character. The engine/Skia renders it as a zero-width space, causing the cursor to "stick" or require two arrow presses to cross the line ending.

**Why skip-engine.** While the framework handles the text string, the core issue is the low-level rendering logic making `
` zero-width but still physically present in the layout nodes. This requires engine/embedder fixes.

**Dedup scan.**
  - **Terms / scope:** "CRLF", "CR char", "invisible", "\r"
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



### #84317 — Share code between RenderParagraph and RenderEditable

- **URL:** https://github.com/flutter/flutter/issues/84317
- **Created:** 2021-06-10 (~4.9 y old) · **Updated:** 2023-07-08
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `a: typography`, `P2`, `c: tech-debt`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** A tech-debt proposal to share underlying logic between `RenderParagraph` and `RenderEditable`.

**Why skip-proposal.** This is a refactoring/architecture proposal without a specific user-facing bug regression surface.

**Dedup scan.**
  - **Terms / scope:** "Share code", "RenderParagraph", "RenderEditable"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #86668 — TextField doesn't handle trailing space as characters if textAlign is TextAlign.right/TextAlign.center

- **URL:** https://github.com/flutter/flutter/issues/86668
- **Created:** 2021-07-19 (~4.8 y old) · **Updated:** 2024-09-26
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.2`, `found in release: 2.4`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **likely-duplicate**

**Root cause.** Trailing spaces fail to render/align when `textAlign` is not `left`. This is exactly the same Skia rendering issue as #40648 and #90058.

**Dedup scan.**
  - **Terms / scope:** "textAlign", "trailing space"
  - **Hits, classified:** 
    - **duplicate:** #40648, #90058
  - **Cluster decision:** join `TRL-SPC-1`

### #103705 — letterSpacing in TextField with monospace font is only applied to right side of the first character

- **URL:** https://github.com/flutter/flutter/issues/103705
- **Created:** 2022-05-13 (~3.9 y old) · **Updated:** 2023-07-08
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `engine`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.0`, `found in release: 3.1`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — engine-level**

**Root cause.** Bug in how the engine handles letterSpacing bounds during string mutation. Was tracked and patched in Skia (skia-review.googlesource.com/c/skia/+/541978).

**Why skip-engine.** Issue is deep within Skia's typography measuring phase; the fix was merged upstream.

**Dedup scan.**
  - **Terms / scope:** "letterSpacing", "monospace", "first character"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #133930 — No good way to get line metrics for `Text`/`TextField` based widgets.

- **URL:** https://github.com/flutter/flutter/issues/133930
- **Created:** 2023-09-03 (~2.6 y old) · **Updated:** 2024-08-23
- **Reactions:** 1 (👍 1)
- **Labels:** `framework`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.13`, `found in release: 3.14`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Feature request for an `onTextLayoutChanged` or similar callback to reliably retrieve line metrics directly from the framework's widgets rather than rebuilding them in a dummy `TextPainter`.

**Why skip-proposal.** Proposal for a new framework API.

**Dedup scan.**
  - **Terms / scope:** "line metrics", "TextPainter"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #174689 — App highlights / selects trailing whitespaces in a multi-line textfield.

- **URL:** https://github.com/flutter/flutter/issues/174689
- **Created:** 2025-08-29 (~0.7 y old) · **Updated:** 2025-09-18
- **Reactions:** 1 (👀 1)
- **Labels:** `a: text input`, `platform-android`, `platform-ios`, `a: desktop`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.35`, `found in release: 3.36`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Selecting text on a line highlights trailing whitespace if the line below it is longer. This differs from native Android/iOS behavior. 

**Why skip-engine.** This is caused by `getRectsForRange` provided by the Skia text engine (which paints selection boxes). The framework uses the rects given to it.

**Dedup scan.**
  - **Terms / scope:** "highlights", "trailing whitespaces", "multi-line"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #184240 — Vertical baseline alignment mismatch between Text and collapsed TextField when changing TextLeadingDistribution

- **URL:** https://github.com/flutter/flutter/issues/184240
- **Created:** 2026-03-27 (~0.1 y old) · **Updated:** 2026-04-02
- **Reactions:** 1 (❤️ 1)
- **Labels:** `framework`, `f: material design`, `has reproducible steps`, `team-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **write-test** [→ **pass-green, exercises bug path**]

**Root cause.** Alleged baseline mismatch when `TextLeadingDistribution.even` is used alongside `InputDecoration.collapsed()`.

**Test approach.** 
  - Render a `Row` with `crossAxisAlignment: CrossAxisAlignment.baseline`.
  - Place a `Text` and an `Expanded(TextField)` inside it.
  - Compare the global Y offset of their RenderBoxes.

**Test:** [`issue_184240_baseline_alignment_test.dart`](../../regression_tests/internationalization_bidi_and_text_layout_v3/issue_184240_baseline_alignment_test.dart)

**Test outcome.** 
  - `pass-green, exercises bug path`. The difference is within 1 pixel, meaning the framework already aligns them successfully on master.

**Dedup scan.**
  - **Terms / scope:** "Vertical baseline", "TextLeadingDistribution"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #13468 — TextSelection.isDirectional is not respected, make it do something useful eg: for Mac

- **URL:** https://github.com/flutter/flutter/issues/13468
- **Created:** 2017-12-09 (~8.4 y old) · **Updated:** 2024-05-09
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `framework`, `c: proposal`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Proposal to wire up the unused `TextSelection.isDirectional` flag to drive text editing shortcuts.

**Why skip-proposal.** The property is dormant/unused API design proposal.

**Dedup scan.**
  - **Terms / scope:** "isDirectional"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #33858 — Unicode input should be indicated.

- **URL:** https://github.com/flutter/flutter/issues/33858
- **Created:** 2019-06-04 (~6.9 y old) · **Updated:** 2024-12-13
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `platform-windows`, `platform-linux`, `a: desktop`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** A feature request to display an underlined 'u' in the text field when awaiting a Unicode hex entry via `Ctrl+Shift+U`.

**Why skip-proposal.** Feature request for IME visual indicators.

**Dedup scan.**
  - **Terms / scope:** "Unicode input", "Ctrl+Shift+U"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #38503 — TextField doesn't appear within a direction:Axis.vertical Wrap

- **URL:** https://github.com/flutter/flutter/issues/38503
- **Created:** 2019-08-14 (~6.7 y old) · **Updated:** 2024-12-11
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **write-test** [→ **fail-as-expected**]

**Root cause.** `Wrap` with `direction: Axis.vertical` fails to provide bounded width constraints to its children. `TextField` (and its `InputDecorator`) asserts that it must have a bounded width to lay itself out.

**Test approach.** 
  - Render a `TextField` inside a `Wrap(direction: Axis.vertical)`.

**Test:** [`issue_38503_vertical_wrap_test.dart`](../../regression_tests/internationalization_bidi_and_text_layout_v3/issue_38503_vertical_wrap_test.dart)

**Test outcome.** 
  - `fail-as-expected`. The test catches the `AssertionError` ("An InputDecorator... cannot have an unbounded width") and fails, accurately reproducing the crash.

**Dedup scan.**
  - **Terms / scope:** "Axis.vertical Wrap", "unbounded width"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #54998 — Directional navigation key binding defaults should be limited to those platforms that use it.

- **URL:** https://github.com/flutter/flutter/issues/54998
- **Created:** 2020-04-16 (~6.0 y old) · **Updated:** 2024-07-22
- **Reactions:** 0 ()
- **Labels:** `framework`, `platform-macos`, `a: desktop`, `a: devtools`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Proposal to change the default behavior of directional focus key bindings on macOS and Linux.

**Why skip-proposal.** Requests changes to default shortcuts and `Intent` configurations rather than reporting a bug.

**Dedup scan.**
  - **Terms / scope:** "navigation key binding"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none



### #75572 — Let RenderEditable use LineMetrics instead of assuming every line has the same height

- **URL:** https://github.com/flutter/flutter/issues/75572
- **Created:** 2021-02-07 (~5.2 y old) · **Updated:** 2026-03-05
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `framework`, `f: material design`, `P2`, `c: tech-debt`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal**

**Root cause.** Tech-debt ticket to remove hardcoded line height assumptions in RenderEditable and instead query LineMetrics.

**Why skip-proposal.** This is an architectural tech-debt tracker.

**Dedup scan.**
  - **Terms / scope:** "RenderEditable", "LineMetrics", "same height"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #87536 — BIDI text painting skipped tests.

- **URL:** https://github.com/flutter/flutter/issues/87536
- **Created:** 2021-08-03 (~4.7 y old) · **Updated:** 2023-07-08
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `c: contributor-productivity`, `framework`, `a: internationalization`, `P2`, `c: tech-debt`, `team: skip-test`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** A tracker to review and un-skip tests in `text_painter_rtl_test.dart`.

**Why skip-proposal.** Tracking issue for skipped tests.

**Dedup scan.**
  - **Terms / scope:** "skipped tests", "BIDI text painting"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #92507 — Document "ghost run" and its interaction with `Paragraph.getBoxesForRange`

- **URL:** https://github.com/flutter/flutter/issues/92507
- **Created:** 2021-10-26 (~4.5 y old) · **Updated:** 2023-08-04
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `engine`, `d: api docs`, `a: typography`, `P2`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — feature/proposal**

**Root cause.** Missing API documentation for Skia's concept of a "ghost run" in text layout metrics.

**Why skip-proposal.** Documentation request for engine behavior.

**Dedup scan.**
  - **Terms / scope:** "ghost run", "getBoxesForRange"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #99139 — [MacOS] Trailing whitespace in multiline TextField overflows and doesn't go to newline.

- **URL:** https://github.com/flutter/flutter/issues/99139
- **Created:** 2022-02-25 (~4.2 y old) · **Updated:** 2024-06-20
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.10`, `found in release: 2.11`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** On Desktop platforms, Skia text layout does not automatically wrap trailing whitespaces in multiline fields to a new line, matching some native desktop behavior but frustrating code-editor developers.

**Why skip-engine.** This text wrapping and boundary behavior is controlled by the engine's text layout implementation. 

**Dedup scan.**
  - **Terms / scope:** "Trailing whitespace", "multiline TextField", "MacOS"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #110470 — canvas.drawLine() does not paint correctly on Samsung Galaxy Note 20 Ultra

- **URL:** https://github.com/flutter/flutter/issues/110470
- **Created:** 2022-08-29 (~3.6 y old) · **Updated:** 2024-09-26
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `e: device-specific`, `platform-android`, `framework`, `engine`, `f: material design`, `dependency: skia`, `c: rendering`, `P2`, `e: samsung`, `team-android`, `triaged-android`
- **Ownership:** `team-android`
- **Decision:** **skip — engine-level**

**Root cause.** Device-specific Skia rendering defect for `drawLine` on older Samsung hardware.

**Why skip-engine.** Engine/Skia GPU rendering issue.

**Dedup scan.**
  - **Terms / scope:** "drawLine()", "Samsung"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #113228 — Provide an API to detect if a TextPosition is located at a soft word wrap

- **URL:** https://github.com/flutter/flutter/issues/113228
- **Created:** 2022-10-10 (~3.5 y old) · **Updated:** 2024-03-06
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `c: new feature`, `platform-ios`, `framework`, `c: proposal`, `P3`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal**

**Root cause.** Request for a new `RenderEditable` API to detect if a text position is at a soft wrap boundary, to control iOS toolbar toggling.

**Why skip-proposal.** Feature/API request.

**Dedup scan.**
  - **Terms / scope:** "soft word wrap", "TextPosition"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #119684 — Extending to paragraph/or word boundary on MacOS should default to the `downstream` position when at a word wrap

- **URL:** https://github.com/flutter/flutter/issues/119684
- **Created:** 2023-02-01 (~3.2 y old) · **Updated:** 2024-06-06
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `framework`, `platform-macos`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** macOS text selection shortcuts (shift+option+up/down) need to default to a downstream affinity when crossing a soft word wrap boundary.

**Why skip-proposal.** This relates to default text selection intent logic for macOS shortcuts, closer to a feature request / behavioral tweak than a testable regression without engine layout metrics.

**Dedup scan.**
  - **Terms / scope:** "downstream", "word wrap", "extend selection"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #139443 — [Windows] Incorrect character deletion in right-to-left texts

- **URL:** https://github.com/flutter/flutter/issues/139443
- **Created:** 2023-12-03 (~2.4 y old) · **Updated:** 2025-08-21
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `platform-windows`, `has reproducible steps`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **write-test** [→ **fail-as-expected**]

**Root cause.** On Windows, manual typing generates CRLF line endings instead of LF. The framework's text selection endpoints return the incorrect visual offset for RTL text containing CRLF boundaries, causing backspace to delete the wrong visual character.

**Test approach.** 
  - Extract the visual X-offset of a collapsed text selection just after a CRLF (`\r\n`) in an RTL string.
  - Compare it to the visual X-offset of the same string using just LF (`\n`).
  - Assert they are equal.

**Test:** [`issue_139443_crlf_rtl_test.dart`](../../regression_tests/internationalization_bidi_and_text_layout_v3/issue_139443_crlf_rtl_test.dart)

**Test outcome.** 
  - `fail-as-expected`. Expected `<747.0>`, actual `<795.0>`. The visual carets diverge because the framework misinterprets the `\r` length during layout in an RTL context.

**Dedup scan.**
  - **Terms / scope:** "deletion in right-to-left", "CRLF", "Windows RTL backspace"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #144759 — Arrow key navigation gets stuck at the end of RTL text using Samsung Keyboard

- **URL:** https://github.com/flutter/flutter/issues/144759
- **Created:** 2024-03-07 (~2.1 y old) · **Updated:** 2024-03-07
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — needs native-platform verification**

**Root cause.** Samsung Keyboard IME on Android ignores the left-arrow key if the cursor is at the visual left edge of the text field. However, Flutter traverses RTL text logically (where the logical start is at the visual right), meaning the framework waits for a key event it never receives.

**Why skip-native.** The core problem relies on the native IME (Samsung Keyboard specifically) consuming/ignoring arrow key inputs before they hit the Flutter engine. Simulating this requires an Android integration test with that specific OEM keyboard.

**Dedup scan.**
  - **Terms / scope:** "Arrow key navigation", "Samsung Keyboard", "stuck at the end"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #155919 — Error where possible null is being asserted in rendering paragraph

- **URL:** https://github.com/flutter/flutter/issues/155919
- **Created:** 2024-09-30 (~1.6 y old) · **Updated:** 2024-10-23
- **Reactions:** 0 ()
- **Labels:** `framework`, `a: error message`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **write-test** [→ **pass-green, exercises bug path**]

**Root cause.** Pumping a `Text` widget inside an un-expanded `Row` child that is forcibly squished to zero width (`BoxConstraints` 0) previously caused a null assertion in `RenderParagraph`.

**Test approach.** 
  - Render a `SizedBox(width: 0)` containing a `Row` with one `Expanded(child: Text())` and one unexpanded `Text()`.
  - Assert that no framework exceptions are thrown.

**Test:** [`issue_155919_squished_text_test.dart`](../../regression_tests/internationalization_bidi_and_text_layout_v3/issue_155919_squished_text_test.dart)

**Test outcome.** 
  - `pass-green, exercises bug path`. The test completes successfully without throwing an assertion. Likely fixed in an intervening layout patch.

**Dedup scan.**
  - **Terms / scope:** "null is being asserted", "rendering paragraph", "width 0"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none



### #165204 — Unicode characters not being rendered correctly in goldens test

- **URL:** https://github.com/flutter/flutter/issues/165204
- **Created:** 2025-03-14 (~0.1 y old) · **Updated:** 2025-03-27
- **Reactions:** 0 ()
- **Labels:** `a: tests`, `a: text input`, `framework`, `has reproducible steps`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** The `Ahem` font used by default in `matchesGoldenFile` does not include the `U+25CF` bullet character, rendering it as a tofu box.

**Why skip-proposal.** This is the expected behavior of the `Ahem` test font. Developers must explicitly load a font that supports the character if they want to render it in golden tests.

**Dedup scan.**
  - **Terms / scope:** "goldens test", "Unicode characters", "Ahem"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #167466 — Ellipsis not working properly when a text overflows via constrained height instead of max lines

- **URL:** https://github.com/flutter/flutter/issues/167466
- **Created:** 2025-04-21 (~0.0 y old) · **Updated:** 2025-12-21
- **Reactions:** 0 ()
- **Labels:** `framework`, `a: typography`, `c: rendering`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Ellipsis is triggered by `maxLines` or maximum width constraints within `TextPainter`. If the text overflows because the parent `Container`'s height is constrained, `TextPainter` does not know to insert an ellipsis because the layout algorithm processes line-by-line width, not aggregate height bounds.

**Why skip-engine.** Modifying `TextPainter` or the underlying `SkParagraph` layout algorithm to support truncation by block height is an engine-level feature request / text-layout architectural change.

**Dedup scan.**
  - **Terms / scope:** "Ellipsis", "constrained height", "overflows"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #177408 — The framework should provide a mechanism to change the paragraph spacing of text

- **URL:** https://github.com/flutter/flutter/issues/177408
- **Created:** 2025-10-22 (~0.5 y old) · **Updated:** 2026-01-06
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `c: new feature`, `a: accessibility`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Request to add `paragraphSpacing` to `TextStyle` to control the space between paragraphs separated by `\n`.

**Why skip-proposal.** Feature proposal for text styling.

**Dedup scan.**
  - **Terms / scope:** "paragraph spacing", "paragraphSpacing"
  - **Hits, classified:** 
    - **adjacent-different:** #36854 (Setting paragraph distance in Text and TextField). Very similar proposal, but distinct issues tracking the same request.
  - **Cluster decision:** none

### #177953 — The framework should apply `paragraphSpacingOverride` to its text

- **URL:** https://github.com/flutter/flutter/issues/177953
- **Created:** 2025-11-03 (~0.4 y old) · **Updated:** 2026-01-02
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `c: new feature`, `a: accessibility`, `platform-web`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Request to apply the existing `MediaQueryData.paragraphSpacingOverride` to the framework's internal text components to meet WCAG standards out of the box.

**Why skip-proposal.** Feature parity / accessibility integration request.

**Dedup scan.**
  - **Terms / scope:** "paragraphSpacingOverride", "WCAG"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #183571 — iOS: NSJSONSerialization crash when deleting SMP characters

- **URL:** https://github.com/flutter/flutter/issues/183571
- **Created:** 2026-03-12 (~0.1 y old) · **Updated:** 2026-03-19
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `platform-ios`, `P1`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Deleting Supplementary Multilingual Plane (SMP) characters on iOS leaves orphaned UTF-16 surrogates, causing `NSJSONSerialization` to crash the app via `FlutterCodecs.mm`.

**Why skip-engine.** This is an embedder/engine crash in the iOS `FlutterCodecs.mm` layer when communicating with the framework.

**Dedup scan.**
  - **Terms / scope:** "NSJSONSerialization crash", "SMP characters", "UTF-16 surrogates"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none


## Duplicate clusters

- **TRL-SPC-1** Trailing space trimmed on TextAlign.right (3 members)
  - Canonical: #40648
  - Members: #90058, #86668

## Likely-stale candidates for closure review
- #155919 — Squished `Text` widget null assertion passes without error on master.
- #184240 — `TextLeadingDistribution.even` baseline alignment test passes on master.

- #41324 — `labelText` alignment passes green framework regression test; highly likely fixed in recent `InputDecoration` refactors.

## Cross-category sibling / split-issue links

## Skipped — engine-level
- #167466 — TextPainter layout ellipsis by height constraint limits
- #183571 — iOS embedder NSJSONSerialization surrogate pair crash
- #99139 — Skia macOS text layout trailing whitespace line break differences
- #110470 — Device-specific Skia drawLine defect on Samsung
- #103705 — Skia letterSpacing bounds issue (fixed upstream)
- #174689 — Skia getRectsForRange highlights trailing spaces
- #71083 — Skia/LibTxt word-breaking constraints
- #93934 — Skia zero-width rendering of pasted \r
- #117139 — SkParagraph getRectsForRange newline bug
- #181759 — macOS/Linux embedder text-input crash (wstring_convert)
- #78864 — SkParagraph BiDi rendering of weak boundaries

- #77023 — CanvasKit font loading delay
- #34610 — Mixed LTR/RTL SkParagraph directionality
- #40648 — Skia trailing space trim on TextAlign.right
- #39755 — LibTxt justification x-offset missing for non-Latin
