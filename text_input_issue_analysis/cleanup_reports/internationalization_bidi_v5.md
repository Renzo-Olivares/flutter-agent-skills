# Internationalization, BiDi, and text layout Cleanup Report

This report audits the "Internationalization, BiDi, and text layout" category from the `text_input_issues.json` snapshot. Workflow and format conventions are defined in `CLEANUP_REPORT_FORMAT.md`. Issues are processed in reactions-descending order.

## Running summary
- Processed: 44 / 44
- Tests written: 3
  - Failed as expected: 1
  - Pass-green, exercises bug path: 1
  - Pass-green, does not exercise bug path: 1
  - Test error: 0
- skip — feature/proposal: 16
- skip — engine-level: 19
- skip — needs native-platform verification: 0
- likely-stale (signal-based): 0
- likely-duplicate: 6

- Duplicate clusters (tentative): 6 (RTA-1, SEL-1, LM-1, PS-1, CRASH-1, CRLF-1)
- Cross-category sibling/split-issue links: 0

## Decision types
- `write-test` — Framework-level `testWidgets`/`test` feasible.
- `skip — feature/proposal` — No regression surface.
- `skip — engine-level` — Fix lives in the engine/embedder; no framework vantage point.
- `skip — needs native-platform verification` — Expected behavior requires a missing native-platform reference.
- `likely-stale (signal-based)` — Framework testing not feasible; issue is very old/inactive.
- `likely-duplicate` — Same root cause as another in-category issue.

## Processed issues

### #61069 - [proposal] ability to change text overflow on the TextField

- **URL:** https://github.com/flutter/flutter/issues/61069
- **Decision:** **skip — feature/proposal**
**Root cause.** User wants to add an `overflow` parameter to `TextFormField` to show ellipses instead of cropping.
**Why skip — feature/proposal.** Architectural request for a new layout API on `TextField`.
**Dedup scan.** Scanned for "overflow", "ellipse". No duplicates.

### #51258 - Need to find how much of a long word could fit in one line before an unnatural line break

- **URL:** https://github.com/flutter/flutter/issues/51258
- **Decision:** **skip — feature/proposal**
**Root cause.** Users need a text measurement/breaking API to determine how much of a string without spaces fits on a line.
**Why skip — feature/proposal.** Request for a new text API. No regression surface.
**Dedup scan.** Canonical for cluster **LM-1** (Line Metrics bounds API).

### #77023 - [Web] [CanvasKit][Feature Request]: Load fonts as soon as detecting browser locale

- **URL:** https://github.com/flutter/flutter/issues/77023
- **Decision:** **skip — engine-level**
**Root cause.** CanvasKit dynamic font loading and fallback pipeline shows tofu/boxes momentarily.
**Why skip — engine-level.** Engine level font management issue.
**Dedup scan.** Scanned for "CanvasKit", "font". No duplicates yet.

### #34610 - Mixing RTL and LTR text bugs

- **URL:** https://github.com/flutter/flutter/issues/34610
- **Decision:** **skip — engine-level**
**Root cause.** SkParagraph mixed LTR/RTL text directionality mapping causes incorrect caret and deletion.
**Why skip — engine-level.** Word-boundary deletion logic in BiDi text is inside the text engine.
**Dedup scan.** Broad issue, no direct duplicates.

### #40648 - Trailing space doesn't work with TextField with TextAlign.right 

- **URL:** https://github.com/flutter/flutter/issues/40648
- **Decision:** **skip — engine-level**
**Root cause.** SkParagraph visual width trimming on trailing spaces for `TextAlign.right`.
**Why skip — engine-level.** Visual width computation happens in the engine.
**Dedup scan.** Canonical for cluster **RTA-1**.

### #78660 - Arrow keys in RTL move the wrong way

- **URL:** https://github.com/flutter/flutter/issues/78660
- **Decision:** **skip — feature/proposal**
**Root cause.** Caret traversal uses logical order rather than visual order.
**Why skip — feature/proposal.** Missing architectural capability in Intent/Action system.
**Dedup scan.** Scanned for "arrow", "RTL", "visual".

### #36854 - Feature request: Setting paragraph distance in Text and TextField

