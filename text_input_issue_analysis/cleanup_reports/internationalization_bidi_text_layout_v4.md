# Internationalization, BiDi, and text layout Cleanup Report v4

Auditing the "Internationalization, BiDi, and text layout" category from the `2026-04-17` snapshot. Processed according to [`CLEANUP_REPORT_FORMAT.md`](CLEANUP_REPORT_FORMAT.md). Issues are processed in descending order of total reactions.

**Running summary**
- Processed: 44 / 44
- Tests written: 5
  - Failed as expected: 4
  - Pass-green, exercises bug path: 1
  - Pass-green, does not exercise bug path: 0
  - Test error: 0
- Skip — feature/proposal: 17
- Skip — engine-level: 19
- Skip — needs native-platform verification: 1
- Likely-duplicate: 2
- Duplicate clusters (tentative): 2 (TRS-1, PS-1)
- Cross-category sibling/split-issue links: 0

## Decision types
- `write-test`: Framework-level `testWidgets`/`test` feasible.
- `skip — feature/proposal`: `c: proposal` / `c: new feature`.
- `skip — engine-level`: Fix lives in engine/embedder.
- `skip — needs native-platform verification`: Framework-testable, but needs native reference.
- `likely-stale`: Age + inactivity suggest invalid.
- `likely-duplicate`: Same root cause as another in-category issue.

## Processed issues

### #61069 — [proposal] ability to change text overflow on the TextField

- **URL:** https://github.com/flutter/flutter/issues/61069
- **Created:** 2020-07-08 (~5.8 y old) · **Updated:** 2025-07-18
- **Reactions:** 65 (THUMBS_UP 65)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `c: proposal`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** User wants the ability to show an ellipsis when text overflows a single-line `TextFormField`, similar to the `Text` widget, instead of just cropping it.

**Why skip-proposal.** This is a feature request for API surface addition (`overflow` parameter on `TextFormField`).

**Dedup scan.** No obvious duplicates in this batch.


### #51258 — Need to find how much of a long word could fit in one line before an unnatural line break

- **URL:** https://github.com/flutter/flutter/issues/51258
- **Created:** 2020-02-22 (~6.2 y old) · **Updated:** 2023-07-08
- **Reactions:** 28 (THUMBS_UP 24, EYES 4)
- **Labels:** `a: text input`, `framework`, `a: typography`, `c: proposal`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** Users want an API to measure text and find word breaks for custom layout, particularly handling long unbroken strings and contextual shaping.

**Why skip-proposal.** The request is for exposing new layout/measurement APIs to Dart. 

**Dedup scan.** No duplicates in this batch.


### #77023 — [Web] [CanvasKit][Feature Request]: Load fonts as soon as detecting browser locale

- **URL:** https://github.com/flutter/flutter/issues/77023
- **Created:** 2021-03-02 (~5.1 y old) · **Updated:** 2025-10-30
- **Reactions:** 21 (THUMBS_UP 17, EYES 4)
- **Labels:** `a: text input`, `c: new feature`, `a: internationalization`, `a: typography`, `platform-web`, `c: proposal`, `c: rendering`, `e: web_canvaskit`, `P2`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level**

**Root cause.** CanvasKit engine dynamically loads CJK/RTL fonts when unknown characters are encountered, leading to temporary rendering of gibberish before the font loads.

**Why skip-engine.** This is a Web CanvasKit engine rendering/font loading behavior. No framework code path controls this dynamic font loading.

**Dedup scan.** No duplicates in this batch.


### #34610 — Mixing RTL and LTR text bugs

- **URL:** https://github.com/flutter/flutter/issues/34610
- **Created:** 2019-06-17 (~6.8 y old) · **Updated:** 2024-03-06
- **Reactions:** 18 (THUMBS_UP 14, ROCKET 1, EYES 3)
- **Labels:** `a: text input`, `framework`, `engine`, `a: typography`, `customer: crowd`, `P2`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — engine-level**

**Root cause.** Mixing RTL and LTR text causes strange deletion behavior, caret positioning issues, and emoji rendering bugs. Root cause identified in comments as SkParagraph text layout directionality bugs.

