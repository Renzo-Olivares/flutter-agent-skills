# Internationalization, BiDi, and text layout Cleanup Report

This report covers the "Internationalization, BiDi, and text layout" category from the `2026-04-17` snapshot. See [`CLEANUP_REPORT_FORMAT.md`](../CLEANUP_REPORT_FORMAT.md) for the workflow and decision palette. Issues are processed in reactions-descending order.

## Running summary

- Processed: 44 / 44
- Tests written: 1
  - Failed as expected: 0
  - Pass-green, exercises bug path: 1
  - Pass-green, does not exercise bug path: 0
  - Test error: 0
- Skip — feature/proposal: 18
- Skip — engine-level: 21
- Skip — needs native-platform verification: 0
- Likely-stale (signal-based): 2
- Likely-duplicate: 2
- Duplicate clusters (tentative): 8 (RTL-TR-1, RTL-SEL-1, RTL-OBS-1, RTL-LINE-1, RTL-NAV-1, CRLF-1, SURR-1, TYPO-PARA-1)
- Cross-category sibling/split-issue links: 0

## Decision types

- `write-test`: Framework-level `testWidgets`/`test` feasible. Author it, run it, record outcome below.
- `skip — feature/proposal`: `c: proposal` / `c: new feature` / architectural request. No regression surface.
- `skip — engine-level`: Fix lives in the engine/embedder; no framework vantage point where the bug's observable behavior reaches a `testWidgets`.
- `skip — needs native-platform verification`: Framework-testable in principle, but the expected behavior requires a current native-platform reference we don't have.
- `likely-stale (signal-based)`: Framework testing not feasible; age + inactivity + obvious framework evolution since filing strongly suggest the issue is no longer valid.
- `likely-duplicate`: Same root cause as another in-category issue. Canonical identified; merge recommended.

## Processed issues

### #61069 — [proposal] ability to change text overflow on the TextField

- **URL:** https://github.com/flutter/flutter/issues/61069
- **Created:** 2020-07-08 · **Updated:** 2025-07-18
- **Reactions:** 65
- **Labels:** `a: text input, c: new feature, framework, f: material design, c: proposal, P2, team-text-input, triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** User is requesting an `overflow` parameter on `TextField` similar to what exists on the `Text` widget to allow for ellipsis truncation instead of cropping.

**Why feature/proposal.** Architectural request for a new API parameter (`overflow`) on `TextField` and its underlying renderers.

**Dedup scan.** No obvious in-category duplicates found for text overflow settings yet.

### #51258 — Need to find how much of a long word could fit in one line before an unnatural line break

- **URL:** https://github.com/flutter/flutter/issues/51258
- **Created:** 2020-02-22 · **Updated:** 2023-07-08
- **Reactions:** 28
- **Labels:** `a: text input, framework, a: typography, c: proposal, P3, team-framework, triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** Request for a way to measure how much of a string fits on a line before wrapping, to facilitate custom text layout for non-rectangular areas.

**Why feature/proposal.** Request for a new framework-level measurement API or text layout capability.

**Dedup scan.** No in-category duplicates.

### #77023 — [Web] [CanvasKit][Feature Request]: Load fonts as soon as detecting browser locale

- **URL:** https://github.com/flutter/flutter/issues/77023
- **Created:** 2021-03-02 · **Updated:** 2025-10-30
- **Reactions:** 21
- **Labels:** `a: text input, c: new feature, a: internationalization, a: typography, platform-web, c: proposal, c: rendering, e: web_canvaskit, P2, team-web, triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level**

**Root cause.** The CanvasKit web renderer dynamically loads CJK fonts only when unknown characters are first encountered, leading to visual popping (tofus -> characters).

**Why engine-level.** The fix lives in the CanvasKit engine's font fallback and loading pipeline. There is no framework vantage point to control this early loading transparently.

**Dedup scan.** No in-category duplicates for web font loading detected yet.

### #34610 — Mixing RTL and LTR text bugs

- **URL:** https://github.com/flutter/flutter/issues/34610
- **Created:** 2019-06-17 · **Updated:** 2024-03-06
- **Reactions:** 18
- **Labels:** `a: text input, framework, engine, a: typography, customer: crowd, P2, team-engine, triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — engine-level**