- **URL:** https://github.com/flutter/flutter/issues/36854
- **Decision:** **skip — feature/proposal**
**Root cause.** Needs parameter for paragraph spacing.
**Why skip — feature/proposal.** New property request.
**Dedup scan.** Canonical for cluster **PS-1**.

### #39755 - Selection of any justified-text is inaccurate in non-latin languages

- **URL:** https://github.com/flutter/flutter/issues/39755
- **Decision:** **skip — engine-level**
**Root cause.** Selection rects drawn by SkParagraph (`getRectsForRange`) are inaccurate for complex BiDi scripts.
**Why skip — engine-level.** Bounding box calculations are in the text engine.
**Dedup scan.** Canonical for cluster **SEL-1**.

### #90058 - TextFormField with textAlign: TextAlign.right  whitespace doesn't show unless text is entered.

- **URL:** https://github.com/flutter/flutter/issues/90058
- **Decision:** **likely-duplicate**
**Root cause.** Same as #40648.
**Why likely-duplicate.** Upstream Skia behavior.
**Dedup scan.** Member of cluster **RTA-1**.

### #91738 - [Proposal] Add support for automatically switching text input to `RTL` or `LTR` based on first character typed

- **URL:** https://github.com/flutter/flutter/issues/91738
- **Decision:** **skip — feature/proposal**
**Root cause.** Auto-directionality based on typing.
**Why skip — feature/proposal.** Architectural request.
**Dedup scan.** No duplicates.

### #71083 - TextFormField (and TextField) widgets do not wrap text correctly

- **URL:** https://github.com/flutter/flutter/issues/71083
- **Decision:** **skip — engine-level**
**Root cause.** Incorrect word wrapping on long URLs.
**Why skip — engine-level.** Line breaking and wrapping algorithm is in the text engine (LibTxt / SkParagraph).
**Dedup scan.** Scanned for "wrap", "URL".

### #91010 - `dart:ui.LineMetrics` should include the line boundaries 

- **URL:** https://github.com/flutter/flutter/issues/91010
- **Decision:** **likely-duplicate**
**Root cause.** Needs `TextRange` included in `LineMetrics`.
**Why likely-duplicate.** Duplicate request for line boundaries.
**Dedup scan.** Member of cluster **LM-1**. Canonical #51258.

### #41324 - TextField/TextFormField labelText and hintText should be right-aligned with TextDirection.rtl

- **URL:** https://github.com/flutter/flutter/issues/41324
- **Decision:** **write-test** → **pass-green, exercises bug path**
**Root cause.** `InputDecoration.labelText` failed to align to the right side of the `TextField` when `TextDirection.rtl` was used.
**Test approach.**
- Wrap a `TextField` with `Directionality(textDirection: TextDirection.rtl)`.
- Use a `labelText`.
- Assert that the physical offset `dx` of the label is positioned on the right half of the input field.
**Test:** `issue_41324_label_rtl_test.dart`
**Test outcome.** The test passed, meaning the `labelText` is now correctly right-aligned by the framework in RTL contexts.
**Dedup scan.** Scanned for "labelText", "InputDecoration", "RTL". No duplicates.

### #181759 - RTL TextField breaks when inserting emojis between existing emojis

- **URL:** https://github.com/flutter/flutter/issues/181759
- **Decision:** **skip — engine-level**
**Root cause.** Crash occurs in `wstring_convert::to_bytes` in the native embedder/engine when dynamically changing text direction.
**Why skip — engine-level.** The bug is explicitly in the platform embedder's text processing code.
**Dedup scan.** Canonical for cluster **CRASH-1**.

### #117139 - Incorrect selection area in RTL TextField.

- **URL:** https://github.com/flutter/flutter/issues/117139
- **Decision:** **likely-duplicate**
**Root cause.** Selection area doesn't match the word in RTL. Upstream Skia bug in `getRectsForRange`.
**Why likely-duplicate.** Same root cause as #39755.
**Dedup scan.** Member of cluster **SEL-1**.

### #93934 - [Desktop] TextField with pasted CRLF endings has invisible CR char