**Why skip-engine.** The bugs reside in Skia/SkParagraph text layout and shaping engine layers.

**Dedup scan.** No duplicates in this batch.


### #40648 — Trailing space doesn't work with TextField with TextAlign.right 

- **URL:** https://github.com/flutter/flutter/issues/40648
- **Created:** 2019-09-17 (~6.6 y old) · **Updated:** 2025-01-29
- **Reactions:** 16 (THUMBS_UP 16)
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.5`, `found in release: 2.6`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause.** Trailing spaces are visually trimmed and not rendered when `TextAlign.right` is used. This is an upstream Skia bug (bugs.chromium.org/p/skia/issues/detail?id=11933) where SkParagraph trims trailing whitespaces or treats `\r` weirdly.

**Why skip-engine.** Framework simply delegates to engine Paragraph rendering.

**Dedup scan.** Cluster **TRS-1** identified with #90058 (exact same issue).


### #78660 — Arrow keys in RTL move the wrong way

- **URL:** https://github.com/flutter/flutter/issues/78660
- **Created:** 2021-03-19 (~5.1 y old) · **Updated:** 2024-03-06
- **Reactions:** 15 (THUMBS_UP 15)
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 2.1`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **write-test** [→ **fail-as-expected**]

**Root cause.** Left and right arrow keys modify the selection logically (character index sequence) instead of visually (left/right screen direction), causing reversed movement in RTL text.

**Test approach.**
- Render a `TextField` with RTL text direction and Arabic text.
- Set the selection index to 0 (logical start, visual right).
- Simulate pressing the Left arrow key.
- Assert the selection index moves to 1 (visual left, logical forward).

**Test:** [`../regression_tests/internationalization_bidi_text_layout_v4/issue_78660_arrow_keys_in_rtl_test.dart`](../regression_tests/internationalization_bidi_text_layout_v4/issue_78660_arrow_keys_in_rtl_test.dart)

**Test outcome.** Test failed as expected (`Expected: <1> Actual: <0>`). The caret does not move visually.

**Dedup scan.** No duplicates in this batch.


### #36854 — Feature request: Setting paragraph distance in Text and TextField

- **URL:** https://github.com/flutter/flutter/issues/36854
- **Created:** 2019-07-24 (~6.7 y old) · **Updated:** 2024-03-06
- **Reactions:** 12 (THUMBS_UP 12)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `a: typography`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** User wants an API to control paragraph spacing inside text widgets.

**Why skip-proposal.** Clear feature request for new text layout properties.

**Dedup scan.** No duplicates in this batch.


### #39755 — Selection of any justified-text is inaccurate in non-latin languages

- **URL:** https://github.com/flutter/flutter/issues/39755
- **Created:** 2019-09-03 (~6.6 y old) · **Updated:** 2024-03-06
- **Reactions:** 10 (THUMBS_UP 9, EYES 1)
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause.** Selection highlight boxes do not accurately match text boundaries for justified Korean, Arabic, Hebrew, and Persian text.

**Why skip-engine.** The selection rects are computed directly by the text engine layout (SkParagraph) which returns the bounding boxes. Framework just paints what it's given.

**Dedup scan.** No duplicates in this batch.


### #90058 — TextFormField with textAlign: TextAlign.right whitespace doesn't show unless text is entered.