**Root cause.** Mixed RTL/LTR text suffers from bugs in caret positioning, deletion bounds, and spacing. Root cause was identified as `ParagraphStyle` directionality and SkParagraph behavior on mixed text boundaries.

**Why engine-level.** Fix targets `SkParagraph` and engine-level text layout and selection measurement routines.

**Dedup scan.** Broad issue covering multiple RTL/LTR boundary bugs. Will watch for other caret/deletion bugs in mixed text.

### #40648 — Trailing space doesn't work with TextField with TextAlign.right 

- **URL:** https://github.com/flutter/flutter/issues/40648
- **Created:** 2019-09-17 · **Updated:** 2025-01-29
- **Reactions:** 16
- **Labels:** `a: text input, framework, f: material design, has reproducible steps, P2, found in release: 2.5, found in release: 2.6, team-framework, triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause.** `TextAlign.right` causes trailing whitespace to be visually trimmed/unrendered. Identified as a Skia bug (11933) where `SkParagraph` treats `\r` and trailing spaces in right-aligned text incorrectly.

**Why engine-level.** Fix targets Skia / `SkParagraph` text alignment layout logic.

**Dedup scan.** Found exact duplicates: #90058, #86668. Canonical for cluster RTL-TR-1.

### #78660 — Arrow keys in RTL move the wrong way

- **URL:** https://github.com/flutter/flutter/issues/78660
- **Created:** 2021-03-19 · **Updated:** 2024-03-06
- **Reactions:** 15
- **Labels:** `a: text input, framework, f: material design, a: internationalization, has reproducible steps, P2, found in release: 2.1, team-framework, triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** Arrow keys currently traverse logical string order, which visually moves the cursor in the "wrong" direction in RTL blocks. User wants visual-order traversal.

**Why feature/proposal.** Acknowledged as a missing architectural feature: visual-order traversal needs to be implemented likely by extending the Intent/Action system's `forward` concept.

**Dedup scan.** Belongs to cluster RTL-NAV-1 (Visual vs logical cursor navigation).

### #36854 — Feature request: Setting paragraph distance in Text and TextField

- **URL:** https://github.com/flutter/flutter/issues/36854
- **Created:** 2019-07-24 · **Updated:** 2024-03-06
- **Reactions:** 12
- **Labels:** `a: text input, c: new feature, framework, f: material design, a: typography, P3, team-framework, triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** Request to add paragraph spacing capabilities to `Text` and `TextField`.

**Why feature/proposal.** Feature request for new typographic API surface.

**Dedup scan.** Relates to #177408, #177953. Opened tentative cluster TYPO-PARA-1.

### #39755 — Selection of any justified-text is inaccurate in non-latin languages

- **URL:** https://github.com/flutter/flutter/issues/39755
- **Created:** 2019-09-03 · **Updated:** 2024-03-06
- **Reactions:** 10
- **Labels:** `a: text input, framework, f: material design, a: internationalization, a: typography, has reproducible steps, P2, found in release: 3.3, found in release: 3.7, team-framework, triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause.** Selection highlight rects generated for non-latin scripts (Arabic, Hebrew, Korean) are inaccurate, especially in mixed text or justified text, due to engine text layout reporting.

**Why engine-level.** Fix requires correcting selection geometry outputs (`getRectsForRange`) in `libtxt` / `SkParagraph` for complex scripts.

**Dedup scan.** Part of the broader engine selection bounds problem family. Included in cluster RTL-SEL-1.

### #90058 — TextFormField with textAlign: TextAlign.right  whitespace doesn't show unless text is entered.

- **URL:** https://github.com/flutter/flutter/issues/90058
- **Created:** 2021-09-14 · **Updated:** 2025-08-13
- **Reactions:** 6
- **Labels:** `a: text input, framework, f: material design, has reproducible steps, P2, found in release: 2.5, found in release: 2.6, team-design, triaged-design`
- **Ownership:** `team-design`
- **Decision:** **likely-duplicate**

