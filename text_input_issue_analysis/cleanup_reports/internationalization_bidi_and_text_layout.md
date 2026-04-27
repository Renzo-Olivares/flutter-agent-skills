# Internationalization, BiDi, and text layout Cleanup Report

This report tracks the per-issue audit of the "Internationalization, BiDi, and text layout" category from the `text_input_issues.json` snapshot. Processing follows the spec in [`CLEANUP_REPORT_FORMAT.md`](../CLEANUP_REPORT_FORMAT.md). Issues are processed in descending order by total reactions.

**Running summary**
- Processed: 44 / 44
- Tests written: 6
  - Failed as expected: 4
  - Pass-green, exercises bug path: 0
  - Pass-green, does not exercise bug path: 1
  - Test error: 1
- Skip — feature/proposal: 17
- Skip — engine-level: 15
- Skip — needs native-platform verification: 1
- Likely-stale (signal-based): 3
- Likely-duplicate: 2
- Duplicate clusters (tentative): 1 (RTL-SEL-1)
- Cross-category sibling/split-issue links: 0

## Decision types
- `write-test`: Framework-level test feasible.
- `skip — feature/proposal`: API request, no regression surface.
- `skip — engine-level`: Fix lives in engine/embedder.
- `skip — needs native-platform verification`: Needs a platform reference we lack.
- `likely-stale`: Age/inactivity suggests invalid.
- `likely-duplicate`: Same root cause as an in-category issue.

## Processed issues

### #119684 — Extending to paragraph/or word boundary on MacOS should default to the `downstream` position when at a word wrap

- **URL:** https://github.com/flutter/flutter/issues/119684
- **Created:** 2023-02-01 (~3.2 y old) · **Updated:** 2024-06-06
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `platform-macos`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — needs native-platform verification**

**Root cause.** Selection extension via `Option+Shift+Arrow` shortcuts on macOS exhibits unexpected behavior at word wrap boundaries compared to native macOS behavior.

**Why skip-needs native-platform verification / Test approach.** To author a valid regression test, we need a verified behavioral baseline from the current native macOS text system to ensure our `DefaultTextEditingShortcuts` intent handlers mimic it perfectly.

**Dedup scan.** Scanned for "paragraph boundary", "downstream", "word wrap". No duplicates.

### #139443 — [Windows] Incorrect character deletion in right-to-left texts

- **URL:** https://github.com/flutter/flutter/issues/139443
- **Created:** 2023-12-03 (~2.4 y old) · **Updated:** 2025-08-21
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `platform-windows`, `has reproducible steps`, `P3`, `found in release: 3.16`, `found in release: 3.18`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Incorrect caret placement and character deletion in multiline RTL text fields on Windows. Triggered specifically when typing text manually (which inserts CRLF-style line endings) rather than pasting.