- **URL:** https://github.com/flutter/flutter/issues/90058
- **Created:** 2021-09-14 (~4.6 y old) · **Updated:** 2025-08-13
- **Reactions:** 6 (THUMBS_UP 6)
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.5`, `found in release: 2.6`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **likely-duplicate**

**Root cause.** Same as #40648. Trailing spaces are visually trimmed with `TextAlign.right`. 

**Dedup scan.** Exact duplicate of #40648. Grouping into cluster **TRS-1**.


### #71083 — TextFormField (and TextField) widgets do not wrap text correctly

- **URL:** https://github.com/flutter/flutter/issues/71083
- **Created:** 2020-11-23 (~5.4 y old) · **Updated:** 2024-03-06
- **Reactions:** 5 (THUMBS_UP 5)
- **Labels:** `a: text input`, `framework`, `f: material design`, `dependency: skia`, `a: typography`, `P2`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause.** Text wrapping logic breaks words incorrectly (at the boundary closest to end of line instead of middle of string) for long continuous strings like URLs.

**Why skip-engine.** Word breaking and line wrapping algorithms are implemented in SkParagraph/engine.

**Dedup scan.** No duplicates in this batch.



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

**Root cause.** Pasting text with CRLF (`\r\n`) endings causes the `\r` character to become an invisible, interactable character boundary that traps or skips caret movement differently on Desktop (Windows/macOS).

**Why skip-engine.** How SkParagraph handles `\r` and determines caret boundary stops at line breaks is an engine text layout issue. Framework just iterates `getWordBoundary` or uses `TextPosition` from the engine.

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


### #86668 — TextField doesn't handle trailing space as characters if textAlign is TextAlign.right/TextAlign.center

- **URL:** https://github.com/flutter/flutter/issues/86668
- **Created:** 2021-07-19 (~4.7 y old) · **Updated:** 2024-09-26
- **Reactions:** 1 (THUMBS_UP 1)
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.2`, `found in release: 2.4`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **likely-duplicate**

**Root cause.** Trailing spaces are not rendered and do not advance the caret/push text when `textAlign` is `TextAlign.center` or `TextAlign.right`.

**Dedup scan.** Exact duplicate of the root cause in #40648 (Skia `SkParagraph` trailing whitespace trimming behavior). Adding to cluster **TRS-1**.


### #103705 — letterSpacing in TextField with monospace font is only applied to right side of the first character until a second character is entered, then letterSpacing is applied correctly to both sides

- **URL:** https://github.com/flutter/flutter/issues/103705
- **Created:** 2022-05-13 (~3.9 y old) · **Updated:** 2023-07-08
- **Reactions:** 1 (THUMBS_UP 1)
- **Labels:** `a: text input`, `engine`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.0`, `found in release: 3.1`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — engine-level**

**Root cause.** Letter spacing was applied asymmetrically for single-character inputs. Confirmed as a Skia bug (https://skia-review.googlesource.com/c/skia/+/541978) which was merged upstream.

**Why skip-engine.** This is a resolved upstream Skia text layout bug.

**Dedup scan.** No duplicates in this batch.


### #133930 — No good way to get line metrics for `Text`/`TextField` based widgets.

- **URL:** https://github.com/flutter/flutter/issues/133930
- **Created:** 2023-09-03 (~2.6 y old) · **Updated:** 2024-08-23
- **Reactions:** 1 (THUMBS_UP 1)
- **Labels:** `framework`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.13`, `found in release: 3.14`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Developers struggle to obtain accurate line metrics because manually constructing a `TextPainter` often misses ambient theme styles applied internally by `TextField`.

**Why skip-proposal.** The request is effectively for a new framework-level API (like `onTextLayoutChanged`) to expose internal text metrics reliably.

**Dedup scan.** No duplicates in this batch.


### #174689 — App highlights / selects trailing whitespaces in a multi-line textfield.

- **URL:** https://github.com/flutter/flutter/issues/174689
- **Created:** 2025-08-29 (~0.6 y old) · **Updated:** 2025-09-18
- **Reactions:** 1 (EYES 1)
- **Labels:** `a: text input`, `platform-android`, `platform-ios`, `a: desktop`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.35`, `found in release: 3.36`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** The selection highlight boxes incorrectly extend to include trailing whitespaces in multiline text fields, unlike native platform behaviors.

**Why skip-engine.** The selection rects are computed and returned by `Paragraph.getBoxesForRange()`, which delegates to SkParagraph text layout.

**Dedup scan.** No duplicates in this batch.


### #184240 — Vertical baseline alignment mismatch between Text and collapsed TextField when changing TextLeadingDistribution

- **URL:** https://github.com/flutter/flutter/issues/184240
- **Created:** 2026-03-27 (~0.1 y old) · **Updated:** 2026-04-02
- **Reactions:** 1 (HEART 1)
- **Labels:** `framework`, `f: material design`, `has reproducible steps`, `team-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **write-test** [→ **fail-as-expected**]