**Root cause.** Trailing spaces are not rendered when `TextAlign.right` is used. Same root cause as #40648.

**Dedup scan.** Exact duplicate of #40648. Added to tentative cluster RTL-TR-1.

### #71083 — TextFormField (and TextField) widgets do not wrap text correctly

- **URL:** https://github.com/flutter/flutter/issues/71083
- **Created:** 2020-11-23 · **Updated:** 2024-03-06
- **Reactions:** 5
- **Labels:** `a: text input, framework, f: material design, dependency: skia, a: typography, P2, team-design, triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause.** Line breaking algorithm breaks words in the middle instead of pushing to the next line for long URLs/unspaced strings.

**Why engine-level.** Line breaking logic lives inside Skia/SkParagraph. The framework just reports the string; the engine determines wrap points.

**Dedup scan.** No in-category duplicates yet.

### #91738 — [Proposal] Add support for automatically switching text input to `RTL` or `LTR` based on first character typed

- **URL:** https://github.com/flutter/flutter/issues/91738
- **Created:** 2021-10-13 · **Updated:** 2023-09-15
- **Reactions:** 5
- **Labels:** `a: text input, c: new feature, framework, a: internationalization, c: proposal, P3, team-framework, triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** Proposal to automatically determine text direction from the first typed character.

**Why feature/proposal.** Architectural request for auto-bidi functionality requiring engine API and `TextPainter` modifications.

**Dedup scan.** No in-category duplicates found.

### #91010 — `dart:ui.LineMetrics` should include the line boundaries 

- **URL:** https://github.com/flutter/flutter/issues/91010
- **Created:** 2021-09-30 · **Updated:** 2023-09-19
- **Reactions:** 4
- **Labels:** `a: text input, engine, a: typography, c: proposal, P3, team-engine, triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — engine-level**

**Root cause.** `dart:ui.LineMetrics` strips out text boundaries, preventing framework from cleanly determining vertical caret navigation.

**Why engine-level.** Fix lives in engine `Metrics.h` to propagate boundaries. The framework has no vantage point until the API is changed.

**Dedup scan.** Relates to #75572. Included in cluster RTL-LINE-1.

### #41324 — TextField/TextFormField labelText and hintText should be right-aligned with TextDirection.rtl

- **URL:** https://github.com/flutter/flutter/issues/41324
- **Created:** 2019-09-25 · **Updated:** 2026-02-16
- **Reactions:** 3
- **Labels:** `a: text input, c: new feature, framework, f: material design, a: internationalization, P2, team-text-input, triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **write-test** [→ **pass-green, exercises bug path**]

**Root cause.** `labelText` in `InputDecoration` fails to right-align under `TextDirection.rtl`.

**Test:** [`issue_41324_textfield_labeltext_rtl_test.dart`](../regression_tests/internationalization_bidi_and_text_layout_v6/issue_41324_textfield_labeltext_rtl_test.dart)

**Test outcome.** Test passes green. The `labelText` `dx` offset is properly right-aligned (>400.0), indicating that the bug has likely been fixed in modern framework versions.

**Dedup scan.** No exact duplicates. Test passes green, indicating fix may have silently landed. Added test `issue_41324_textfield_labeltext_rtl_test.dart`.

### #93934 — [Desktop] TextField with pasted CRLF endings has invisible CR char

- **URL:** https://github.com/flutter/flutter/issues/93934
- **Created:** 2021-11-19 · **Updated:** 2024-06-07
- **Reactions:** 2
- **Labels:** `a: text input, framework, platform-windows, a: desktop, has reproducible steps, P2, found in release: 2.5, found in release: 2.6, found in release: 2.8, team-windows, triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **skip — engine-level**

**Root cause.** Carriage return characters (`\r`) from pasted CRLF text behave as invisible extra characters that the arrow keys navigate over on desktop.

**Why engine-level.** The way `SkParagraph` and engine text layout report caret boundaries for `\r` characters dictates cursor behavior.

**Dedup scan.** Shares root cause with #139443. Canonical for cluster CRLF-1.

### #117139 — Incorrect selection area in RTL TextField.

- **URL:** https://github.com/flutter/flutter/issues/117139
- **Created:** 2022-12-15 · **Updated:** 2023-07-08
- **Reactions:** 2
- **Labels:** `a: text input, framework, a: internationalization, has reproducible steps, P2, found in release: 3.3, found in release: 3.7, team-framework, triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause.** `getRectsForRange` produces incorrect selection geometry for a dot character at the end of a line followed by another line in RTL.