- **URL:** https://github.com/flutter/flutter/issues/93934
- **Decision:** **skip — engine-level**
**Root cause.** `\r` cursor placement is handled poorly by text layout on desktop, creating a ghost character.
**Why skip — engine-level.** Line ending interpretation and cursor positioning over invisible chars is done in SkParagraph.
**Dedup scan.** Canonical for cluster **CRLF-1**.

### #184240 - Vertical baseline alignment mismatch between Text and collapsed TextField when changing TextLeadingDistribution

- **URL:** https://github.com/flutter/flutter/issues/184240
- **Decision:** **skip — engine-level**
**Root cause.** Changing `TextLeadingDistribution` causes baseline mismatch between `Text` and `TextField`.
**Why skip — engine-level.** Text layout baselines and height metrics are computed by the engine.
**Dedup scan.** Scanned for "baseline", "alignment".

### #174689 - App highlights / selects trailing whitespaces in a multi-line textfield.

- **URL:** https://github.com/flutter/flutter/issues/174689
- **Decision:** **likely-duplicate**
**Root cause.** Selection rect incorrectly includes trailing whitespace differently than native platforms.
**Why likely-duplicate.** Belongs to the broader selection rect inaccuracies cluster originating from SkParagraph.
**Dedup scan.** Member of cluster **SEL-1**.

### #133930 - No good way to get line metrics for `Text`/`TextField` based widgets.

- **URL:** https://github.com/flutter/flutter/issues/133930
- **Decision:** **likely-duplicate**
**Root cause.** Request for framework API exposing text layout metrics reliably.
**Why likely-duplicate.** A variation of the line boundaries API gap.
**Dedup scan.** Member of cluster **LM-1**.

### #103705 - letterSpacing in TextField with monospace font is only applied to right side of the first character until a second character is entered, then letterSpacing is applied correctly to both sides

- **URL:** https://github.com/flutter/flutter/issues/103705
- **Decision:** **skip — engine-level**
**Root cause.** Skia bug involving letter spacing application on the first character.
**Why skip — engine-level.** Skia text shaping issue (fixed upstream).
**Dedup scan.** Scanned for "letterSpacing".

### #86668 - TextField doesn't handle trailing space as characters if textAlign is TextAlign.right/TextAlign.center

- **URL:** https://github.com/flutter/flutter/issues/86668
- **Decision:** **likely-duplicate**
**Root cause.** Trailing spaces do not push text or break lines as expected when `textAlign` is `center` or `right`.
**Why likely-duplicate.** Same upstream Skia issue where trailing whitespace visual width is trimmed.
**Dedup scan.** Member of cluster **RTA-1**.

### #84317 - Share code between RenderParagraph and RenderEditable

- **URL:** https://github.com/flutter/flutter/issues/84317
- **Decision:** **skip — feature/proposal**
**Root cause.** Tech-debt to share code between `RenderParagraph` and `RenderEditable` for `WidgetSpan` support.
**Why skip — feature/proposal.** Architectural refactoring. No regression surface.
**Dedup scan.** Scanned for "RenderParagraph", "RenderEditable".

### #78864 - Text does not draw correctly based on text direction

- **URL:** https://github.com/flutter/flutter/issues/78864
- **Decision:** **skip — engine-level**
**Root cause.** Text rendering directionality mapping incorrectly for Hebrew and Arabic in certain contexts.
**Why skip — engine-level.** Text shaping and directionality are handled by Skia/HarfBuzz.
**Dedup scan.** Broad RTL rendering issue, keeping an eye out for specific duplicates.

### #71318 - TextField RTL input problem with LTR letters/numbers while obscureText is true

- **URL:** https://github.com/flutter/flutter/issues/71318
- **Decision:** **skip — engine-level**
**Root cause.** When `obscureText` is true in an RTL field, typing LTR characters visually renders them in the wrong direction due to the neutral directionality of obscuring characters.
**Why skip — engine-level.** BiDi algorithm layout for neutral characters is handled by the text engine (SkParagraph).
**Dedup scan.** Scanned for "obscureText", "RTL".

### #41641 - [web] Support line height + word spacing in text fields

- **URL:** https://github.com/flutter/flutter/issues/41641
- **Decision:** **skip — feature/proposal**
**Root cause.** Request to add line height and word spacing support to `TextInput.setStyle` on web.
**Why skip — feature/proposal.** Missing API implementation.
**Dedup scan.** Scanned for "line height", "word spacing".