**Root cause.** A `TextField` with `InputDecoration.collapsed` does not vertically align its baseline with a plain `Text` widget when `TextLeadingDistribution.proportional` is used.

**Test approach.**
- Render a `Row` with `crossAxisAlignment: CrossAxisAlignment.baseline`.
- Add a `Text` widget and a `TextField` (with `InputDecoration.collapsed`), both using the same proportional leading style.
- Assert their top Y-coordinates match.

**Test:** [`../regression_tests/internationalization_bidi_text_layout_v4/issue_184240_baseline_alignment_test.dart`](../regression_tests/internationalization_bidi_text_layout_v4/issue_184240_baseline_alignment_test.dart)

**Test outcome.** Test failed as expected (`Expected: a numeric value within <2.0> of <2.625> Actual: <0.0>`). The text field is incorrectly aligned compared to the text widget.

**Dedup scan.** No duplicates in this batch.


### #13468 — TextSelection.isDirectional is not respected, make it do something useful eg: for Mac

- **URL:** https://github.com/flutter/flutter/issues/13468
- **Created:** 2017-12-09 (~8.4 y old) · **Updated:** 2024-05-09
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `c: proposal`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** The `isDirectional` property on `TextSelection` exists but isn't wired up to control directional navigation behaviors as intended.

**Why skip-proposal.** This is a tech-debt/cleanup proposal to either wire up or remove the unused property.

**Dedup scan.** No duplicates in this batch.


### #33858 — Unicode input should be indicated.

- **URL:** https://github.com/flutter/flutter/issues/33858
- **Created:** 2019-06-04 (~6.9 y old) · **Updated:** 2024-12-13
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `platform-windows`, `platform-linux`, `a: desktop`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** The standard `Ctrl+Shift+U` Unicode input sequence (especially on Linux) accepts input but does not display the expected underlined "u" indicator.

**Why skip-engine.** Handling of platform-specific raw key events for Unicode entry and passing the appropriate composing state to the framework is the responsibility of the embedder's text input plugin (e.g., Linux GTK input method context).

**Dedup scan.** No duplicates in this batch.


### #38503 — TextField doesn't appear within a direction:Axis.vertical Wrap

- **URL:** https://github.com/flutter/flutter/issues/38503
- **Created:** 2019-08-14 (~6.7 y old) · **Updated:** 2024-12-11
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **write-test** [→ **fail-as-expected**]

**Root cause.** Placing a `TextField` directly inside a `Wrap` with `direction: Axis.vertical` throws a layout assertion error because `InputDecorator` requires a bounded width, which `Wrap` does not provide in the cross-axis.

**Test approach.**
- Render a `Wrap` with `direction: Axis.vertical` containing a `TextField`.
- Assert that `tester.takeException()` is null (i.e., no layout exception is thrown).

**Test:** [`../regression_tests/internationalization_bidi_text_layout_v4/issue_38503_vertical_wrap_test.dart`](../regression_tests/internationalization_bidi_text_layout_v4/issue_38503_vertical_wrap_test.dart)

**Test outcome.** Test failed as expected (`Expected: null Actual: 'Multiple exceptions (11) were detected...'`). The `InputDecorator` layout constraint assertion is thrown.

**Dedup scan.** No duplicates in this batch.


### #54998 — Directional navigation key binding defaults should be limited to those platforms that use it.

- **URL:** https://github.com/flutter/flutter/issues/54998
- **Created:** 2020-04-16 (~6.0 y old) · **Updated:** 2024-07-22
- **Reactions:** 0
- **Labels:** `framework`, `platform-macos`, `a: desktop`, `a: devtools`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Default directional focus key bindings (up/down arrow keys) interfere with custom widget navigation on macOS because they are enabled globally rather than per-widget.