**Why engine-level.** Root cause identified as Skia bug 14035 in `SkParagraph`'s `getRectsForRange`.

**Dedup scan.** Belongs to the broader cluster of SkParagraph selection-geometry issues in RTL. Included in cluster RTL-SEL-1.

### #181759 — RTL TextField breaks when inserting emojis between existing emojis

- **URL:** https://github.com/flutter/flutter/issues/181759
- **Created:** 2026-01-31 · **Updated:** 2026-03-06
- **Reactions:** 2
- **Labels:** `a: text input, platform-android, framework, f: material design, platform-macos, P2, team-text-input, triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Engine crashes or invalidates IME composition state when inserting emojis into RTL text due to text direction changing during composition.

**Why engine-level.** The issue causes engine-level aborts (macOS/Linux) and IME failures (Android) due to surrogate pair handling in the embedder layer.

**Dedup scan.** Shares surrogate pair JSON decoding crash root cause with #183571. Included in cluster SURR-1.

### #41641 — [web] Support line height + word spacing in text fields

- **URL:** https://github.com/flutter/flutter/issues/41641
- **Created:** 2019-09-30 · **Updated:** 2024-03-06
- **Reactions:** 1
- **Labels:** `a: text input, c: new feature, framework, platform-web, P3, team-web, triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — feature/proposal**

**Root cause.** Feature request to support line height and word spacing in text fields on web.

**Why feature/proposal.** Feature request for new API parameters to be plumbed through to the engine.

**Dedup scan.** No exact duplicates.

### #71318 — TextField RTL input problem with LTR letters/numbers while obscureText is true

- **URL:** https://github.com/flutter/flutter/issues/71318
- **Created:** 2020-11-27 · **Updated:** 2024-07-11
- **Reactions:** 1
- **Labels:** `a: text input, framework, engine, f: material design, a: typography, has reproducible steps, P2, found in release: 3.3, found in release: 3.7, team-design, triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause.** Obscured characters (bullets) are drawn in logical order rather than visual RTL order when typing LTR letters in an obscured RTL field.

**Why engine-level.** Text layout and bullet substitution is performed by `SkParagraph`, which handles the RTL/LTR layout.

**Dedup scan.** Found related issues #47745, #50098, #54099 mentioned in comments. Canonical for cluster RTL-OBS-1.

### #78864 — Text does not draw correctly based on text direction

- **URL:** https://github.com/flutter/flutter/issues/78864
- **Created:** 2021-03-23 · **Updated:** 2025-07-22
- **Reactions:** 1
- **Labels:** `a: text input, framework, f: material design, a: internationalization, a: typography, has reproducible steps, P2, found in release: 2.1, team-design, triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause.** Text direction is rendered incorrectly. Vague description.

**Why engine-level.** Layout bugs with directional text without specific framework misconfiguration usually trace back to `SkParagraph`.

**Dedup scan.** Too vague to strongly cluster, but related to general RTL layout issues.

### #84317 — Share code between RenderParagraph and RenderEditable

- **URL:** https://github.com/flutter/flutter/issues/84317
- **Created:** 2021-06-10 · **Updated:** 2023-07-08
- **Reactions:** 1
- **Labels:** `a: text input, framework, a: typography, P2, c: tech-debt, team-framework, triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** Tech debt ticket to share code between `RenderParagraph` and `RenderEditable`.

**Why feature/proposal.** Tech debt/architectural restructuring. No observable bug regression surface.

**Dedup scan.** No duplicates.

### #86668 — TextField doesn't handle trailing space as characters if textAlign is TextAlign.right/TextAlign.center

- **URL:** https://github.com/flutter/flutter/issues/86668
- **Created:** 2021-07-19 · **Updated:** 2024-09-26
- **Reactions:** 1
- **Labels:** `a: text input, framework, f: material design, has reproducible steps, P2, found in release: 2.2, found in release: 2.4, team-text-input, triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **likely-duplicate**

