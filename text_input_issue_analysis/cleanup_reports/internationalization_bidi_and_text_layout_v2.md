# Internationalization, BiDi, and text layout Cleanup Report (v2)

Independent re-audit of the *Internationalization, BiDi, and text layout*
category — 44 open issues from the 2026-04-17 snapshot of
`text_input_issues.json`. Authored without consulting the v1 cleanup
report or v1 regression tests for this category, so this is a clean
second pass.

Snapshot: `text_input_issues.json` (last_refreshed 2026-04-17).
Workflow: [`CLEANUP_REPORT_FORMAT.md`](../CLEANUP_REPORT_FORMAT.md).
Order: reactions descending; ties broken by `updated_at` descending.
Scope note: per the user's standing direction for this re-audit, RTL
issues currently classified into other categories (Cursor, Selection,
SelectableText) are **not** absorbed into this report — only the 44
issues whose `category` is exactly *"Internationalization, BiDi, and
text layout"* are processed here.

## Running summary

- Processed: 44 / 44
- Tests written: 3
  - Failed as expected: 2
  - Pass-green, exercises bug path: 0
  - Pass-green, does not exercise bug path: 1
  - Test error: 0
- skip — feature/proposal: 19
- skip — engine-level: 14
- skip — needs native-platform verification: 0
- likely-stale (signal-based): 5
- likely-duplicate: 3
- Duplicate clusters (tentative): 6 (TWA-1, PS-1, VKN-1, LM-1, SK-RECT-1, CRLF-W-1)
- Cross-category sibling/split-issue links: 0

## Decision types

| Decision | Meaning |
|---|---|
| `write-test` | Framework-level `testWidgets`/`test` feasible. Author it, run it, record outcome. Sub-outcomes: `fail-as-expected`, `pass-green, exercises bug path`, `pass-green, does not exercise the real bug path`, `test-error`. |
| `skip — feature/proposal` | `c: proposal` / `c: new feature` / architectural request. No regression surface. |
| `skip — engine-level` | Fix lives in the engine/embedder; no framework vantage point reaches the bug. Optional framework gate may be useful as future guard. |
| `skip — needs native-platform verification` | Framework-testable in principle, but expected behavior requires a current native reference we don't have. Deferred. |
| `likely-stale (signal-based)` | Framework testing not feasible; age + inactivity + framework evolution since filing strongly suggest the issue is no longer valid. |
| `likely-duplicate` | Same root cause as another in-category issue. Canonical identified; merge recommended. |

## Processed issues

<!-- Append `### #<number> — <title>` blocks below, in reactions-desc order. -->

### #61069 — [proposal] ability to change text overflow on the TextField

- **URL:** https://github.com/flutter/flutter/issues/61069
- **Created:** 2020-07-08 (~5.8 y old) · **Updated:** 2025-07-18
- **Reactions:** 65 (👍 65)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `c: proposal`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** `TextField` lacks an `overflow` parameter analogous to `Text.overflow`, so input text exceeding a single-line width is hard-clipped with no way to render an ellipsis or fade. The thread is overwhelmingly me-too / bumps; one substantive comment links DevTools work and notes @LongCatIsLooong was looking at overflow ellipsis. Workarounds: the third-party `auto_size_text_field` package, or a manual `TextPainter` ellipsis.

**Why skip-proposal.** Pure additive API request. Labeled `c: proposal` + `c: new feature`. There is no current observable misbehavior to gate via a regression test — the field intentionally does not support overflow.

**Dedup scan.** Searched `overflow`, `ellipsis` in titles/bodies/summaries within the category. Only #167466 hit (ellipsis under constrained height for `Text`, not `TextField` overflow API). No in-category duplicate.

### #51258 — Need to find how much of a long word could fit in one line before an unnatural line break