**Why skip-proposal.** The issue is a request to change the default framework-level shortcut bindings for macOS.

**Dedup scan.** No duplicates in this batch.


### #75572 — Let RenderEditable use LineMetrics instead of assuming every line has the same height

- **URL:** https://github.com/flutter/flutter/issues/75572
- **Created:** 2021-02-07 (~5.2 y old) · **Updated:** 2026-03-05
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `f: material design`, `P2`, `c: tech-debt`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal**

**Root cause.** `RenderEditable` currently calculates vertical key movements assuming uniform line heights, causing the caret to jump incorrectly when lines have different heights.

**Why skip-proposal.** This is marked as `c: tech-debt`. It requests an architectural refactor of `RenderEditable` to use `LineMetrics` for vertical movement calculations instead of simpler approximations.

**Dedup scan.** No duplicates in this batch.


### #87536 — BIDI text painting skipped tests.

- **URL:** https://github.com/flutter/flutter/issues/87536
- **Created:** 2021-08-03 (~4.7 y old) · **Updated:** 2023-07-08
- **Reactions:** 0
- **Labels:** `a: text input`, `c: contributor-productivity`, `framework`, `a: internationalization`, `P2`, `c: tech-debt`, `team: skip-test`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** This is a tracking bug for several RTL text painting tests that were skipped in `text_painter_rtl_test.dart` and need to be investigated or turned back on.

**Why skip-proposal.** Marked as `c: tech-debt`; it is an internal test suite cleanup tracking issue, not a specific bug to reproduce.

**Dedup scan.** No duplicates in this batch.


### #92507 — Document "ghost run" and its interaction with `Paragraph.getBoxesForRange`

- **URL:** https://github.com/flutter/flutter/issues/92507
- **Created:** 2021-10-26 (~4.5 y old) · **Updated:** 2023-08-04
- **Reactions:** 0
- **Labels:** `a: text input`, `engine`, `d: api docs`, `a: typography`, `P2`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — feature/proposal**

**Root cause.** Documentation gap regarding SkParagraph "ghost runs" (e.g., trailing whitespace) and how `getRectsForRange` can return boxes outside the paragraph's bounding box.

**Why skip-proposal.** The request is for API documentation updates (`d: api docs`), not code changes.

**Dedup scan.** No duplicates in this batch.


### #99139 — [MacOS] Trailing whitespace in multiline TextField overflows and doesn't go to newline.