**Root cause.** Trailing spaces do not render or break lines when `textAlign` is right or center.

**Dedup scan.** Exact duplicate of #40648 and #90058. Added to cluster RTL-TR-1.

### #103705 — letterSpacing in TextField with monospace font is only applied to right side of the first character until a second character is entered, then letterSpacing is applied correctly to both sides

- **URL:** https://github.com/flutter/flutter/issues/103705
- **Created:** 2022-05-13 · **Updated:** 2023-07-08
- **Reactions:** 1
- **Labels:** `a: text input, engine, a: typography, has reproducible steps, P2, found in release: 3.0, found in release: 3.1, team-engine, triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — engine-level**

**Root cause.** Letter spacing geometry is incorrect for the first character in monospace fonts. Skia bug.

**Why engine-level.** Fix was submitted and merged in Skia (skia-review.googlesource.com/c/skia/+/541978).

**Dedup scan.** No exact duplicates for letterSpacing monospace.

### #133930 — No good way to get line metrics for `Text`/`TextField` based widgets.

- **URL:** https://github.com/flutter/flutter/issues/133930
- **Created:** 2023-09-03 · **Updated:** 2024-08-23
- **Reactions:** 1
- **Labels:** `framework, a: typography, has reproducible steps, P2, found in release: 3.13, found in release: 3.14, team-text-input, triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Request for a framework API to get line metrics from a `TextField` without manually matching its `TextStyle`.

**Why feature/proposal.** Architectural request for a new `onTextLayoutChanged` callback or similar text metrics API on the framework layer.

**Dedup scan.** No in-category duplicates.

### #174689 — App highlights / selects trailing whitespaces in a multi-line textfield.

- **URL:** https://github.com/flutter/flutter/issues/174689
- **Created:** 2025-08-29 · **Updated:** 2025-09-18
- **Reactions:** 1
- **Labels:** `a: text input, platform-android, platform-ios, a: desktop, has reproducible steps, P2, team-text-input, triaged-text-input, found in release: 3.35, found in release: 3.36`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Highlight/selection rects extend to trailing whitespace in multi-line fields on mobile/desktop, unlike native apps.

**Why engine-level.** Selection geometry mapping for whitespace comes from the embedder/engine text layout routines.

**Dedup scan.** Related to RTL-TR-1, but specifically about selection rendering. Added to cluster RTL-SEL-1.

### #184240 — Vertical baseline alignment mismatch between Text and collapsed TextField when changing TextLeadingDistribution

- **URL:** https://github.com/flutter/flutter/issues/184240
- **Created:** 2026-03-27 · **Updated:** 2026-04-02
- **Reactions:** 1
- **Labels:** `framework, f: material design, has reproducible steps, team-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Vertical baseline alignment mismatch when `TextLeadingDistribution` changes.

**Why engine-level.** Baseline metrics and alignment computations are engine-level layout properties reported by `SkParagraph`.

**Dedup scan.** No exact duplicates in this category yet.

### #13468 — TextSelection.isDirectional is not respected, make it do something useful eg: for Mac

- **URL:** https://github.com/flutter/flutter/issues/13468
- **Created:** 2017-12-09 · **Updated:** 2024-05-09
- **Reactions:** 0
- **Labels:** `a: text input, framework, c: proposal, P2, team-text-input, triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Tech debt. The `isDirectional` property on `TextSelection` does nothing and should either be wired up or removed.

**Why feature/proposal.** Cleanup/Tech-debt request.

**Dedup scan.** No duplicates.

### #33858 — Unicode input should be indicated.