### #183571 - iOS: NSJSONSerialization crash when deleting SMP characters

- **URL:** https://github.com/flutter/flutter/issues/183571
- **Decision:** **skip — engine-level**
**Root cause.** Deleting SMP characters leaves orphaned UTF-16 surrogates, crashing the iOS embedder (`FlutterCodecs.mm`).
**Why skip — engine-level.** The crash and the fix are located entirely in the native iOS engine code.
**Dedup scan.** Member of cluster **CRASH-1** (Native embedder crashes on string manipulation of complex chars).

### #177953 - The framework should apply `paragraphSpacingOverride` to its text

- **URL:** https://github.com/flutter/flutter/issues/177953
- **Decision:** **likely-duplicate**
**Root cause.** Proposal to apply `paragraphSpacingOverride` to framework text widgets, blocked on `TextStyle.paragraphSpacing`.
**Why likely-duplicate.** Belongs to the broader paragraph spacing API request.
**Dedup scan.** Member of cluster **PS-1**. Canonical #36854.

### #177408 - The framework should provide a mechanism to change the paragraph spacing of text

- **URL:** https://github.com/flutter/flutter/issues/177408
- **Decision:** **likely-duplicate**
**Root cause.** Proposal for `TextStyle.paragraphSpacing`.
**Why likely-duplicate.** Duplicate proposal of #36854.
**Dedup scan.** Member of cluster **PS-1**. Canonical #36854.

### #167466 - Ellipsis not working properly when a text overflows via constrained height instead of max lines

- **URL:** https://github.com/flutter/flutter/issues/167466
- **Decision:** **skip — engine-level**
**Root cause.** Ellipsis logic fails when text is clipped by a constrained parent height instead of a `maxLines` limit.
**Why skip — engine-level.** Ellipsis insertion and text metrics during layout truncation are computed by the engine's `TextPainter` and `SkParagraph`.
**Dedup scan.** Scanned for "ellipsis", "overflow", "height".

### #165204 - Unicode characters not being rendered correctly in goldens test

- **URL:** https://github.com/flutter/flutter/issues/165204
- **Decision:** **skip — engine-level**
**Root cause.** The Ahem font used by default in `matchesGoldenFile` does not include the U+25CF bullet character, rendering as a tofu box.
**Why skip — engine-level.** Font glyph coverage and fallback in golden tests are handled at the engine/font-loading level.
**Dedup scan.** Scanned for "Ahem", "golden", "unicode".

### #155919 - Error where possible null is being asserted in rendering paragraph

- **URL:** https://github.com/flutter/flutter/issues/155919
- **Decision:** **write-test** → **pass-green, does not exercise bug path**
**Root cause.** A null assertion fires in `RenderParagraph` when an async redraw occurs with a 0-width constraint.
**Test approach.**
- Construct a layout where a `Text` widget has a 0-width constraint.
- Pump the widget and verify no exception is thrown during initial layout.
**Test:** `issue_155919_render_paragraph_null_test.dart`
**Test outcome.** The test passed, but because the bug explicitly requires "spamming asynchronous redraws by resizing the window", a simple 0-width static layout does not reach the invalid state. Kept as a baseline regression gate.
**Dedup scan.** Scanned for "RenderParagraph", "null". No duplicates.

### #144759 - Arrow key navigation gets stuck at the end of RTL text using Samsung Keyboard

- **URL:** https://github.com/flutter/flutter/issues/144759
- **Decision:** **skip — engine-level**
**Root cause.** Samsung keyboard uses visual order for arrow keys but Flutter's engine and framework use logical order, causing navigation to get stuck.
**Why skip — engine-level.** Mismatch between platform IME expectations and Flutter's text layout order strategy.
**Dedup scan.** Similar architectural gap to #78864.

### #139443 - [Windows] Incorrect character deletion in right-to-left texts

- **URL:** https://github.com/flutter/flutter/issues/139443
- **Decision:** **likely-duplicate**
**Root cause.** When RTL text contains CRLF-style line endings, the cursor offset reported is incorrect, deleting the wrong character.
**Why likely-duplicate.** Variation of Skia CRLF offset bugs.
**Dedup scan.** Member of cluster **CRLF-1**. Canonical #93934.