- **URL:** https://github.com/flutter/flutter/issues/99139
- **Created:** 2022-02-25 (~4.1 y old) · **Updated:** 2024-06-20
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.10`, `found in release: 2.11`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Trailing whitespace in a multiline `TextField` on macOS does not trigger a line wrap visually, allowing the caret/selection to overflow the widget's bounds, unlike native macOS editors.

**Why skip-engine.** Text wrapping and trailing whitespace ("ghost run") layout logic is implemented in SkParagraph in the engine.

**Dedup scan.** No duplicates in this batch.


### #110470 — canvas.drawLine() does not paint correctly on Samsung Galaxy Note 20 Ultra

- **URL:** https://github.com/flutter/flutter/issues/110470
- **Created:** 2022-08-29 (~3.6 y old) · **Updated:** 2024-09-26
- **Reactions:** 0
- **Labels:** `a: text input`, `e: device-specific`, `platform-android`, `framework`, `engine`, `f: material design`, `dependency: skia`, `c: rendering`, `P2`, `e: samsung`, `team-android`, `triaged-android`, `found in release: 3.19`
- **Ownership:** `team-android`
- **Decision:** **skip — engine-level**

**Root cause.** `canvas.drawLine()` produces visual artifacts/incorrect rendering specifically on older Samsung hardware (e.g. GT-I9500).

**Why skip-engine.** This is a device-specific hardware/Skia rendering defect.

**Dedup scan.** No duplicates in this batch.


### #113228 — Provide an API to detect if a TextPosition is located at a soft word wrap

- **URL:** https://github.com/flutter/flutter/issues/113228
- **Created:** 2022-10-10 (~3.5 y old) · **Updated:** 2024-03-06
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `platform-ios`, `framework`, `c: proposal`, `P3`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal**

**Root cause.** There is no API in `RenderEditable` to detect if a `TextPosition` is exactly at a soft word wrap, which is needed to mimic native iOS toolbar toggling behavior.

**Why skip-proposal.** This is a feature request for a new API surface.

**Dedup scan.** No duplicates in this batch.


### #119684 — Extending to paragraph/or word boundary on MacOS should default to the `downstream` position when at a word wrap

- **URL:** https://github.com/flutter/flutter/issues/119684
- **Created:** 2023-02-01 (~3.2 y old) · **Updated:** 2024-06-06
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `platform-macos`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — needs native-platform verification**

**Root cause.** When using macOS keyboard shortcuts (`shift + option + arrow`) to extend selection, if the caret is at a word wrap, returning to the original position inherits affinity rather than defaulting to `downstream` as native macOS does.

**Why skip — needs native-platform verification.** The issue requests matching a specific macOS native selection behavior (downstream affinity at word wraps) that requires verification against current native macOS NSTextView behavior.

**Dedup scan.** No duplicates in this batch.


### #139443 — [Windows] Incorrect character deletion in right-to-left texts

- **URL:** https://github.com/flutter/flutter/issues/139443
- **Created:** 2023-12-03 (~2.4 y old) · **Updated:** 2025-08-21
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `platform-windows`, `has reproducible steps`, `P3`, `found in release: 3.16`, `found in release: 3.18`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** When manually typing RTL text with `CRLF` endings on Windows, the caret offset reported by the framework is incorrect, causing Backspace to delete the wrong character.

**Why skip-engine.** SkParagraph's handling of `CRLF` vs `LF` and how it calculates caret boundaries and string offsets for RTL text is an engine layout layer responsibility.

**Dedup scan.** No duplicates in this batch.


### #144759 — Arrow key navigation gets stuck at the end of RTL text using Samsung Keyboard

- **URL:** https://github.com/flutter/flutter/issues/144759
- **Created:** 2024-03-07 (~2.1 y old) · **Updated:** 2024-03-07
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 3.19`, `team-text-input`, `triaged-text-input`, `found in release: 3.21`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Flutter uses logical order for arrow key navigation, while the Samsung keyboard assumes visual order. When at the visual end of RTL text, the Samsung keyboard ignores the left-arrow key, trapping the caret.

**Why skip-engine.** The translation of logical to visual cursor traversal, and interaction with specific platform IME behaviors (Samsung keyboard), involves engine/embedder key event synthesis. Supporting visual order traversal is a major missing architectural piece.

**Dedup scan.** No duplicates in this batch.


### #155919 — Error where possible null is being asserted in rendering paragraph

- **URL:** https://github.com/flutter/flutter/issues/155919
- **Created:** 2024-09-30 (~1.6 y old) · **Updated:** 2024-10-23
- **Reactions:** 0
- **Labels:** `framework`, `a: error message`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **write-test** [→ **pass-green, exercises bug path**]

**Root cause.** A null assertion fires in `RenderParagraph` during `debugDescribeChildren` or JSON serialization when the widget is constrained to a 0 width (e.g. inside an `Expanded` in a `Row` with 0 width).

**Test approach.**
- Render a `Text` widget inside an `Expanded` inside a `Row` constrained to `SizedBox(width: 0)`.
- Extract the `RenderBox` for the `Text` and call `debugDescribeChildren()`.
- Verify it returns normally without throwing.

**Test:** [`../regression_tests/internationalization_bidi_text_layout_v4/issue_155919_0_width_text_diagnostics_test.dart`](../regression_tests/internationalization_bidi_text_layout_v4/issue_155919_0_width_text_diagnostics_test.dart)

**Test outcome.** Test passed green (`All tests passed!`). This indicates the specific crash path described has either been fixed in master or the test setup avoids the null state. Tagging for closure review.

**Dedup scan.** No duplicates in this batch.


### #165204 — Unicode characters not being rendered correctly in goldens test