- **URL:** https://github.com/flutter/flutter/issues/51258
- **Created:** 2020-02-22 (~6.2 y old) · **Updated:** 2023-07-08
- **Reactions:** 28 (👍 24, 👀 4)
- **Labels:** `a: text input`, `framework`, `a: typography`, `c: proposal`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** Custom non-rectangular text layouts (referenced via #35994) need to know how many characters of an unbreakable run will fit in a given line width. There is no public per-character cumulative-advance API on `Paragraph`/`TextPainter`, and the body notes scripts like Mongolian and Arabic use context-dependent glyph sizing so naive sum-of-character-widths is wrong. No comment summary; body is the authoritative description.

**Why skip-proposal.** Asks for a new public measurement primitive. Labeled `c: proposal`. No current bug surface to gate.

**Dedup scan.** Searched `unnatural`, `measure long word`, `word.*break`. No in-category duplicates. Adjacent: #71083 (engine wrapping algorithm) and #91010 (`LineMetrics` line-boundary completeness) overlap thematically with text-measurement gaps but are distinct surfaces.

### #77023 — [Web] [CanvasKit][Feature Request]: Load fonts as soon as detecting browser locale

- **URL:** https://github.com/flutter/flutter/issues/77023
- **Created:** 2021-03-02 (~5.2 y old) · **Updated:** 2025-10-30
- **Reactions:** 21 (👍 17, 👀 4)
- **Labels:** `a: text input`, `c: new feature`, `a: internationalization`, `a: typography`, `platform-web`, `c: proposal`, `c: rendering`, `e: web_canvaskit`, `P2`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level**

**Root cause.** CanvasKit downloads fallback CJK / RTL fonts on demand only after the user types the first character that the bundled font cannot render, producing brief tofu/gibberish until the network fetch completes. The same flicker reproduces on Hebrew, Arabic, and Korean. Persists through 3.32.4 / current Wasm build. The HTML renderer (now removed) and bundling a custom font both hide the symptom.

**Layer check (C1).** Comments name CanvasKit and the web font-loading pipeline. Fix surface is `engine/lib/web_ui/lib/src/engine/canvaskit/font_fallback*` — web-engine concern.

**Why skip-engine.** Web-engine font-fallback prefetching by browser-reported locale belongs to the web UI engine. The framework does not see the font-load pipeline. Recent comments propose system-font query and inter-session caching — both engine-side architecture work.

**Dedup scan.** Searched `canvaskit`, `fallback font`, `tofu`, `browser locale`. Only #165204 hits (Unicode goldens-rendering test — different scenario). No in-category duplicate.

### #34610 — Mixing RTL and LTR text bugs

- **URL:** https://github.com/flutter/flutter/issues/34610
- **Created:** 2019-06-17 (~6.9 y old) · **Updated:** 2024-03-06
- **Reactions:** 18 (👍 14, 👀 3, 🚀 1)
- **Labels:** `a: text input`, `framework`, `engine`, `a: typography`, `customer: crowd`, `P2`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — engine-level**

**Root cause.** Comment 0 (engine team) attributes the symptoms to `ParagraphStyle.direction` being LTR for paragraphs that mix LTR + RTL runs, so a typed space lands at the wrong logical end of an Arabic span. Comment 2 explicitly defers the work to the SkParagraph migration (#39420). Subsequent reports confirm caret positioning improved post-engine PR `flutter/engine#9489`, but cross-direction deletion (typing Arabic, switching keyboard to Chinese, hitting Backspace) still fails.

**Layer check (C1).** Direct hits: `ParagraphStyle`, `SkParagraph`, `flutter/engine` PR reference. Engine layer.

**Why skip-engine.** Paragraph direction synthesis for mixed-script inputs and IME-coordinated deletion across direction boundaries are both engine + embedder concerns. The framework owns the keystroke-to-edit pipeline, but the deletion semantics that fail here come from how the embedder reports composing-region replacements during keyboard switches.

**Dedup scan.** Searched `mixing`, `mixed`, `rtl and ltr`, `opposite direction`. No in-category duplicates by symptom. Adjacent: #181759 (RTL + emoji insertion) shares the "RTL + supplementary char" surface but differs in root cause (emoji-cluster handling) — see batch 2.

### #40648 — Trailing space doesn't work with TextField with TextAlign.right

- **URL:** https://github.com/flutter/flutter/issues/40648
- **Created:** 2019-09-17 (~6.6 y old) · **Updated:** 2025-01-29
- **Reactions:** 16 (👍 16)
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.5`, `found in release: 2.6`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause.** With `TextAlign.right`, a trailing space is visually trimmed from the rendered glyph run and the caret cannot advance past the start of the trimmed region. Comment 8 cites an upstream Skia bug, `bugs.chromium.org/p/skia/issues/detail?id=11933`, filed and accepted. One commenter notes SkParagraph treats `\r` with `CodeUnitFlag 0x0006` similarly. Reproduces on stable 3.27.2 (Jan 2025) — bug is current.

**Layer check (C1).** Multiple comments cite Skia / SkParagraph and an upstream Skia tracker; the trim happens in SkParagraph's line-end whitespace handling for non-`left` alignment.

**Why skip-engine.** Fix lives in Skia's paragraph layout. The framework's caret rect comes from `Paragraph.getBoxesForRange`/`getOffsetForCaret`; once Skia stops trimming the trailing whitespace from the right-aligned run, the caret naturally lands correctly. A framework gate could compute an expected caret rect via `TextPainter` and check the trailing space contributes to width, but that test would just mirror the engine output and would not catch any framework regression.

**Cluster.** Canonical of **TWA-1** (Trailing Whitespace under TextAlign.right). Members: #40648 (this issue, R=16), #86668 (R=1, see batch 2), #90058 (R=6, dup, this batch).

**Dedup scan.** Searched `trailing space`, `trailing whitespace`, `textalign.right`. Direct hits: #86668 and #90058 (both same root cause). Adjacent (different scenarios): #99139 (multiline overflow trailing-whitespace), #174689 (selection highlight on trailing whitespace), #92507 ("ghost run" + `getBoxesForRange` documentation — same Skia surface but distinct symptom).

### #78660 — Arrow keys in RTL move the wrong way

- **URL:** https://github.com/flutter/flutter/issues/78660
- **Created:** 2021-03-19 (~5.1 y old) · **Updated:** 2024-03-06
- **Reactions:** 15 (👍 15)
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 2.1`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **write-test** → **fail-as-expected**

**Root cause.** `default_text_editing_shortcuts.dart:191-198` binds `LogicalKeyboardKey.arrowRight` to `ExtendSelectionByCharacterIntent(forward: true)` and `arrowLeft` to `forward: false`. "Forward" is logical (toward higher offset). In an RTL paragraph, ArrowRight therefore advances the caret toward higher offsets, rendering as a *visually leftward* movement. Comment 9 confirms visual-order traversal is "planned but not implemented"; comment 8 sketches extending the Intent system with an explicit left/right flag.

**Test approach.**
  - Pump a `MaterialApp` with `Directionality(textDirection: TextDirection.rtl)` wrapping a `TextField` containing the four-glyph Arabic word `'شسيب'` (logical: ش=0, س=1, ي=2, ب=3; visually right-to-left).
  - Place caret at offset 2 (between ي and ب).
  - Send `LogicalKeyboardKey.arrowRight`.
  - Assert `controller.selection.baseOffset < 2`. Visual-right semantics in RTL means the offset should *decrease* (toward 'ش' on the visual right edge of the line).

**Test:** [`issue_78660_rtl_arrow_keys_test.dart`](../regression_tests/internationalization_bidi_and_text_layout_v2/issue_78660_rtl_arrow_keys_test.dart)

**Test outcome.** Fails as expected: `Expected: a value less than <2>; Actual: <3>`. ArrowRight advanced the caret to logical offset 3 (visually toward ب on the left edge), demonstrating the bug. Sub-outcome: **fail-as-expected**. The test will start passing once visual-order arrow navigation lands.

**Cluster.** Canonical of **VKN-1** (Visual Keyboard Navigation in RTL). Members: #78660 (this issue, framework Intent definition) + weak #54998 (defaults policy proposal). #144759 (Samsung-keyboard RTL-end stuck) is engine/embedder-side and likely not part of the same cluster.

**Dedup scan.** Searched `arrow key`, `visual order`, `directional`. Surfaces #54998 and #144759 (both batch 4). Neither shares root cause with #78660 directly, but the directional-key Intent system underlies all three; recorded under VKN-1.

### #36854 — Feature request: Setting paragraph distance in Text and TextField

- **URL:** https://github.com/flutter/flutter/issues/36854
- **Created:** 2019-07-24 (~6.8 y old) · **Updated:** 2024-03-06
- **Reactions:** 12 (👍 12)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `a: typography`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** Body asks for control over inter-paragraph distance in `Text`/`TextField`. No comment summary. Strict feature request.

**Why skip-proposal.** Same surface area is re-filed more concretely in #177408 / #177953 ("`paragraphSpacingOverride`"). Nothing currently observable to regress against.

**Cluster.** Canonical of **PS-1** (Paragraph Spacing API). Members: #36854 (this issue, oldest framing) + #177408 + #177953 (both batch 3, more concrete API names).

**Dedup scan.** Direct hits on `paragraph spac` / `paragraphspac` / `paragraph distance` — #177408, #177953. All three are restatements of the same gap.

### #39755 — Selection of any justified-text is inaccurate in non-latin languages

- **URL:** https://github.com/flutter/flutter/issues/39755
- **Created:** 2019-09-03 (~6.6 y old) · **Updated:** 2024-03-06
- **Reactions:** 10 (👍 9, 👀 1)
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause.** Selection rect highlights are drawn beyond actual glyph bounds when justifying non-Latin runs (Korean / Arabic / Hebrew / Persian). Comment 2 (engine team) hypothesizes LibTxt is mishandling `justification_x_offset` per code-unit run for scripts where a space starts a new run. Comments 7 and 13 confirm the artifact *vanishes* when an appropriate-script font is loaded (Amiri for Arabic), strongly implicating font-shape / justification interaction in paragraph layout, not framework selection geometry. Mixed Latin+RTL still misbehaves even with a proper font.

**Layer check (C1).** Direct hits: LibTxt, `justification_x_offset`. Engine layer.

**Why skip-engine.** `RenderEditable.getRectsForSelection` queries `Paragraph.getBoxesForRange`. If those boxes overshoot the actual glyph run (because justification expanded space-runs incorrectly), the framework just paints what the engine returned. Fix has to be in paragraph-layout justification.

**Dedup scan.** Searched `justif`, `inaccurate.*selection`. No in-category duplicate. Cross-category sibling: #175983 ("[iOS & Android] Wrong selection for wrapped Arabic text in `SelectableText`") sits in *SelectableText / SelectionArea / SelectableRegion* and likely shares the same engine surface — out-of-scope per user direction.

### #90058 — TextFormField with textAlign: TextAlign.right whitespace doesn't show unless text is entered

- **URL:** https://github.com/flutter/flutter/issues/90058
- **Created:** 2021-09-14 (~4.6 y old) · **Updated:** 2025-08-13
- **Reactions:** 6 (👍 6)
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.5`, `found in release: 2.6`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **likely-duplicate** (canonical: #40648)

**Root cause.** Same Skia trailing-whitespace trimming under `TextAlign.right` as #40648. Reproduces on web / macOS / Android / Windows. Filed two years after #40648 with a smaller follow-up reaction count.

**Why likely-duplicate.** Identical reproduction (TextField + `TextAlign.right` + trailing space → no rendered space, cursor stuck), identical workaround pattern (transparent overlay hack). #40648 has earlier filing date, the upstream Skia bug ID, and a richer comment thread — preferred canonical.

**Cluster.** Member of **TWA-1**. See #40648 entry for cluster definition.

**Dedup scan.** Same scope as #40648; this is the duplicate to merge.

### #71083 — TextFormField (and TextField) widgets do not wrap text correctly

- **URL:** https://github.com/flutter/flutter/issues/71083
- **Created:** 2020-11-23 (~5.4 y old) · **Updated:** 2024-03-06
- **Reactions:** 5 (👍 5)
- **Labels:** `a: text input`, `framework`, `f: material design`, `dependency: skia`, `a: typography`, `P2`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause.** `TextField` wraps long unbreakable runs at the *previous* word boundary, leaving the line short rather than character-breaking inside the run as browsers do. Body explicitly contrasts the Flutter screenshot with Chrome's correct behavior on the same long URL. The `dependency: skia` label is direct — this is SkParagraph line-breaking behavior; the engine does not implement a fall-back to character-break when no breakable opportunity exists in the line.

**Layer check (C1).** Label `dependency: skia` and explicit Chrome-vs-Flutter contrast. Engine layer.

**Why skip-engine.** Line-break decisions live in the engine's `Paragraph` layout. The framework supplies `softWrap` / `maxLines` and consumes the resulting line break offsets; it cannot retroactively split a glyph run that the engine returned as a single block.

**Dedup scan.** Searched `wrap.*long`, `word boundary`, `line break.*url`. No in-category duplicate. Weak hit #119684 is about caret-extension `downstream` default on macOS (different surface).

### #91738 — [Proposal] Add support for automatically switching text input to `RTL` or `LTR` based on first character typed

- **URL:** https://github.com/flutter/flutter/issues/91738
- **Created:** 2021-10-13 (~4.5 y old) · **Updated:** 2023-09-15
- **Reactions:** 5 (👍 4, ❤️ 1)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `a: internationalization`, `c: proposal`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** Asks for `dir="auto"`-style behavior on `TextField` so the first typed character chooses the run direction (mirrors WhatsApp / browser behavior). Comments note Flutter's `intl` package has a `Bidi` class and ICU exposes `ubidi_getBaseDirection`; the proposed implementation is a `TextDirection.auto` (or sentinel) that `EditableText` resolves on first character.

**Why skip-proposal.** Pure additive API. Labeled `c: proposal` + `c: new feature`. No current behavior to gate.

**Dedup scan.** Searched `auto`, `first character`, `direction switching` — no in-category duplicates.

### #91010 — `dart:ui.LineMetrics` should include the line boundaries

- **URL:** https://github.com/flutter/flutter/issues/91010
- **Created:** 2021-09-30 (~4.6 y old) · **Updated:** 2023-09-19
- **Reactions:** 4 (👍 3, 👀 1)
- **Labels:** `a: text input`, `engine`, `a: typography`, `c: proposal`, `P3`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — feature/proposal**

**Root cause.** `dart:ui.LineMetrics` deliberately strips the SkParagraph `Metrics.h` text-range fields. The body links to a TODO in `flutter/flutter#90684` for vertical caret movement that would benefit from explicit per-line `TextRange`. Today callers approximate by calling `Paragraph.getPositionForOffset` for each line edge.

**Layer check (C1).** Body cites `skia/modules/skparagraph/include/Metrics.h` and the engine API surface. Engine layer.

**Why skip-proposal.** The bug is the absence of a public field on `LineMetrics`; both implementations (engine `dart:ui` and bridge to Skia) need to be extended. Tagged `c: proposal` and `team-engine`. Nothing observable to regress against — adding the field is purely additive.

**Dedup scan.** Searched `LineMetrics`, `line boundaries`, `TextRange.*line`. Adjacent: #75572 ("Let RenderEditable use LineMetrics instead of assuming every line has the same height") consumes line metrics and shares the broader theme, but is a different concern. #133930 is a similar API-gap proposal for line metrics on `Text`/`TextField`. All three are recorded under cluster **LM-1** (Line Metrics API gaps); see batches 3 and 4 for the other members.

### #41324 — TextField/TextFormField labelText and hintText should be right-aligned with TextDirection.rtl

- **URL:** https://github.com/flutter/flutter/issues/41324
- **Created:** 2019-09-25 (~6.6 y old) · **Updated:** 2026-02-16
- **Reactions:** 3 (👍 3)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `a: internationalization`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **write-test** → **fail-as-expected**

**Root cause.** When `textDirection: TextDirection.rtl` is set on a `TextField` directly (rather than via a surrounding `Directionality`), the `InputDecoration.labelText` is rendered left-aligned within the field. The framework already has an explicit M3 RTL label-position assertion at `test/material/input_decorator_test.dart:2331-2345` — but that test pumps with `buildInputDecorator(textDirection: TextDirection.rtl)`, which threads the direction down via `Directionality`. The bug is that the field-level `textDirection` parameter does not reach `InputDecorator`'s label-position resolution. Recent activity (2026-02-16) confirms the issue is current.

**Test approach.**
  - Pump a `TextField` inside an LTR-default `MaterialApp`, with `textDirection: TextDirection.rtl` set on the `TextField` itself.
  - `decoration: InputDecoration(labelText: 'Email', hintText: 'hint')`.
  - Locate the rendered label via `find.text('Email')` and the field via `find.byType(TextField)`.
  - Assert label.right is within ~40 px of field.right (i.e. label is right-aligned), and that label.right is closer to field.right than label.left is to field.left.

**Test:** [`issue_41324_rtl_input_decoration_label_test.dart`](../regression_tests/internationalization_bidi_and_text_layout_v2/issue_41324_rtl_input_decoration_label_test.dart)

**Test outcome.** Fails as expected: `rightEdgeDelta=217.5` (label sits flush with the field's *left* edge, not its right edge). `labelRect=Rect.fromLTRB(250, 292, 332.5, 308)`, `fieldRect=Rect.fromLTRB(250, 272, 550, 328)`. Sub-outcome: **fail-as-expected**. The fix surface is `InputDecorator` — make it consult the effective `textDirection` of the inner `TextField`/`EditableText` rather than only the ambient `Directionality`.

**Dedup scan.** Searched `labelText`, `hintText`, `InputDecoration.*rtl`. No in-category duplicates. Adjacent: #78864 in this batch ("Text does not draw correctly based on text direction") shares the "directionality-not-honored" theme but the symptom is BiDi reordering of `06 PM`-style mixed-script strings — different surface.

### #181759 — RTL TextField breaks when inserting emojis between existing emojis

- **URL:** https://github.com/flutter/flutter/issues/181759
- **Created:** 2026-01-31 (~0.2 y old) · **Updated:** 2026-03-06
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `platform-android`, `framework`, `f: material design`, `platform-macos`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Per the comment summary: on macOS / Linux, dynamically changing `textDirection` mid-IME-composition triggers a `wstring_convert::to_bytes` exception in the engine (built with `-fno-exceptions`), causing an abort. On Android, the IME composing state is invalidated, producing `?` replacement characters. iOS / web don't repro. A linked tracker (#183112) explicitly states the fix lives in each affected embedder (macOS, Linux), not the framework.

**Layer check (C1).** Comments cite `wstring_convert`, abort traces, and per-embedder fix surfaces — embedder layer.

**Why skip-engine.** The fix path is entirely in the macOS / Linux text-input plugins and engine BiDi-aware composing state machinery. The framework's role here is just to forward the new `textDirection` and the inserted emoji bytes — both correct.

**Dedup scan.** Searched `emoji`, `composing.*rtl`, `embedder.*abort`. Only direct hit; no in-category duplicates.

### #93934 — [Desktop] TextField with pasted CRLF endings has invisible CR char

- **URL:** https://github.com/flutter/flutter/issues/93934
- **Created:** 2021-11-19 (~4.4 y old) · **Updated:** 2024-06-07
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `framework`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.5`, `found in release: 2.6`, `found in release: 2.8`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **skip — engine-level**

**Root cause.** Pasting CRLF-terminated text into a desktop `TextField` leaves the `\r` character in the buffer; the caret skips it but it remains stored. Reproduces on Windows and macOS desktop (per a follow-up comment), not on web. Native desktop apps (TextEdit, Notepad) normalize CRLF → LF on paste; Flutter does not.

**Layer check (C1).** No explicit engine class names, but the symptom is platform-clipboard-specific. The Windows embedder's `Clipboard` channel returns the raw clipboard string verbatim. SkParagraph treats `\r` with `CodeUnitFlag 0x0006` (cited in #40648 raw comments), giving it line-break semantics in layout but not removing it.

**Why skip-engine.** CRLF normalization is most naturally done in the desktop embedder's clipboard reader (or in `Clipboard.getData` in `dart:ui` if we want it cross-platform). The framework's `TextField` paste handler just inserts whatever the channel returns. Filing-team `team-windows` reflects that the embedder is the natural fix-point.

**Dedup scan.** Searched `crlf`, `\\r`, `clipboard`, `paste.*line ending`. No in-category duplicates.

### #117139 — Incorrect selection area in RTL TextField

- **URL:** https://github.com/flutter/flutter/issues/117139
- **Created:** 2022-12-15 (~3.4 y old) · **Updated:** 2023-07-08
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause.** Double-clicking a word in an RTL multi-line `TextField` whose first line ends with `.` (followed by a newline) draws a selection rect that extends beyond the word boundaries. Per summary: "Root cause identified: Skia SkParagraph's `getRectsForRange` API; a Skia bug was filed at `bugs.chromium.org/p/skia/issues/detail?id=14035`."

**Layer check (C1).** Skia, SkParagraph, `getRectsForRange` — engine layer.

**Why skip-engine.** Same situation as #39755: selection-rect drawing is downstream of `Paragraph.getRectsForRange`. The fix is in Skia's range-rect computation for RTL runs that abut a paragraph break.

**Dedup scan.** Searched `selection rect.*rtl`, `getRectsForRange`. Adjacent: #39755 (justified-text selection inaccurate non-Latin) and #34610 (mixed RTL/LTR generally) are also `getRectsForRange`-adjacent engine surfaces. All three share **SK-RECT-1** (Skia getRectsForRange RTL/non-Latin geometry) tentative cross-issue cluster.

### #184240 — Vertical baseline alignment mismatch between Text and collapsed TextField when changing TextLeadingDistribution

- **URL:** https://github.com/flutter/flutter/issues/184240
- **Created:** 2026-03-27 (~0.1 y old) · **Updated:** 2026-04-02
- **Reactions:** 1 (❤️ 1)
- **Labels:** `framework`, `f: material design`, `has reproducible steps`, `team-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **write-test** → **pass-green, does not exercise the real bug path**

**Root cause.** Reporter places a `Text` and a `TextField(decoration: InputDecoration.collapsed())` with the same `TextStyle` (specifically same `fontSize`, `height`, `textBaseline`, `leadingDistribution`) into a `Row` and observes the TextField rendering visibly higher or lower than the Text depending on the `leadingDistribution` value. Issue is recent (2026-03-27) and routed to @LongCatIsLooong; explicitly notes related bug #144502.

**Test approach.**
  - Pump a baseline-aligned `Row` with `Text('X', style)` and `TextField` containing 'X' with the same style.
  - Run for both `TextLeadingDistribution.proportional` and `TextLeadingDistribution.even`.
  - Assert (a) the visible glyph bottoms agree to within 2 px (baseline parity), and (b) the rendered widget heights agree to within 2 px (intrinsic-vertical-extent parity).

**Test:** [`issue_184240_baseline_text_vs_textfield_test.dart`](../regression_tests/internationalization_bidi_and_text_layout_v2/issue_184240_baseline_text_vs_textfield_test.dart)

**Test outcome.** Both variants pass under the test font (Ahem). Sub-outcome: **pass-green, does not exercise the real bug path**. The reporter's repro likely depends on a font whose ascender / descender metrics differ from Ahem's box-uniform shape, or on a content string with descenders, neither of which the default test font exposes. The test is retained as a framework gate against any future regression in baseline / height parity between `Text` and collapsed `TextField` for identical styles.

**Dedup scan.** Searched `baseline`, `leadingDistribution`, `collapsed.*TextField`. No in-category duplicates. Body explicitly cross-references #144502 (Material) which is out-of-category.

### #174689 — App highlights / selects trailing whitespaces in a multi-line textfield

- **URL:** https://github.com/flutter/flutter/issues/174689
- **Created:** 2025-08-29 (~0.7 y old) · **Updated:** 2025-09-18
- **Reactions:** 1 (👀 1)
- **Labels:** `a: text input`, `platform-android`, `platform-ios`, `a: desktop`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.35`, `found in release: 3.36`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Selecting a word at the end of a multi-line `TextField` includes the trailing whitespace in the highlight rect, even though native Android / iOS apps stop the selection at the word boundary. Reproduces on Android / iOS / desktop, not web. `maxLines: null` (or `minLines`) is required. Per summary, root cause not identified; routed to @LongCatIsLooong.

**Layer check (C1).** Symptom is a *selection rect* that extends past the word — same `getRectsForRange`/`getBoxesForRange` family as #117139 and #39755. The framework's `RenderEditable` queries Skia for the rects of the current selection; if Skia's range-rect computation grows the rect to the end of the run when the run ends in whitespace, the framework just paints what's returned.

**Why skip-engine.** Word-boundary-aware selection rect computation lives in the engine paragraph layout. The framework can choose what range to ask for, but cannot post-trim the returned rect without asserting glyph bounds it doesn't have direct access to.

**Dedup scan.** Searched `trailing whitespace.*select`, `selection.*end of line`. Members of the broader Skia getRectsForRange surface noted under **SK-RECT-1** above. Not a strict duplicate of #40648 (TWA-1) — that bug is about *rendering* the trailing space, this is about *selecting* it.

### #78864 — Text does not draw correctly based on text direction

- **URL:** https://github.com/flutter/flutter/issues/78864
- **Created:** 2021-03-23 (~5.1 y old) · **Updated:** 2025-07-22
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 2.1`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **likely-stale (signal-based)**

**Root cause.** Body claims that formatted date strings `"06 PM"` and `"PM 06"` render identically in some directionality / locale combinations. The "bug" is the standard Unicode BiDi algorithm reordering weak (digits) and neutral (space) characters according to the surrounding strong context — visually, both forms collapse to a canonical visual order. No commenter has framed this as a Flutter bug. Summary: "Comments are limited to a compile error in the original sample and a single confirmation screenshot; no root cause, fix, or additional platform data added beyond what is in the body."

**Why likely-stale.** Five-year-old `f: material design` design-team issue with a single confirming reaction, no triage progress, and a symptom description that is more likely correct Unicode bidi behavior misunderstood by the reporter than a Flutter rendering bug. There is no clear failure mode to gate.

**Dedup scan.** Searched `06 PM`, `PM 06`, `bidi.*format`. No in-category duplicates.

### #86668 — TextField doesn't handle trailing space as characters if textAlign is TextAlign.right/TextAlign.center

- **URL:** https://github.com/flutter/flutter/issues/86668
- **Created:** 2021-07-19 (~4.8 y old) · **Updated:** 2024-09-26
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.2`, `found in release: 2.4`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **likely-duplicate** (canonical: #40648)

**Root cause.** Same Skia trailing-whitespace trimming as #40648, with the additional observation that `TextAlign.center` exhibits the same symptom (not just `TextAlign.right`). Confirmed by triage (video provided); no PR.

**Why likely-duplicate.** Identical mechanism to #40648 (TWA-1). The center-align observation is additional evidence for the same root cause — the center-align trim happens for the same reason as right-align: SkParagraph trims trailing whitespace from the visible run for non-`left` alignments. Merge into #40648.

**Cluster.** Member of **TWA-1**. See #40648 entry for cluster definition.

**Dedup scan.** Same scope as #40648 / #90058; this is the third member to merge.

### #133930 — No good way to get line metrics for `Text`/`TextField` based widgets

- **URL:** https://github.com/flutter/flutter/issues/133930
- **Created:** 2023-09-03 (~2.6 y old) · **Updated:** 2024-08-23
- **Reactions:** 1 (👍 1)
- **Labels:** `framework`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.13`, `found in release: 3.14`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Reporter constructs a parallel `TextPainter` to count lines but doesn't apply the same Material-theme-resolved `TextStyle` the `TextField` uses, so widths diverge. @dnfield initially suggested `controller.buildTextSpan(...)` but later confirmed it does not reliably carry the resolved styles. @LongCatIsLooong noted a planned framework API exposing immutable text-layout metrics via a callback (e.g. `onTextLayoutChanged`), but flagged that `TextEditingController` is not the right place to host it because one controller can serve multiple fields with different styles.

**Why skip-proposal.** The reporter's symptom is fixable today by replicating the resolved style; the open issue is the absence of a clean public API. Both ends of the resolution are additive — no current behavior to gate. No `c: proposal` label but the surface is proposal-shaped.

**Cluster.** Member of **LM-1** (Line Metrics API gaps): #91010 (`LineMetrics` line boundaries), #75572 (`RenderEditable` use of `LineMetrics`), #133930 (this issue).

**Dedup scan.** Searched `line metrics`, `computeLineMetrics`, `text layout.*api`. Direct hits #91010 and #75572.

### #71318 — TextField RTL input problem with LTR letters/numbers while obscureText is true

- **URL:** https://github.com/flutter/flutter/issues/71318
- **Created:** 2020-11-27 (~5.4 y old) · **Updated:** 2024-07-11
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `engine`, `f: material design`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause.** With `textDirection: TextDirection.rtl` + `obscureText: true`, typing English characters renders the obscuring `•` glyphs visually *to the left* of the existing run during typing, even though the underlying value (and the value when `obscureText` is later set false) is correct. Reporter explicitly notes the bug only manifests during typing animation; the submitted value is fine. Multiple sibling RTL issues linked: #47745, #50098, #54099. Reproduced through Flutter 3.3.

**Layer check (C1).** Both `framework` and `engine` labels. The visual rendering during typing depends on how `•` (U+2022 BULLET) is classified by Unicode BiDi — neutral characters in an RTL run inherit RTL, making cursor advance visually leftward. The framework's `EditableText` does not synthesize visual cursor position; it relies on the engine's per-frame paragraph layout.

**Why skip-engine.** Mid-IME typing visual position is downstream of paragraph layout's BiDi handling of obscure-char runs. The framework just hands the engine the new text + cursor offset; the engine renders.

**Dedup scan.** Searched `obscureText.*rtl`, `password.*rtl`, `cursor.*direction`. No in-category duplicates beyond the linked siblings (which are not in this category).

### #41641 — [web] Support line height + word spacing in text fields

- **URL:** https://github.com/flutter/flutter/issues/41641
- **Created:** 2019-09-30 (~6.6 y old) · **Updated:** 2024-03-06
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `platform-web`, `P3`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — feature/proposal**

**Root cause.** `TextInput.setStyle` does not include `lineHeight` / `wordSpacing` parameters. The web embedder's editable element therefore can't honor those styles. Empty comment summary; body is one sentence.

**Why skip-proposal.** Pure additive engine-protocol enhancement. Labeled `c: new feature` + `team-web`. No current behavior to gate.

**Dedup scan.** No in-category duplicates.

### #84317 — Share code between RenderParagraph and RenderEditable

- **URL:** https://github.com/flutter/flutter/issues/84317
- **Created:** 2021-06-10 (~4.9 y old) · **Updated:** 2023-07-08
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `a: typography`, `P2`, `c: tech-debt`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** Tech-debt observation that `RenderParagraph` and `RenderEditable` share substantial WidgetSpan-handling logic, and a third candidate (`SelectableText` WidgetSpan support) would compound the duplication. Body proposes inheritance or a mixin. No comment summary.

**Why skip-proposal.** `c: tech-debt` refactor proposal. No user-visible bug to gate; the right outcome is a code restructure.

**Dedup scan.** No in-category duplicates.

### #103705 — letterSpacing in TextField with monospace font is only applied to the right side of the first character until a second character is entered, then letterSpacing is applied correctly to both sides

- **URL:** https://github.com/flutter/flutter/issues/103705
- **Created:** 2022-05-13 (~4.0 y old) · **Updated:** 2023-07-08
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `engine`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.0`, `found in release: 3.1`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **likely-stale (signal-based)**

**Root cause.** First-character letterSpacing was only applied to the right side until a second character was typed. Per summary: a Skia fix was submitted (`skia-review.googlesource.com/c/skia/+/541978`) and merged. A commenter confirmed the bug was fixed; the Flutter issue is open only pending stable promotion.

**Why likely-stale.** Strong staleness signal: fix is upstream and merged; the issue is a tracker remnant. Verify the Flutter stable channel includes the Skia roll containing 541978 (it should — the issue is from May 2022, and Skia 541978 landed not long after; we're now on Flutter 3.32+).

**Dedup scan.** No in-category duplicates. Recommend closing after a quick stable-version check.

### #183571 — iOS: NSJSONSerialization crash when deleting SMP characters

- **URL:** https://github.com/flutter/flutter/issues/183571
- **Created:** 2026-03-12 (~0.1 y old) · **Updated:** 2026-03-19
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-ios`, `P1`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Deleting Supplementary Multilingual Plane characters byte-by-byte on iOS leaves orphaned UTF-16 surrogates in the `NSString` carrying the editing-state JSON, which `NSJSONSerialization` then rejects ("failed to convert to UTF8") and the app crashes. Per summary, a contributor has prepared a fix in `engine/src/flutter/shell/platform/darwin/common/framework/Source/FlutterCodecs.mm` that drops lone surrogates and re-maps cursor indices; PR submission against the monorepo is pending.

**Layer check (C1).** Direct hits: `FlutterCodecs.mm`, `NSJSONSerialization`, `UITextInput.deleteBackward`. iOS embedder layer.

**Why skip-engine.** The fix lives in the iOS embedder's codec layer. The framework's editing-state is correct (string with surrogate pairs); the encoder mishandles them.

**Dedup scan.** No in-category duplicates. Pre-triage note suggests this may overlap with #179727 — out of scope for in-category dedup (C2).

### #75572 — Let RenderEditable use LineMetrics instead of assuming every line has the same height

- **URL:** https://github.com/flutter/flutter/issues/75572
- **Created:** 2021-02-07 (~5.2 y old) · **Updated:** 2026-03-05
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `f: material design`, `P2`, `c: tech-debt`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal**

**Root cause.** `RenderEditable` computes vertical caret movement assuming all lines share a common line height. With variable-height lines (e.g. mixed font sizes via `controller.buildTextSpan`), Up/Down arrow can skip a short line. Body links the offending code at `editable.dart:864-873`; comment 0 sketches the expected "preserve horizontal offset across varying-height lines" behavior.

**Why skip-proposal.** `c: tech-debt` framework refactor: replace the uniform-line-height assumption with `LineMetrics`-aware traversal. Surface depends on the upstream API gap also tracked in #91010 (line boundaries on `LineMetrics`).

**Cluster.** Member of **LM-1**. See #133930 entry for cluster definition.

**Dedup scan.** Searched `LineMetrics`, `vertical caret`, `arrow.*line.*skip`. Direct hits #91010, #133930.

### #177408 — The framework should provide a mechanism to change the paragraph spacing of text

- **URL:** https://github.com/flutter/flutter/issues/177408
- **Created:** 2025-10-22 (~0.5 y old) · **Updated:** 2026-01-06
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `a: accessibility`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Concrete restatement of #36854: add `paragraphSpacing` to `TextStyle` analogous to `letterSpacing` / `wordSpacing`. Use case framed around WCAG accessibility compliance.

**Cluster.** Member of **PS-1** (Paragraph Spacing API). See #36854 entry. #177408 has the most concrete proposed API name (`paragraphSpacing` field on `TextStyle`).

**Dedup scan.** Direct hits #36854 and #177953 (both same theme).

### #177953 — The framework should apply `paragraphSpacingOverride` to its text

- **URL:** https://github.com/flutter/flutter/issues/177953
- **Created:** 2025-11-03 (~0.5 y old) · **Updated:** 2026-01-02
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `a: accessibility`, `platform-web`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Follow-on to #172915, which exposed `MediaQueryData.paragraphSpacingOverride`. This issue asks the framework's own widgets (Material/Cupertino Text-using components) to honor that value — except in cases where it shouldn't apply (buttons, headers, navigation destinations, etc.).

**Cluster.** Member of **PS-1**. See #36854 entry.

**Dedup scan.** Direct hits #36854 and #177408.

### #167466 — Ellipsis not working properly when a text overflows via constrained height instead of max lines

- **URL:** https://github.com/flutter/flutter/issues/167466
- **Created:** 2025-04-21 (~1.0 y old) · **Updated:** 2025-12-21
- **Reactions:** 0
- **Labels:** `framework`, `a: typography`, `c: rendering`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.29`, `found in release: 3.32`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** When `Text` is laid out under a height constraint (via parent), `overflow: TextOverflow.ellipsis` only renders the ellipsis correctly when `maxLines: 1`. With `maxLines: null` it collapses to one line; with `maxLines: large`, no ellipsis appears at all. Comments confirm reproducible on stable 3.29 and master 3.32 across all platforms. One commenter notes "may be working as intended" but acknowledges the workaround (LayoutBuilder + TextPainter to compute fitting lines) is awkward.

**Layer check (C1).** No explicit engine names, but the failing API is `Paragraph.layout(maxLines: ...)`. Skia paragraph-layout accepts a max-lines budget but no height budget. The framework would need to derive the max-lines from the height constraint and the (variable) per-line metrics — which requires the same line-metrics surface tracked in **LM-1**.

**Why skip-engine.** Fundamentally an API gap between framework intent ("ellipsis when this line count exceeds height-derived budget") and engine surface (`maxLines` only). Either Skia must accept a height budget, or the framework must build a height-to-lines pre-pass on top of `LineMetrics`. Either path is engine-adjacent.

**Dedup scan.** Searched `ellipsis`, `overflow.*height`, `constrained height`. Adjacent: #61069 (TextField overflow API request) and #75572 (variable-height lines) — distinct surfaces.

### #139443 — [Windows] Incorrect character deletion in right-to-left texts

- **URL:** https://github.com/flutter/flutter/issues/139443
- **Created:** 2023-12-03 (~2.4 y old) · **Updated:** 2025-08-21
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `platform-windows`, `has reproducible steps`, `P3`, `found in release: 3.16`, `found in release: 3.18`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Manually typed Persian/Farsi text in a multiline `TextField` on Windows: Backspace deletes the wrong-side character. Pasting the same text reproduces correctly. Per summary: caret offset reported by the framework is incorrect for RTL text in multiline mode on Windows when the buffer contains CRLF-style line endings from typed Enter keys; explicitly linked to #140739 and CRLF handling. Workaround: insert `\r\n` instead of `\n` on Enter.

**Layer check (C1).** Reporter says "DO NOT COPY AND PASTE" reproduces only on direct typing → implicates the keystroke path through the Windows embedder. CRLF handling on Windows + RTL multiline is a Windows-`TextInputPlugin` concern.

**Why skip-engine.** Cross-references with #93934 (CRLF clipboard normalization) and the broader CRLF-on-Windows handling. The fix surface is the Windows embedder's per-keystroke editing-state synthesis. The framework just reports the cursor offsets the embedder hands it.

**Cluster.** Tentative cross-issue link to **CRLF-W-1** (CRLF on Windows): #93934 (clipboard paste) + #139443 (manual typing in RTL multiline). Both share the symptom that Windows reports `\r` characters in editing-state where macOS / Linux normalize.

**Dedup scan.** Searched `windows.*rtl`, `crlf`, `\\r.*delete`. Direct hit #93934 (cross-reference noted). No clean in-category duplicate.

### #165204 — Unicode characters not being rendered correctly in goldens test

- **URL:** https://github.com/flutter/flutter/issues/165204
- **Created:** 2025-03-14 (~1.1 y old) · **Updated:** 2025-03-27
- **Reactions:** 0
- **Labels:** `a: tests`, `a: text input`, `framework`, `has reproducible steps`, `P3`, `team-text-input`, `triaged-text-input`, `found in release: 3.29`, `found in release: 3.31`
- **Ownership:** `team-text-input`
- **Decision:** **likely-stale (signal-based)**

**Root cause.** Per summary: "the issue reproduces only in golden tests, not at runtime: the Ahem test font (used by default in `matchesGoldenFile`) does not include the U+25CF bullet character, rendering it as a tofu box." The fix is documented test-infra hygiene: load real fonts via `loadAppFonts()` (or use a different font in the golden).

**Why likely-stale.** Behavior is correct: Ahem is intentionally limited; non-Latin code points are tofu by design. The issue is user expectation, not a Flutter bug. Recommend closing with a doc pointer.

**Dedup scan.** No in-category duplicates.

### #33858 — Unicode input should be indicated

- **URL:** https://github.com/flutter/flutter/issues/33858
- **Created:** 2019-06-04 (~6.9 y old) · **Updated:** 2024-12-13
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `platform-windows`, `platform-linux`, `a: desktop`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** On Linux, Ctrl+Shift+U triggers an OS-level Unicode-input mode shown as an underlined "u" in native fields. Flutter accepts the keystrokes (the resulting Unicode code point arrives in the buffer) but does not render the indicator UI. Reporter wants visual parity with native text fields. Labeled `c: new feature`.

**Why skip-proposal.** Pure additive UI: rendering a transient indicator inside `EditableText` while the OS-level Unicode entry mode is active. Implementation depends on per-platform signal availability (Linux IBus / Windows IMM) — partly framework, partly embedder. No current bug to gate.

**Dedup scan.** No in-category duplicates.

### #38503 — TextField doesn't appear within a direction:Axis.vertical Wrap

- **URL:** https://github.com/flutter/flutter/issues/38503
- **Created:** 2019-08-14 (~6.7 y old) · **Updated:** 2024-12-11
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal**

**Root cause.** `Wrap(direction: Axis.vertical)` provides unbounded horizontal constraints to its children. `InputDecorator` asserts that its width is bounded; the resulting AssertionError surfaces as "TextField doesn't appear". Working as intended w.r.t. the `InputDecorator` contract, but the user-facing failure mode is an assertion crash rather than a graceful intrinsic-width fallback or a clearer error.

**Why skip-proposal.** Resolution would be (a) doc/error-message improvement explaining the unbounded-width interaction, or (b) loosening `InputDecorator` to compute an intrinsic width when the parent provides unbounded constraints. Both proposal-shaped.

**Dedup scan.** No in-category duplicates.

### #155919 — Error where possible null is being asserted in rendering paragraph

- **URL:** https://github.com/flutter/flutter/issues/155919
- **Created:** 2024-09-30 (~1.6 y old) · **Updated:** 2024-10-23
- **Reactions:** 0
- **Labels:** `framework`, `a: error message`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** `RenderParagraph.text` non-null assertion fires during `debugDescribeChildren` → `DiagnosticsNode.toJsonMap` when an `Expanded(child: Text(...))` Row child has its `BoxConstraints` width collapse to 0 during async window resize on macOS. Per summary, related PR #155920 was filed; issue still needs a fix. No clean minimal reproducer.

**Why skip-proposal.** This is a debug-time diagnostics edge case along the DevTools serialization path — not a runtime user-facing rendering bug. The fix is a defensive `?` / null-aware access in `RenderParagraph.debugDescribeChildren`. The associated PR #155920 is the appropriate vehicle; no regression test surface beyond the diagnostics path.

**Dedup scan.** No in-category duplicates.

### #110470 — canvas.drawLine() does not paint correctly on Samsung Galaxy Note 20 Ultra

- **URL:** https://github.com/flutter/flutter/issues/110470
- **Created:** 2022-08-29 (~3.7 y old) · **Updated:** 2024-09-26
- **Reactions:** 0
- **Labels:** `a: text input`, `e: device-specific`, `platform-android`, `framework`, `engine`, `f: material design`, `dependency: skia`, `c: rendering`, `P2`, `e: samsung`, `team-android`, `triaged-android`, `found in release: 3.19`
- **Ownership:** `team-android`
- **Decision:** **likely-stale (signal-based)**

**Root cause.** `canvas.drawLine()` mis-paints on a Samsung Galaxy S4 (GT-I9500, Android 5.0.1). Triagers could not reproduce on a Samsung Tab A7 (Android 11/12). Title says "Note 20 Ultra" but body is the GT-I9500. A different Samsung-device drawLine bug (#145872) was closed in favor of this one. Per summary, the GT-I9500 is discontinued.

**Why likely-stale.** Discontinued device, no recent triage progress, no engine-side investigation, `dependency: skia` rendering path is unlikely to receive attention for an Android 5.0.1 minimum-SDK device. Recommend closing with a "device EOL, can't repro on supported hardware" rationale. Note this is also tangentially mis-categorized — `canvas.drawLine` is not a text-input concern; the inclusion in this category appears incidental.

**Dedup scan.** No in-category duplicates.

### #54998 — Directional navigation key binding defaults should be limited to those platforms that use it

- **URL:** https://github.com/flutter/flutter/issues/54998
- **Created:** 2020-04-16 (~6.0 y old) · **Updated:** 2024-07-22
- **Reactions:** 0
- **Labels:** `framework`, `platform-macos`, `a: desktop`, `a: devtools`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **likely-stale (signal-based)**

**Root cause.** Default `DirectionalFocusIntent` key bindings in `app.dart` were enabled on macOS (and possibly Linux), causing unwanted focus traversal on systems that don't use OS-level directional nav. Per summary: "the default bindings were intended to be removed but the issue remained open with stale labels." Workarounds documented (`Shortcuts(... DoNothingAction)`).

**Why likely-stale.** Per the summary's own framing — fix was intended and the issue is bookkeeping. Recommend closing after verifying current default bindings on macOS / Linux.

**Cluster.** Member of **VKN-1** (Visual Keyboard Navigation in RTL): policy-level companion to #78660. See #78660 entry for cluster definition.

**Dedup scan.** Searched `directional`, `default key binding`. Adjacent: #78660 (the actual RTL arrow-direction bug).

### #99139 — [MacOS] Trailing whitespace in multiline TextField overflows and doesn't go to newline

- **URL:** https://github.com/flutter/flutter/issues/99139
- **Created:** 2022-02-25 (~4.2 y old) · **Updated:** 2024-06-20
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.10`, `found in release: 2.11`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Multi-line `TextField` on macOS / desktop allows trailing whitespace to overflow horizontally instead of soft-wrapping to a new line. Per summary: "Attributed to Skia-level text layout behavior." Differs from the TWA-1 family (which is about TextAlign.right rendering) — this is about line-wrap policy for trailing whitespace.

**Layer check (C1).** Per summary, attributed to Skia paragraph-layout. Engine layer.

**Why skip-engine.** Wrap-policy decision lives in SkParagraph: "do trailing whitespace runs participate in soft-wrap budget?" The framework can't override this without adding a normalization pass on text content (which would break exact-character round-trips).

**Dedup scan.** Searched `trailing whitespace.*multiline`, `trailing whitespace.*wrap`. Adjacent to **TWA-1** but distinct (alignment vs wrap). Recorded as cousin, not member.

### #119684 — Extending to paragraph/or word boundary on MacOS should default to the `downstream` position when at a word wrap

- **URL:** https://github.com/flutter/flutter/issues/119684
- **Created:** 2023-02-01 (~3.2 y old) · **Updated:** 2024-06-06
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `platform-macos`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Body proposes a default-affinity policy change: when extend-to-paragraph / extend-to-word-boundary shortcuts on macOS collapse a selection at a soft word-wrap, the resulting collapsed selection should default to `TextAffinity.downstream` rather than inheriting `selection.base.affinity`. References discussion in PR #116549.

**Why skip-proposal.** Pure default-policy change in framework selection logic. Subjective — there is no obviously-correct answer; the proposal advocates for one specific default. No bug-symptom regression target.

**Dedup scan.** No in-category duplicates.

### #13468 — TextSelection.isDirectional is not respected, make it do something useful eg: for Mac

- **URL:** https://github.com/flutter/flutter/issues/13468
- **Created:** 2017-12-09 (~8.4 y old) · **Updated:** 2024-05-09
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `c: proposal`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** `TextSelection.isDirectional` field exists but is not consulted anywhere; current directional-extension behavior is implemented in `DefaultTextEditingShortcuts` and is purely platform-driven. Body proposes either wiring `isDirectional` into the shortcuts logic or removing the field. Labeled `c: proposal`.

**Why skip-proposal.** Pure API tidying. No user-visible bug to gate.

**Dedup scan.** No in-category duplicates.

### #144759 — Arrow key navigation gets stuck at the end of RTL text using Samsung Keyboard

- **URL:** https://github.com/flutter/flutter/issues/144759
- **Created:** 2024-03-07 (~2.1 y old) · **Updated:** 2024-03-07
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 3.19`, `team-text-input`, `triaged-text-input`, `found in release: 3.21`
- **Ownership:** `team-text-input`
- **Decision:** **likely-duplicate** (canonical: #78660)

**Root cause.** With ten Persian `'ی'` characters and selection at logical offset 10 (visual far-left in RTL), pressing the Samsung keyboard's left arrow doesn't move the cursor. Per summary: Samsung keyboard sends the key only when it thinks the cursor is not at the end; it tracks the cursor's *visual* position; Flutter's logical-order navigation says the cursor is *logically* at the end (offset 10), so the keyboard observes "cursor at start" in visual terms and refuses to send. Gboard, which forwards the key unconditionally, is unaffected.

**Why likely-duplicate.** Same root cause as #78660: Flutter's arrow-key behavior is logical-order while every native keyboard / OS expects visual-order. Implementing visual-order arrow navigation (the #78660 fix) would automatically resolve this — the cursor would advance visually, Samsung keyboard would observe progress, and the key would continue to be forwarded. The Samsung-keyboard-specific framing here is a downstream symptom of the same architectural gap.

**Cluster.** Member of **VKN-1**. See #78660 entry.

**Dedup scan.** Searched `arrow.*rtl`, `samsung.*arrow`, `visual order`. Direct hit #78660. #54998 (default directional bindings) is policy-adjacent.

### #113228 — Provide an API to detect if a TextPosition is located at a soft word wrap

- **URL:** https://github.com/flutter/flutter/issues/113228
- **Created:** 2022-10-10 (~3.5 y old) · **Updated:** 2024-03-06
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `platform-ios`, `framework`, `c: proposal`, `P3`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal**

**Root cause.** Body proposes a public `RenderEditable` API to query whether a given `TextPosition` is at a soft word-wrap. Use case: iOS-style "tap-to-toggle-toolbar" where the toggle behavior should differ at a soft-wrap boundary. Labeled `c: new feature` + `c: proposal`.

**Why skip-proposal.** Pure additive query API. Implementation surface depends on `LineMetrics` line-boundary fields (cluster **LM-1**); without those, the API can be approximated but not authoritative.

**Cluster.** Loosely tied to **LM-1** (consumer of line-metrics line-boundary information). Recorded as adjacent, not core.

**Dedup scan.** Searched `soft word wrap`, `RenderEditable.*api`, `TextPosition.*wrap`. No in-category duplicates.

### #92507 — Document "ghost run" and its interaction with `Paragraph.getBoxesForRange`

- **URL:** https://github.com/flutter/flutter/issues/92507
- **Created:** 2021-10-26 (~4.5 y old) · **Updated:** 2023-08-04
- **Reactions:** 0
- **Labels:** `a: text input`, `engine`, `d: api docs`, `a: typography`, `P2`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — feature/proposal**

**Root cause.** `getRectsForRange` can return boxes outside the paragraph's bounding box for "ghost runs" (trailing whitespace on centered/right-aligned paragraphs that does not contribute to layout but is selectable). Body links the engine code comment in `paragraph_txt.cc:742` and asks for this surface to be documented in the public API. Labeled `d: api docs`.

**Why skip-proposal.** Documentation request; resolution is text in API doc-comments. Tangentially relevant to the **TWA-1** cluster (the same ghost-run mechanism explains why trailing whitespace renders inconsistently under TextAlign.right) — recorded as adjacent context.

**Dedup scan.** Cross-references #40648 / TWA-1 cluster (ghost-run is the underlying mechanism that produces the bug).

### #87536 — BIDI text painting skipped tests

- **URL:** https://github.com/flutter/flutter/issues/87536
- **Created:** 2021-08-03 (~4.7 y old) · **Updated:** 2023-07-08
- **Reactions:** 0
- **Labels:** `a: text input`, `c: contributor-productivity`, `framework`, `a: internationalization`, `P2`, `c: tech-debt`, `team: skip-test`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** Tracking bug for several skipped tests in `packages/flutter/test/painting/text_painter_rtl_test.dart` that don't have individual bug references. Body lists the specific line numbers. Labeled `c: tech-debt` + `c: contributor-productivity`.

**Why skip-proposal.** Cleanup / contributor-productivity tracking — the resolution is per-skipped-test triage (re-enable, mark intentional, or file specific bug). No user-visible regression surface.

**Dedup scan.** No in-category duplicates.

## Duplicate clusters

Six tentative clusters were identified across the 44 issues. Cluster codes are local to this report.

### TWA-1 — Trailing Whitespace under TextAlign.right (Skia)

**Canonical:** #40648 (R=16, oldest concrete reproduction with upstream Skia tracker).

**Members:** #40648, #86668, #90058.

**Shared root cause.** SkParagraph's right/center alignment trims trailing whitespace from the rendered glyph run. Caret math then cannot advance past the trimmed region. Upstream Skia bug `chromium.org/p/skia/issues/detail?id=11933` accepted.

**Coordination.** Close #86668 and #90058 in favor of #40648. When the Skia fix rolls into Flutter, all three are resolved together. #92507 (ghost-run documentation) explains the underlying mechanism but is a separate doc deliverable.

### PS-1 — Paragraph Spacing API (TextStyle / TextOverride)

**Canonical:** #36854 (R=12, oldest framing) — though **#177408 has the most concrete proposed API name** (`paragraphSpacing` on `TextStyle`).

**Members:** #36854, #177408, #177953.

**Shared root cause.** `TextStyle` has no public `paragraphSpacing` field analogous to `letterSpacing` / `wordSpacing`. Drives a recurring accessibility request (WCAG paragraph-spacing requirements).

**Coordination.** Merge #36854 and #177953 into #177408 (or vice-versa). #172915 already exposed `MediaQueryData.paragraphSpacingOverride`; #177953 asks the framework's own widgets to honor it; #177408 / #36854 ask for the underlying `TextStyle` field.

### VKN-1 — Visual Keyboard Navigation in RTL

**Canonical:** #78660 (R=15, framework Intent definition).

**Members:** #78660, #54998, #144759.

**Shared root cause.** `default_text_editing_shortcuts.dart` binds arrow keys to logical-direction `ExtendSelectionByCharacterIntent(forward: ...)`. In RTL paragraphs this produces visually-reversed cursor movement. Downstream symptoms include keyboards (Samsung) refusing to forward arrow keys at the *visual* end of an RTL run because Flutter's logical-end position disagrees.

**Coordination.** Implement visual-order arrow navigation per #78660 (extend Intent system with explicit left/right semantics). #144759 is auto-fixed. #54998 is a policy-adjacent default-bindings concern, partly addressed.

### LM-1 — Line Metrics API gaps

**Canonical:** #91010 (engine `LineMetrics` line-boundary fields).

**Members:** #91010, #75572, #133930. **Adjacent (consumer):** #113228, #167466.

**Shared root cause.** `dart:ui.LineMetrics` strips the `TextRange` info SkParagraph already computes. Downstream consumers (`RenderEditable` vertical caret, framework-level layout-callback APIs, soft-wrap-detection APIs) work around this with brittle pre-passes.

**Coordination.** Land #91010 (engine adds the field), then #75572 (`RenderEditable` adopts), then #133930 / #113228 (framework callbacks built on the new surface). #167466 (height-constrained ellipsis) becomes implementable once line metrics include line-boundary `TextRange`.

### SK-RECT-1 — Skia `getRectsForRange` RTL / non-Latin geometry

**Canonical:** #39755 (R=10, oldest concrete reproduction with engine-team analysis).

**Members:** #39755, #117139, #174689. **Adjacent:** #34610 (mixed RTL/LTR is geometry-adjacent at the paragraph-direction level).

**Shared root cause.** SkParagraph's range-rect computation produces incorrect geometry for non-Latin / RTL runs in several scenarios: justified Korean / Arabic / Hebrew (#39755), RTL multi-line `.`-terminated runs (#117139, with upstream Skia bug #14035), and trailing-whitespace word selection (#174689). All depend on `Paragraph.getRectsForRange` / `getBoxesForRange`.

**Coordination.** Track each Skia upstream bug; the framework can't usefully gate any of these.

### CRLF-W-1 — CRLF on Windows (embedder editing-state synthesis)

**Canonical:** #93934 (R=2, oldest concrete reproduction).

**Members:** #93934, #139443.

**Shared root cause.** Windows' embedder reports `\r` characters in editing-state where macOS / Linux embedders normalize to `\n` (or never produce `\r` to begin with). #93934 is the clipboard-paste path; #139443 is the manual-typing-of-Enter path in RTL multi-line. Both leave `\r` in the buffer and produce caret-skip / wrong-side-deletion symptoms.

**Coordination.** Decide normalization point: Windows `TextInputPlugin.cpp` (most natural) or `dart:ui.Clipboard.getData` (cross-platform). Once normalized at any layer, both issues resolve.

## Likely-stale candidates for closure review

Five signal-based stale candidates from this re-audit. Each has either an obvious resolution upstream, a documented user-expectation mismatch, or an EOL'd reproduction surface:

| # | Title | Reason |
|---|---|---|
| #103705 | letterSpacing in TextField with monospace font (only first char) | Skia fix landed (`skia-review.googlesource.com/c/skia/+/541978`); commenter confirmed fixed pending stable promotion. Verify current stable Flutter includes the roll. |
| #165204 | Unicode characters not being rendered correctly in goldens test | Behavior is correct: Ahem test font is intentionally limited; non-Latin code points render as tofu by design. Use `loadAppFonts()` or pick a different font. |
| #110470 | `canvas.drawLine()` does not paint correctly on Samsung Galaxy Note 20 Ultra | Discontinued device (GT-I9500, Android 5.0.1). No engine-side investigation in 3.5 years. Also tangentially mis-categorized — `canvas.drawLine` is not text-input. |
| #54998 | Directional navigation key binding defaults | Per discussion: "default bindings were intended to be removed but the issue remained open with stale labels." Verify current default bindings on macOS / Linux and close. |
| #78864 | Text does not draw correctly based on text direction | 5-year-old `f: material design` with one confirming reaction, no triage progress, and a symptom description that more closely matches correct Unicode BiDi behavior misunderstood by the reporter than a Flutter bug. |

(No `pass-green, exercises bug path` test outcomes in this re-audit. The single `pass-green, does not exercise the real bug path` outcome — #184240 — is **not** a staleness signal per the workflow spec.)

## Cross-category sibling / split-issue links

Per the user's standing direction for this re-audit, RTL / BiDi / text-layout issues currently classified into other categories (Cursor, Selection gestures, SelectableText) are **not** absorbed into this report. The dedup scans noted several such siblings while in flight (e.g. #175983 for #39755, #11738 / #117140 / #178945 for #117139), all out of scope here. They remain candidates for a future cross-category dedup pass when Step 3 re-organizes the taxonomy.

## Skipped — engine-level

Roll-up of the 14 `skip — engine-level` decisions for quick scanning:

| # | Title | Engine surface |
|---|---|---|
| #34610 | Mixing RTL and LTR text bugs | `ParagraphStyle.direction`, SkParagraph (#39420 migration) |
| #39755 | Selection of any justified-text is inaccurate in non-latin languages | LibTxt `justification_x_offset` per code-unit run |
| #40648 | Trailing space doesn't work with TextField with TextAlign.right | Skia bug 11933 (paragraph-layout trailing-whitespace trim) |
| #71083 | TextField widgets do not wrap text correctly | SkParagraph line-break (no character-fallback when run is unbreakable) |
| #71318 | TextField RTL input problem with LTR letters/numbers while obscureText is true | Engine BiDi handling of `•` (U+2022) runs in RTL paragraphs |
| #77023 | [Web] CanvasKit feature request: Load fonts as soon as detecting browser locale | `engine/lib/web_ui/.../canvaskit/font_fallback*` |
| #93934 | [Desktop] TextField with pasted CRLF endings has invisible CR char | Desktop embedder clipboard reader — CRLF normalization (CRLF-W-1) |
| #99139 | [MacOS] Trailing whitespace in multiline TextField overflows | SkParagraph soft-wrap policy for trailing whitespace |
| #117139 | Incorrect selection area in RTL TextField | Skia `getRectsForRange` (Skia bug 14035) |
| #139443 | [Windows] Incorrect character deletion in right-to-left texts | Windows embedder editing-state synthesis with CRLF / RTL multi-line (CRLF-W-1) |
| #167466 | Ellipsis not working properly when text overflows via constrained height | Skia paragraph layout has no height-budget input (LM-1 surface) |
| #174689 | App highlights / selects trailing whitespaces in a multi-line textfield | Skia `getRectsForRange` for trailing-whitespace runs (SK-RECT-1) |
| #181759 | RTL TextField breaks when inserting emojis between existing emojis | macOS / Linux embedder composing-state machinery during direction switch |
| #183571 | iOS: NSJSONSerialization crash when deleting SMP characters | `FlutterCodecs.mm` — orphaned UTF-16 surrogate sanitization |