- **URL:** https://github.com/flutter/flutter/issues/33858
- **Created:** 2019-06-04 · **Updated:** 2024-12-13
- **Reactions:** 0
- **Labels:** `a: text input, c: new feature, framework, f: material design, platform-windows, platform-linux, a: desktop, P3, team-text-input, triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Linux/Windows native `Ctrl+Shift+U` unicode entry state is not visually indicated in Flutter text fields.

**Why feature/proposal.** Feature request for IME composition visual indication.

**Dedup scan.** No duplicates.

### #38503 — TextField doesn't appear within a direction:Axis.vertical Wrap

- **URL:** https://github.com/flutter/flutter/issues/38503
- **Created:** 2019-08-14 · **Updated:** 2024-12-11
- **Reactions:** 0
- **Labels:** `a: text input, framework, f: material design, has reproducible steps, P2, found in release: 3.3, found in release: 3.7, team-design, triaged-design`
- **Ownership:** `team-design`
- **Decision:** **likely-stale (signal-based)**

**Root cause.** `InputDecorator` throws an unbounded width exception when placed inside a vertical `Wrap` without explicit constraints.

**Dedup scan.** No duplicates.

### #54998 — Directional navigation key binding defaults should be limited to those platforms that use it.

- **URL:** https://github.com/flutter/flutter/issues/54998
- **Created:** 2020-04-16 · **Updated:** 2024-07-22
- **Reactions:** 0
- **Labels:** `framework, platform-macos, a: desktop, a: devtools, P2, team-text-input, triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Request to change default keybindings in `app.dart` so directional focus navigation isn't enabled by default on macOS where it isn't standard.

**Why feature/proposal.** Default platform configuration change request.

**Dedup scan.** No duplicates.

### #75572 — Let RenderEditable use LineMetrics instead of assuming every line has the same height

- **URL:** https://github.com/flutter/flutter/issues/75572
- **Created:** 2021-02-07 · **Updated:** 2026-03-05
- **Reactions:** 0
- **Labels:** `a: text input, framework, f: material design, P2, c: tech-debt, team-design, triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal**

**Root cause.** `RenderEditable` currently assumes uniform line height when determining caret vertical movement. It should use actual `LineMetrics` from engine.

**Why feature/proposal.** Tech debt/architectural request.

**Dedup scan.** Relates to #91010. Included in cluster RTL-LINE-1.

### #87536 — BIDI text painting skipped tests.

- **URL:** https://github.com/flutter/flutter/issues/87536
- **Created:** 2021-08-03 · **Updated:** 2023-07-08
- **Reactions:** 0
- **Labels:** `a: text input, c: contributor-productivity, framework, a: internationalization, P2, c: tech-debt, team: skip-test, team-framework, triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** Tracking bug for skipped BIDI tests in `text_painter_rtl_test.dart`.

**Why feature/proposal.** Tech debt/testing tracking issue, no product bug.

**Dedup scan.** No duplicates.

### #92507 — Document "ghost run" and its interaction with `Paragraph.getBoxesForRange`

- **URL:** https://github.com/flutter/flutter/issues/92507
- **Created:** 2021-10-26 · **Updated:** 2023-08-04
- **Reactions:** 0
- **Labels:** `a: text input, engine, d: api docs, a: typography, P2, team-engine, triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — engine-level**

**Root cause.** Missing API documentation for "ghost run" in engine's C++ text layout code (`Paragraph.getBoxesForRange`).

**Why engine-level.** C++ documentation request.

**Dedup scan.** No duplicates.

### #99139 — [MacOS] Trailing whitespace in multiline TextField overflows and doesn't go to newline.

- **URL:** https://github.com/flutter/flutter/issues/99139
- **Created:** 2022-02-25 · **Updated:** 2024-06-20
- **Reactions:** 0
- **Labels:** `a: text input, framework, f: material design, a: desktop, has reproducible steps, P2, found in release: 2.10, found in release: 2.11, team-text-input, triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Skia text layout on desktop/macOS does not wrap trailing whitespaces to a new line in a multiline `TextField`.

**Why engine-level.** Skia-level text layout behavior.