### #119684 - Extending to paragraph/or word boundary on MacOS should default to the `downstream` position when at a word wrap

- **URL:** https://github.com/flutter/flutter/issues/119684
- **Decision:** **skip — feature/proposal**
**Root cause.** Expanding selection to boundaries should default to downstream affinity on macOS, to match native behavior.
**Why skip — feature/proposal.** Architectural capability change for Shortcuts/Actions.
**Dedup scan.** Scanned for "downstream", "affinity".

### #113228 - Provide an API to detect if a TextPosition is located at a soft word wrap

- **URL:** https://github.com/flutter/flutter/issues/113228
- **Decision:** **skip — feature/proposal**
**Root cause.** API request on `RenderEditable` to detect soft word wraps.
**Why skip — feature/proposal.** API proposal.
**Dedup scan.** Related to metrics requests (**LM-1**), but specifically for soft-wrap bounds rather than line metrics.

### #110470 - canvas.drawLine() does not paint correctly on Samsung Galaxy Note 20 Ultra

- **URL:** https://github.com/flutter/flutter/issues/110470
- **Decision:** **skip — engine-level**
**Root cause.** Skia `canvas.drawLine` rendering bug on specific older Samsung hardware/GPUs.
**Why skip — engine-level.** Deep rendering/GPU bug in Skia.
**Dedup scan.** Scanned for "drawLine", "samsung".

### #99139 - [MacOS] Trailing whitespace in multiline TextField overflows and doesn't go to newline.

- **URL:** https://github.com/flutter/flutter/issues/99139
- **Decision:** **skip — engine-level**
**Root cause.** Trailing whitespace does not wrap on macOS, unlike native editors.
**Why skip — engine-level.** Skia text layout behavior.
**Dedup scan.** Similar to trailing whitespace handling in RTA-1, but specific to multiline wrapping.

### #92507 - Document "ghost run" and its interaction with `Paragraph.getBoxesForRange`

- **URL:** https://github.com/flutter/flutter/issues/92507
- **Decision:** **skip — engine-level**
**Root cause.** Need documentation for LibTxt/SkParagraph `ghost run` behavior which returns rects outside bounds.
**Why skip — engine-level.** Engine level text layout behavior docs.
**Dedup scan.** Scanned for "ghost run".

### #87536 - BIDI text painting skipped tests.

- **URL:** https://github.com/flutter/flutter/issues/87536
- **Decision:** **skip — feature/proposal**
**Root cause.** Tracking bug for skipped BIDI tests.
**Why skip — feature/proposal.** Tech-debt tracking bug.
**Dedup scan.** No duplicates.

### #75572 - Let RenderEditable use LineMetrics instead of assuming every line has the same height

- **URL:** https://github.com/flutter/flutter/issues/75572
- **Decision:** **skip — feature/proposal**
**Root cause.** Tech debt to refactor `RenderEditable` to use `LineMetrics` for vertical caret movement instead of assuming uniform line height.
**Why skip — feature/proposal.** Refactoring/architectural improvement request.
**Dedup scan.** Member of cluster **LM-1** conceptually, but unique enough to stand alone.

### #54998 - Directional navigation key binding defaults should be limited to those platforms that use it.

- **URL:** https://github.com/flutter/flutter/issues/54998
- **Created:** 2020-04-16 (~6.0 y old) · **Updated:** 2024-07-22
- **Reactions:** 0 (none)
- **Labels:** `framework`, `platform-macos`, `a: desktop`, `a: devtools`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** The default directional focus key bindings (arrow keys) map to specific layout structures on Mac, leading to unexpected navigation skips between disparate UI elements.
**Why skip — feature/proposal.** Architectural request to disable generic directional focus actions on platforms that do not use them (like macOS) while retaining them for specific widgets.
**Dedup scan.** Scanned for "directional", "key binding". No duplicates.

### #38503 - TextField doesn't appear within a direction:Axis.vertical Wrap