**Why skip-engine / Test approach.** The engine (specifically `SkParagraph` and the embedder's text mapping) mishandles CRLF line endings when determining caret offsets in RTL mode. Framework tests cannot override or fix this layout bug.

**Dedup scan.** Scanned for "Incorrect character deletion", "CRLF". No duplicates.

### #144759 — Arrow key navigation gets stuck at the end of RTL text using Samsung Keyboard

- **URL:** https://github.com/flutter/flutter/issues/144759
- **Created:** 2024-03-07 (~2.1 y old) · **Updated:** 2024-03-07
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 3.19`, `team-text-input`, `triaged-text-input`, `found in release: 3.21`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Arrow key navigation gets stuck at the end of RTL text when using the Samsung Keyboard because the keyboard operates in visual order while Flutter uses logical order.

**Why skip-engine / Test approach.** This is a fundamental mismatch between the native Android IME (Samsung Keyboard) behavior and Flutter's text model. 

**Dedup scan.** Scanned for "Samsung Keyboard", "Arrow key". No duplicates.

### #155919 — Error where possible null is being asserted in rendering paragraph

- **URL:** https://github.com/flutter/flutter/issues/155919
- **Created:** 2024-09-30 (~1.6 y old) · **Updated:** 2024-10-23
- **Reactions:** 0
- **Labels:** `framework`, `a: error message`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **write-test** → **pass-green, does not exercise the real bug path**

**Root cause.** A null assertion fires in `RenderParagraph` when resizing a window on macOS causes a `Text` widget within a `Row` to be constrained to a 0-width `BoxConstraints`.

**Test approach.** Drafted a test pumping a `Row` with an `Expanded(child: Text)` and a `Text` constrained to 0 width.

**Test:** [`issue_155919_render_paragraph_zero_width_test.dart`](../regression_tests/internationalization_bidi_and_text_layout/issue_155919_render_paragraph_zero_width_test.dart)

**Test outcome.** The test passed without any assertion errors. Because the bug reporter noted it happens during asynchronous redraws while spam-resizing the macOS window, a simple static 0-width constraint does not fully exercise the exact bug path that triggers the null assertion.

**Dedup scan.** Scanned for "possible null", "RenderParagraph", "0 width". No duplicates.

### #165204 — Unicode characters not being rendered correctly in goldens test

- **URL:** https://github.com/flutter/flutter/issues/165204
- **Created:** 2025-03-14 (~1.1 y old) · **Updated:** 2025-03-27
- **Reactions:** 0
- **Labels:** `a: tests`, `a: text input`, `framework`, `has reproducible steps`, `P3`, `team-text-input`, `triaged-text-input`, `found in release: 3.29`, `found in release: 3.31`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Certain Unicode characters (like `\u25CF`) render as tofu boxes in golden tests because the default test font (`Ahem`) does not include those glyphs.

**Why skip-proposal / Test approach.** This is a testing infrastructure request (updating the `Ahem` font or improving default fallback behaviors in tests), not a bug in the text input framework's production code.

**Dedup scan.** Scanned for "goldens test", "Ahem", "tofu". No duplicates.

### #167466 — Ellipsis not working properly when a text overflows via constrained height instead of max lines

- **URL:** https://github.com/flutter/flutter/issues/167466
- **Created:** 2025-04-21 (~1.0 y old) · **Updated:** 2025-12-21
- **Reactions:** 0
- **Labels:** `framework`, `a: typography`, `c: rendering`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.29`, `found in release: 3.32`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** `TextOverflow.ellipsis` is not applied when text is clipped due to its parent's constrained height, rather than being explicitly constrained by `maxLines`.

**Why skip-engine / Test approach.** Text ellipsis rendering is handled internally by `SkParagraph` layout algorithms, which only insert an ellipsis when breaking lines based on a `maxLines` limit, not based on vertical height clipping.

**Dedup scan.** Scanned for "constrained height", "ellipsis not working". No duplicates.

### #177408 — The framework should provide a mechanism to change the paragraph spacing of text

- **URL:** https://github.com/flutter/flutter/issues/177408
- **Created:** 2025-10-22 (~0.5 y old) · **Updated:** 2026-01-06
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `a: accessibility`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Feature request to add `paragraphSpacing` to `TextStyle` to control spacing between paragraphs.

**Why skip-proposal / Test approach.** API feature request.

**Dedup scan.** Scanned for "paragraph spacing". No duplicates.

### #177953 — The framework should apply `paragraphSpacingOverride` to its text

- **URL:** https://github.com/flutter/flutter/issues/177953
- **Created:** 2025-11-03 (~0.5 y old) · **Updated:** 2026-01-02
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `a: accessibility`, `platform-web`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Feature request to automatically apply `MediaQueryData.paragraphSpacingOverride` to text layout globally for accessibility.

**Why skip-proposal / Test approach.** API feature request building on #177408.

**Dedup scan.** Scanned for "paragraphSpacingOverride". No duplicates.

### #183571 — iOS: NSJSONSerialization crash when deleting SMP characters

- **URL:** https://github.com/flutter/flutter/issues/183571
- **Created:** 2026-03-12 (~0.1 y old) · **Updated:** 2026-03-19
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-ios`, `P1`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Deleting Supplementary Multilingual Plane (SMP) characters on iOS leaves orphaned UTF-16 surrogates, causing `NSJSONSerialization` to fail and crash the app.

**Why skip-engine / Test approach.** A fix is already proposed in the engine codebase (`FlutterCodecs.mm`). The framework cannot catch or test this low-level iOS serialization failure.

**Dedup scan.** Scanned for "NSJSONSerialization", "SMP". No duplicates.


### #13468 — TextSelection.isDirectional is not respected, make it do something useful eg: for Mac

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


### #181759 — RTL TextField breaks when inserting emojis between existing emojis

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


### #78660 — Arrow keys in RTL move the wrong way

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

**Root cause.** Pasting text with CRLF (`
`) endings causes the `
` character to be inserted as an invisible character, disrupting arrow key navigation and rendering.

**Test approach.** Attempted to test by simulating a paste from clipboard with `
` and asserting caret movement using arrow keys.

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


### #40648 — Trailing space doesn't work with TextField with TextAlign.right 

- **URL:** https://github.com/flutter/flutter/issues/40648
- **Created:** 2019-09-17 (~6.5 y old) · **Updated:** 2025-01-29
- **Reactions:** 16
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.5`, `found in release: 2.6`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause.** Trailing spaces are visually trimmed or fail to render the cursor advancement when a `TextField` is set to `TextAlign.right`. This happens because `SkParagraph` drops or mishandles trailing whitespace width in right-aligned contexts.

**Why skip-engine / Test approach.** A corresponding Skia bug (issue 11933) confirms the root cause lives in `SkParagraph` layout algorithms. The framework merely passes `TextAlign.right` to the engine, which incorrectly computes the cursor or line width. This cannot be fixed or isolated with a framework test.

**Dedup scan.** Scanned for "TextAlign.right", "trailing space", "whitespace". Found #90058 ("TextFormField with textAlign: TextAlign.right whitespace doesn't show unless text is entered"), which is a clear duplicate. 


### #34610 — Mixing RTL and LTR text bugs

- **URL:** https://github.com/flutter/flutter/issues/34610
- **Created:** 2019-06-17 (~6.8 y old) · **Updated:** 2024-03-06
- **Reactions:** 18
- **Labels:** `a: text input`, `framework`, `engine`, `a: typography`, `customer: crowd`, `P2`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — engine-level**

**Root cause.** When mixing LTR and RTL text, `ParagraphStyle` directionality, caret positioning, and deletion behave unexpectedly. Spaces and ellipses may appear in the middle of mixed-direction text rather than at the ends.

**Why skip-engine / Test approach.** As confirmed by the raw comments and ownership, the fix requires changes to the underlying text rendering engine (`SkParagraph`). Framework tests cannot meaningfully isolate these BiDi rendering edge cases because they depend entirely on the engine's glyph run analysis and layout algorithms.

**Dedup scan.** Scanned for "RTL", "LTR", "mixing", "BiDi". Issue #39755 mentions justified text in non-latin languages, but focuses on justification rather than directionality mixing. No clear duplicates found.


### #77023 — [Web] [CanvasKit][Feature Request]: Load fonts as soon as detecting browser locale

- **URL:** https://github.com/flutter/flutter/issues/77023
- **Created:** 2021-03-02 (~5.1 y old) · **Updated:** 2025-10-30
- **Reactions:** 21
- **Labels:** `a: text input`, `c: new feature`, `a: internationalization`, `a: typography`, `platform-web`, `c: proposal`, `c: rendering`, `e: web_canvaskit`, `P2`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level**

**Root cause.** On Flutter Web with CanvasKit, dynamic font loading for CJK (and other non-Latin characters like Arabic and Hebrew) happens lazily. When a character is first typed, a "tofu" or gibberish glyph is rendered momentarily while the fallback font is fetched.

**Why skip-engine / Test approach.** The font-loading pipeline and fallback rendering strategy are part of the web engine (`flutter/engine` -> `lib/web_ui`). There is no framework-level test that can meaningfully assert against the network-bound timing of CanvasKit fallback font fetching.

**Dedup scan.** Searched for "CanvasKit", "font", "gibberish". No other issues in this category describe dynamic font-loading flashes.


### #51258 — Need to find how much of a long word could fit in one line before an unnatural line break

- **URL:** https://github.com/flutter/flutter/issues/51258
- **Created:** 2020-02-22 (~6.2 y old) · **Updated:** 2023-07-08
- **Reactions:** 28
- **Labels:** `a: text input`, `framework`, `a: typography`, `c: proposal`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** The user is requesting a new typography API (similar to Android's `Paint.breakText`) to determine how many characters of a string will fit within a specified physical width. This is especially tricky for context-dependent glyphs like Mongolian or Arabic.

**Why skip-proposal / Test approach.** This is an API feature request for text measurement primitives. There is no bug path or framework regression surface to test here.

**Dedup scan.** Searched for "breakText" and "unnatural line break". No duplicates found in this category. (The issue explicitly references #35994 and #50171, but neither is in our category's purview).


### #61069 — [proposal] ability to change text overflow on the TextField

- **URL:** https://github.com/flutter/flutter/issues/61069
- **Created:** 2020-07-08 (~5.8 y old) · **Updated:** 2025-07-18
- **Reactions:** 65
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `c: proposal`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** The user is requesting a feature to add `overflow` handling (e.g., `TextOverflow.ellipsis`) to single-line text fields when the text exceeds the available space.

**Why skip-proposal / Test approach.** This is an API request for a new `overflow` property on `TextField`/`TextFormField`. There is no bug path to test, just a missing feature.

**Dedup scan.** Scanned for "overflow" and "ellipsis". Found #99139 (MacOS trailing whitespace multiline overflow) and #167466 (ellipsis bug on constrained height), but these are different bugs. No exact duplicates found.


## Duplicate clusters

- **RTL-SEL-1** RTL selection rect inaccuracies (Canonical: #117139, Members: #39755)

## Likely-stale candidates for closure review

## Cross-category sibling / split-issue links

## Skipped — engine-level
- #139443 ([Windows] Incorrect character deletion in right-to-left texts)
- #144759 (Arrow key navigation gets stuck at the end of RTL text using Samsung Keyboard)
- #167466 (Ellipsis not working properly when a text overflows via constrained height instead of max lines)
- #183571 (iOS: NSJSONSerialization crash when deleting SMP characters)
- #99139 ([MacOS] Trailing whitespace in multiline TextField overflows and doesn't go to newline.)
- #110470 (canvas.drawLine() does not paint correctly on Samsung Galaxy Note 20 Ultra)
- #181759 (RTL TextField breaks when inserting emojis between existing emojis)
- #71318 (TextField RTL input problem with LTR letters/numbers while obscureText is true)
- #174689 (App highlights / selects trailing whitespaces in a multi-line textfield.)
- #39755 (Selection of any justified-text is inaccurate in non-latin languages)
- #71083 (TextFormField (and TextField) widgets do not wrap text correctly)
- #117139 (Incorrect selection area in RTL TextField.)
- #40648 (Trailing space does not work with TextAlign.right)
- #34610 (Mixing RTL and LTR text bugs)
- #77023 ([Web] [CanvasKit][Feature Request]: Load fonts as soon as detecting browser locale)