**Dedup scan.** Relates to RTL-TR-1 but concerns line wrapping of whitespace rather than text alignment rendering.

### #110470 —   canvas.drawLine() does not paint correctly on Samsung Galaxy Note 20 Ultra

- **URL:** https://github.com/flutter/flutter/issues/110470
- **Created:** 2022-08-29 · **Updated:** 2024-09-26
- **Reactions:** 0
- **Labels:** `a: text input, e: device-specific, platform-android, framework, engine, f: material design, dependency: skia, c: rendering, P2, e: samsung, team-android, triaged-android, found in release: 3.19`
- **Ownership:** `team-android`
- **Decision:** **skip — engine-level**

**Root cause.** Rendering defect in Skia's `drawLine` on older Samsung Android hardware.

**Why engine-level.** Hardware-specific Skia rendering bug.

**Dedup scan.** No duplicates.

### #113228 — Provide an API to detect if a TextPosition is located at a soft word wrap

- **URL:** https://github.com/flutter/flutter/issues/113228
- **Created:** 2022-10-10 · **Updated:** 2024-03-06
- **Reactions:** 0
- **Labels:** `a: text input, c: new feature, platform-ios, framework, c: proposal, P3, team-design, triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal**

**Root cause.** Request for an API (likely on `RenderEditable`) to determine if a `TextPosition` is at a soft wrap.

**Why feature/proposal.** New API request.

**Dedup scan.** No duplicates.

### #119684 — Extending to paragraph/or word boundary on MacOS should default to the `downstream` position when at a word wrap

- **URL:** https://github.com/flutter/flutter/issues/119684
- **Created:** 2023-02-01 · **Updated:** 2024-06-06
- **Reactions:** 0
- **Labels:** `a: text input, framework, platform-macos, P2, team-text-input, triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** When extending selection to a word/paragraph boundary on macOS, if the caret is at a soft wrap, the framework should default to the downstream position.

**Why feature/proposal.** Proposal to change the default caret affinity/position logic for specific keyboard shortcuts.

**Dedup scan.** No duplicates.

### #139443 — [Windows] Incorrect character deletion in right-to-left texts

- **URL:** https://github.com/flutter/flutter/issues/139443
- **Created:** 2023-12-03 · **Updated:** 2025-08-21
- **Reactions:** 0
- **Labels:** `a: text input, framework, a: internationalization, platform-windows, has reproducible steps, P3, found in release: 3.16, found in release: 3.18, team-text-input, triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** CRLF (`\r\n`) line endings from manual typing on Windows cause incorrect cursor offset reporting in RTL text, breaking character deletion.

**Why engine-level.** Caret placement and boundaries around `\r` and CRLF are reported by engine `SkParagraph`.

**Dedup scan.** Shares root cause with #93934. Added to cluster CRLF-1.

### #144759 — Arrow key navigation gets stuck at the end of RTL text using Samsung Keyboard

- **URL:** https://github.com/flutter/flutter/issues/144759
- **Created:** 2024-03-07 · **Updated:** 2024-03-07
- **Reactions:** 0
- **Labels:** `a: text input, framework, a: internationalization, has reproducible steps, P2, found in release: 3.19, team-text-input, triaged-text-input, found in release: 3.21`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Samsung keyboard uses visual order for arrow keys, but Flutter relies on logical order. When cursor is logically at the end but visually on the left, the left arrow is ignored.

**Why feature/proposal.** Architectural gap: visual vs logical order traversal in Flutter framework/engine.

**Dedup scan.** Relates to #78660. Added to cluster RTL-NAV-1.

### #155919 — Error where possible null is being asserted in rendering paragraph

- **URL:** https://github.com/flutter/flutter/issues/155919
- **Created:** 2024-09-30 · **Updated:** 2024-10-23
- **Reactions:** 0
- **Labels:** `framework, a: error message, P2, team-text-input, triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **likely-stale (signal-based)**

**Root cause.** `RenderParagraph.text` null assertion occurs when a `Row` child with `Expanded` wrapping a `Text` widget has its `BoxConstraints` width collapse to 0.

