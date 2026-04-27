# Internationalization, BiDi, and text layout Cleanup Report (v3)

This report covers the "Internationalization, BiDi, and text layout" category from the `2026-04-17` snapshot.
Workflow per [`CLEANUP_REPORT_FORMAT.md`](../CLEANUP_REPORT_FORMAT.md).
Note: This is a v3 audit, run independently from previous reports.

## Running summary

- Processed: 9 / 44
- Tests written: 1
  - Failed as expected: 1
  - Pass-green, exercises bug path: 0
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


## Duplicate clusters

- **TRL-SPC-1** Trailing space trimmed on TextAlign.right (2 members)
  - Canonical: #40648
  - Members: #90058

## Likely-stale candidates for closure review

## Cross-category sibling / split-issue links

## Skipped — engine-level

- #77023 — CanvasKit font loading delay
- #34610 — Mixed LTR/RTL SkParagraph directionality
- #40648 — Skia trailing space trim on TextAlign.right
- #39755 — LibTxt justification x-offset missing for non-Latin