- **URL:** https://github.com/flutter/flutter/issues/38503
- **Created:** 2019-08-14 (~6.7 y old) · **Updated:** 2024-12-11
- **Reactions:** 0 (none)
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **write-test** → **fail-as-expected**

**Root cause.** `InputDecorator` throws an unbounded width assertion when used inside a `Wrap` with `direction: Axis.vertical` because a vertical wrap imposes unbounded width constraints on its children.
**Test approach.**
- Render a `Wrap` with `direction: Axis.vertical`.
- Place a `TextField` inside it.
- Expect an unbounded width assertion exception.
**Test:** `issue_38503_vertical_wrap_test.dart`
**Test outcome.** Fails as expected due to the unbounded width assertion in `InputDecorator`, confirming the framework exception logic.
**Dedup scan.** Scanned for "Wrap", "vertical", "unbounded".

### #33858 - Unicode input should be indicated.

- **URL:** https://github.com/flutter/flutter/issues/33858
- **Created:** 2019-06-04 (~6.9 y old) · **Updated:** 2024-12-13
- **Reactions:** 0 (none)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `platform-windows`, `platform-linux`, `a: desktop`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Missing visual indication (underlined 'u') for Ctrl+Shift+U unicode input mode on desktop platforms (Linux, Windows).
**Why skip — feature/proposal.** Architectural capability missing for IME composition visual indication.
**Dedup scan.** Scanned for "Unicode", "indicator".

### #13468 - TextSelection.isDirectional is not respected, make it do something useful eg: for Mac

- **URL:** https://github.com/flutter/flutter/issues/13468
- **Created:** 2017-12-09 (~8.4 y old) · **Updated:** 2024-05-09
- **Reactions:** 0 (none)
- **Labels:** `a: text input`, `framework`, `c: proposal`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** `TextSelection.isDirectional` is an unused field and not wired up to any framework behavior.
**Why skip — feature/proposal.** Architectural/API debt.
**Dedup scan.** Scanned for "isDirectional".

## Duplicate clusters
- **RTA-1** (Right Text Alignment trailing space). Canonical: #40648. Members: #90058, #86668. Upstream Skia behavior where trailing whitespace is not visually rendered when aligned right or center.
- **SEL-1** (Selection rect inaccuracies). Canonical: #39755. Members: #117139, #174689. Incorrect selection highlight areas drawn by the engine's `getRectsForRange` for BiDi, trailing spaces, etc.
- **LM-1** (Line Metrics bounds API). Canonical: #51258. Members: #91010, #133930. Architectural gaps in exposing line text boundaries and metrics to framework developers.
- **PS-1** (Paragraph Spacing API). Canonical: #36854. Members: #177953, #177408. Requests for a mechanism to control paragraph spacing.
- **CRASH-1** (Native embedder crashes on complex characters). Canonical: #181759. Members: #183571. Engine crashes related to surrogate pairs, SMP, and emojis when dynamically manipulating strings or text directions.
- **CRLF-1** (CRLF SkParagraph offsets). Canonical: #93934. Members: #139443. Windows/Desktop cursor offset issues with CRLF line endings in SkParagraph layout.

## Likely-stale candidates for closure review
- #41324: Passed regression test confirming right-alignment of labelText.

## Skipped — engine-level
- #77023: CanvasKit dynamic font loading
- #34610: SkParagraph mixed LTR/RTL rendering bugs
- #40648: SkParagraph trailing space in right-aligned text
- #39755: SkParagraph selection rects for complex scripts
- #71083: Word wrapping on long URLs
- #181759: Embedder crash on dynamically changing directionality
- #93934: SkParagraph handling of CRLF endings
- #184240: SkParagraph baseline math inconsistencies
- #103705: Skia letterSpacing application
- #78864: RTL directionality rendering issues in engine
- #71318: ObscureText masking directionality issues
- #183571: iOS embedder NSJSONSerialization crash with SMP chars
- #167466: SkParagraph ellipsis logic with height constraints
- #165204: Ahem font glyph coverage in golden tests
- #144759: Samsung keyboard visual order vs logical order
- #110470: Skia canvas.drawLine Samsung hardware bug
- #99139: macOS trailing whitespace wrapping logic
- #92507: SkParagraph ghost run documentation