**Dedup scan.** No duplicates in this category.

### #165204 — Unicode characters not being rendered correctly in goldens test

- **URL:** https://github.com/flutter/flutter/issues/165204
- **Created:** 2025-03-14 · **Updated:** 2025-03-27
- **Reactions:** 0
- **Labels:** `a: tests, a: text input, framework, has reproducible steps, P3, team-text-input, triaged-text-input, found in release: 3.29, found in release: 3.31`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** The Ahem font used by default in goldens doesn't contain U+25CF (bullet), rendering a tofu box.

**Why feature/proposal.** Not a product bug; user issue with test font missing a character.

**Dedup scan.** No duplicates.

### #167466 — Ellipsis not working properly when a text overflows via constrained height instead of max lines

- **URL:** https://github.com/flutter/flutter/issues/167466
- **Created:** 2025-04-21 · **Updated:** 2025-12-21
- **Reactions:** 0
- **Labels:** `framework, a: typography, c: rendering, has reproducible steps, P2, team-text-input, triaged-text-input, found in release: 3.29, found in release: 3.32`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Ellipsis is not shown when text is clipped by a constrained parent height rather than by `maxLines`.

**Why engine-level.** Text layout and ellipsis rendering geometry lives in `SkParagraph`.

**Dedup scan.** No duplicates.

### #177408 — The framework should provide a mechanism to change the paragraph spacing of text

- **URL:** https://github.com/flutter/flutter/issues/177408
- **Created:** 2025-10-22 · **Updated:** 2026-01-06
- **Reactions:** 0
- **Labels:** `a: text input, c: new feature, a: accessibility, P3, team-text-input, triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** There is no mechanism to change the paragraph spacing of text in the framework (`TextStyle` `paragraphSpacing`).

**Why feature/proposal.** Feature request for new typographic API.

**Dedup scan.** Relates to #36854, #177953. Included in cluster TYPO-PARA-1.

### #177953 — The framework should apply `paragraphSpacingOverride` to its text

- **URL:** https://github.com/flutter/flutter/issues/177953
- **Created:** 2025-11-03 · **Updated:** 2026-01-02
- **Reactions:** 0
- **Labels:** `a: text input, c: new feature, a: accessibility, platform-web, P3, team-text-input, triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** The framework should apply `paragraphSpacingOverride` to its text.

**Why feature/proposal.** Feature request for new typographic API.

**Dedup scan.** Relates to #36854, #177408. Included in cluster TYPO-PARA-1.

### #183571 — iOS: NSJSONSerialization crash when deleting SMP characters

- **URL:** https://github.com/flutter/flutter/issues/183571
- **Created:** 2026-03-12 · **Updated:** 2026-03-19
- **Reactions:** 0
- **Labels:** `a: text input, platform-ios, P1, team-text-input, triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** When deleting SMP characters on iOS, the text input system leaves orphaned UTF-16 surrogates in the NSString. This causes NSJSONSerialization to fail.

**Why engine-level.** Engine-level bug in iOS text input handling and serialization (`FlutterCodecs.mm`).

**Dedup scan.** Shares JSON serialization crash due to surrogate pairs with #181759. Added to cluster SURR-1.

## Duplicate clusters

- **RTL-TR-1** (Trailing space trimmed on right/center align): Canonical #40648, includes #90058, #86668.
- **RTL-SEL-1** (Incorrect RTL selection geometry in SkParagraph): Includes #39755, #117139, #174689.
- **RTL-OBS-1** (RTL obscureText order bug): Canonical #71318 (watch for #47745, #50098, #54099 in future batches).
- **RTL-LINE-1** (LineMetrics/caret navigation needs): Includes #91010, #75572.
- **RTL-NAV-1** (Visual vs logical order traversal): Includes #78660, #144759.
- **CRLF-1** (CRLF \r cursor boundaries on desktop): Includes #93934, #139443.
- **SURR-1** (Surrogate pair JSON serialization crash in embedder): Includes #181759, #183571.
- **TYPO-PARA-1** (Paragraph spacing API request): Includes #36854, #177408, #177953.