- **URL:** https://github.com/flutter/flutter/issues/165204
- **Created:** 2025-03-14 (~1.1 y old) · **Updated:** 2025-03-27
- **Reactions:** 0
- **Labels:** `a: tests`, `a: text input`, `framework`, `has reproducible steps`, `P3`, `team-text-input`, `triaged-text-input`, `found in release: 3.29`, `found in release: 3.31`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** The Ahem font, used by default in `flutter_test` golden tests, lacks the bullet character (`\u25CF`), causing it to render as a tofu box.

**Why skip-proposal.** The request is to either update the Ahem font or improve test framework default font loading to handle common Unicode obscuring characters, which is a test framework enhancement request.

**Dedup scan.** No duplicates in this batch.


### #167466 — Ellipsis not working properly when a text overflows via constrained height instead of max lines

- **URL:** https://github.com/flutter/flutter/issues/167466
- **Created:** 2025-04-21 (~1.0 y old) · **Updated:** 2025-12-21
- **Reactions:** 0
- **Labels:** `framework`, `a: typography`, `c: rendering`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.29`, `found in release: 3.32`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Text truncation via `TextOverflow.ellipsis` fails to render the ellipsis when the text is visually clipped by its parent's height constraints rather than a specified `maxLines`.

**Why skip-engine.** Ellipsis insertion based on layout constraints is managed internally by SkParagraph during layout calculation.

**Dedup scan.** No duplicates in this batch.


### #177408 — The framework should provide a mechanism to change the paragraph spacing of text

- **URL:** https://github.com/flutter/flutter/issues/177408
- **Created:** 2025-10-22 (~0.5 y old) · **Updated:** 2026-01-06
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `a: accessibility`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Request to add a `paragraphSpacing` property to `TextStyle` to control space between `\n` separated paragraphs, driven by WCAG accessibility requirements.

**Why skip-proposal.** This is a feature request for new `TextStyle` rendering APIs.

**Dedup scan.** Found cluster members #36854 (oldest request for the same API) and #177953 (request to use a global override). Recorded as cluster **PS-1**.


### #177953 — The framework should apply `paragraphSpacingOverride` to its text

- **URL:** https://github.com/flutter/flutter/issues/177953
- **Created:** 2025-11-03 (~0.5 y old) · **Updated:** 2026-01-02
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `a: accessibility`, `platform-web`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Follow-up to PR #172915. Asks the framework's widgets to automatically consume the `MediaQueryData.paragraphSpacingOverride` to meet WCAG standards out of the box.

**Why skip-proposal.** A proposal for new behavior in existing widgets, fundamentally blocked by the missing `TextStyle` property described in #177408.

**Dedup scan.** Clustered under **PS-1** alongside #177408 and #36854.


### #183571 — iOS: NSJSONSerialization crash when deleting SMP characters

- **URL:** https://github.com/flutter/flutter/issues/183571
- **Created:** 2026-03-12 (~0.1 y old) · **Updated:** 2026-03-19
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-ios`, `P1`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Deleting SMP characters (surrogate pairs) on iOS can leave orphaned UTF-16 surrogates in the string state, causing a C++ `NSJSONSerialization` crash during platform channel messaging. 

**Why skip-engine.** The bug lives in `FlutterCodecs.mm` and `UITextInput` string manipulation at the iOS embedder layer.

**Dedup scan.** No duplicates in this batch.

## Duplicate clusters
- **PS-1** (Paragraph Spacing API). Canonical: #36854. Members: #177408, #177953. Proposals to add paragraph spacing controls to `TextStyle` and apply them via MediaQuery.
- **TRS-1** (Trailing Right Space Trimmed). Canonical: #40648. Members: #90058, #86668. Upstream Skia bug causes trailing spaces to be visually omitted when `TextAlign.right` (or center) is set.

## Likely-stale candidates for closure review
- **#155919** — Test `issue_155919_0_width_text_diagnostics_test.dart` passes green, suggesting the null assertion in `RenderParagraph` diagnostics is fixed.

## Cross-category sibling / split-issue links
(None yet)
