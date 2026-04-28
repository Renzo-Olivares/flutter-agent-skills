# Internationalization, BiDi, and Text Layout Cleanup Report

Iterative cleanup audit for the **Internationalization, BiDi, and text
layout** category (44 open issues as of the `text_input_issues.json`
snapshot).

Format and workflow specified in
[`../CLEANUP_REPORT_FORMAT.md`](../CLEANUP_REPORT_FORMAT.md). Processed
**one issue at a time** in batches; order is reactions-descending.

**Category scope (per taxonomy).** Text rendering fundamentals that
affect editable/selectable widgets: RTL/LTR direction mixing, BiDi
painting, line breaking (especially CJK and non-Latin), line height and
line metrics, paragraph spacing, letter/word spacing, trailing
whitespace behavior, text overflow/ellipsis, and baseline alignment.
Distinct from IME composing (text entry state) and from generic
TextField rendering bugs.

**Priors from previous categories (watch for overlap):**
- **IME/CJK report** explicitly excludes CJK *line breaking* and CJK
  *layout* — those land here. Watch for ICU-dictionary line-break and
  word-segmentation issues spanning both reports.
- **Hardware keyboard report** includes some RTL navigation issues
  (e.g. #78660 in this category — arrow-keys move wrong way in RTL)
  that are also keyboard-shortcut-shaped. Cross-link rather than
  re-classify.
- **Selection gestures report** ended at 0% write-test rate; selection
  inside justified non-Latin text (#39755 here) likely shares its
  blockers (selection-handle drag, multi-line selection painting).

## Running summary — **CATEGORY COMPLETE**

- **Processed: 44 / 44** ✅
- Tests written: **1** (retained as framework-level gate)
  - Failed as expected: **1** (#93934 paste preserves \r)
  - Pass-green, exercises bug path: 0
  - Pass-green, does not exercise bug path: 0
  - Test error: 0
- Skipped — feature/proposal: **21** (48%)
- Skipped — engine-level: **16** (36%)
- Skipped — needs native-platform verification: 0
- Likely-duplicate: **3**
- Likely-stale candidates (no test, signal-based): **3**
- Duplicate clusters (tentative): **8** — TWS-1 (5 members, 2 confirmed dups) · PSP-1 (3 confirmed, all in-category) · SLR-1 (2 confirmed) · LBW-1 (2) · LM-1 (3 confirmed, in-category) · VOR-1 (2 confirmed) · CRLF-1 (2) · SUR-1 (2)
- Cross-category sibling/split-issue links: **3**

### Coverage summary

- **1 regression test (2.3% write-test rate)** — lower than
  Scrolling containers (8.3%), close to IME/CJK (2.9%) and Hardware
  keyboard (2.0%), and below Selection gestures (0%). The category's
  bugs concentrate where the framework has no observable surface
  (engine-side text layout, embedder JSON encoding, IME composing
  state, Skia BiDi resolution) or where the request is API-shaped
  rather than regression-shaped.
- **21 skip-proposal (48%)** — the highest proposal share of any
  audited category so far. The category absorbs many "framework
  should expose X" requests: paragraph spacing (PSP-1), line
  metrics (LM-1), visual-order RTL traversal (VOR-1),
  TextField overflow control, RTL auto-direction, soft-wrap
  detection API, label-direction cascade, etc.
- **16 skip-engine (36%)** — meaningfully *lower* than the prior
  three categories' 70-73% baseline. Engine bugs in this category
  are dense (SkParagraph BiDi, getRectsForRange, ghost runs,
  trailing-whitespace measurement, embedder JSON encoding) but
  fewer than the proposal pile.
- **3 likely-duplicate, 3 likely-stale** — eight issues
  recommendable for closure or merge after maintainer review.
- **8 clusters identified.** Two have closure paths today (PSP-1
  could ship as one paragraph-spacing PR; LM-1 as one dart:ui
  LineMetrics expansion). TWS-1 and SUR-1 already have engine fix
  paths in the wild (Skia bug 11933 / FlutterCodecs.mm fork patch).

### Hypothesis re-calibration

This category re-confirms the pattern that **write-test rate
correlates with how much of the category's bugs surface through
observable framework state**. Here, the bugs are dominated by:
1. Paragraph layout outputs that are computed in dart:ui /
   SkParagraph and have no framework probe (line metrics,
   getRectsForRange, BiDi resolution, line-break policy, ghost
   runs).
2. Embedder-side IME / clipboard / JSON encoding paths that don't
   round-trip into framework-observable state (#181759, #183571,
   #93934 partial).
3. API-shaped requests with no current bug at all (PSP-1, LM-1,
   VOR-1).

The **one write-test that landed (#93934, fail-as-expected)** found
the rare framework-side lever in this category: the paste handler
in `EditableText.pasteText` is a framework function that takes raw
clipboard payload — normalizing CRLF there is a clean framework fix
that retires both #93934 and the related #139443 (CRLF-1 cluster).

### Strategic notes for any future i18n / text-layout doc

- **PSP-1** (paragraph spacing, 3 issues): PR #172915 already added
  `MediaQueryData.paragraphSpacingOverride`. Closing the loop by
  surfacing it in `TextStyle` (#177408) and consuming it in
  framework Text components (#177953) plus an old form of the same
  ask (#36854) is one feature with three GitHub issues attached.
- **LM-1** (line metrics, 3 issues): a dart:ui `LineMetrics`
  expansion to include line `TextRange` would unblock the framework-
  side consumers (#75572 vertical caret movement, #133930 line-
  count for TextField). #91010 is the engine-side root.
- **VOR-1** (visual-order RTL, 2 issues): explicitly classified as
  planned-but-unimplemented by the team. Cross-cuts Hardware
  keyboard (key bindings) and i18n/bidi (caret semantics).
- **TWS-1** (trailing whitespace, 5 issues, 2 confirmable
  duplicates today): the engine's "ghost run" mechanism (#92507) is
  the canonical explanation. Strategic question for the team: keep
  ghost-run behavior (revise the user-facing symptoms ad-hoc) or
  retire it (one engine change retires the whole cluster).
- **SUR-1** (surrogate-pair embedder JSON crashes, 2 issues): each
  embedder needs its own surrogate-sanitization layer. iOS fix
  pending PR submission per #183571.
- **CRLF-1** (CRLF handling, 2 issues): a framework-side
  normalization in `EditableText.pasteText` (and possibly the
  Windows newline insertion path) closes both. The write-test for
  #93934 already proves the framework lacks this normalization.

## Decision types

Canonical definitions: see [`../CLEANUP_REPORT_FORMAT.md`](../CLEANUP_REPORT_FORMAT.md).
Restated here for in-file reference.

- **write-test** — author a framework-level `testWidgets`/`test` and run it.
  Sub-outcomes:
  - `fail-as-expected` — confirms the bug is real.
  - `pass-green, exercises bug path` — strong staleness signal.
  - `pass-green, does not exercise the real bug path` — bug lives below
    the framework (embedder); retain the test as a forward-gate but a pass
    is *not* a staleness signal.
  - `test-error` — could not run.
- **skip — feature/proposal** — `c: proposal` / `c: new feature` /
  architectural request. No regression surface.
- **skip — engine-level** — fix lives in the engine/embedder and there is
  no framework vantage point where the bug reaches a `testWidgets`.
- **skip — needs native-platform verification** — framework-testable in
  principle, but the *expected* behavior requires a native reference we
  don't have. Deferred.
- **likely-stale (signal-based)** — framework testing not feasible and
  age + inactivity + framework evolution strongly suggest no longer valid.
- **likely-duplicate** — same root cause as another in-category issue;
  canonical identified, merge recommended.

## Processed issues

### #61069 — [proposal] ability to change text overflow on the TextField

- **URL:** https://github.com/flutter/flutter/issues/61069
- **Created:** 2020-07-08 (~5.8 y old) · **Updated:** 2025-07-18
- **Reactions:** 65 (👍 65)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `c: proposal`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** No regression — `TextField`/`TextFormField` simply lack
the `overflow` parameter that `Text` exposes (ellipsis/fade/clip/visible).
When input overflows a single-line field, the end is cropped and (in
debug) the overflow warning paints. The proposal asks for parity with
`Text`'s overflow handling.

**Why proposal.** Labeled `c: proposal` and `c: new feature`. Body is an
API ask, not a regression description. Comments are mostly bumps; one
mentions @LongCatIsLooong working on overflow-ellipsis for editable
text but no PR linked. Workarounds: `auto_size_text_field` package or
manual `TextPainter`-based ellipsis. Belongs in design/API discussion,
not regression-test cleanup.

**Dedup scan.** No exact duplicate within the category. Related:
**#167466** (ellipsis not working when text overflows via constrained
height) — that one IS a bug report on the existing `Text`-side overflow
machinery, not a missing-API request. Distinct.

---

### #51258 — Need to find how much of a long word could fit in one line before an unnatural line break

- **URL:** https://github.com/flutter/flutter/issues/51258
- **Created:** 2020-02-22 (~6.2 y old) · **Updated:** 2023-07-08
- **Reactions:** 28 (👍 24, 👀 4)
- **Labels:** `a: text input`, `framework`, `a: typography`, `c: proposal`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** No bug — the body proposes a public API to query *how
much of a long unbreakable run fits in N pixels*, so apps doing custom
layout can avoid measuring per-character. Cross-references #35994
(non-rectangular layout use cases), #50171 (word/line breaker request).

**Why proposal.** Labeled `c: proposal`. The body explicitly lays out
use cases, complications (Mongolian/Arabic context-shaped glyphs), and
asks for a `Paragraph`/`TextPainter` extension. Pure API request,
no regression surface.

**Dedup scan.** Related but distinct: **#71083** (TextField doesn't
break long unbreakable words at character level) — that one is a bug
about existing wrapping behavior; this one is an API ask for app-side
custom layout. Both touch the same Skia line-break primitive but
have different shapes (bug vs. proposal).

---

### #77023 — [Web] [CanvasKit][Feature Request]: Load fonts as soon as detecting browser locale

- **URL:** https://github.com/flutter/flutter/issues/77023
- **Created:** 2021-03-02 (~5.2 y old) · **Updated:** 2025-10-30
- **Reactions:** 21 (👍 17, 👀 4)
- **Labels:** `a: text input`, `c: new feature`, `a: internationalization`, `a: typography`, `platform-web`, `c: proposal`, `c: rendering`, `e: web_canvaskit`, `P2`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level** (web)

**Root cause.** CanvasKit's font fallback is lazy — it loads CJK (and
Hebrew/Arabic per comments) glyph fonts only after first encountering
unknown characters. The first paint of CJK input shows tofu/gibberish
glyphs, then re-paints correctly once the font arrives. Reproducible on
Chrome/Edge through 3.32.4 (recent stable). HTML renderer + bundling a
CJK font as the family both bypass the issue.

**Why engine-level.** Even though the title and labels frame this as a
feature request, the underlying issue is a current observable rendering
bug whose fix lives in the web engine's font-loading strategy
(CanvasKit's dynamic-font-fallback timing). No framework vantage point
intercepts the canvas paint output to assert glyph correctness; even if
one did, the fix isn't in the framework.

**Dedup scan.** No within-category duplicate. Solely about web canvas
font fallback. Adjacent CJK rendering issues in this category are
about line-break/layout (#71083 wrapping, #51258 measure), not glyph
fallback timing.

---

### #34610 — Mixing RTL and LTR text bugs

- **URL:** https://github.com/flutter/flutter/issues/34610
- **Created:** 2019-06-17 (~6.9 y old) · **Updated:** 2024-03-06
- **Reactions:** 18 (👍 14, 🚀 1, 👀 3)
- **Labels:** `a: text input`, `framework`, `engine`, `a: typography`, `customer: crowd`, `P2`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`

**Layer check (C1).** Body mentions "Type arabic, Type chinese, Type
arabic, switch to chinese keyboard, delete. The arabic will delete all
at once." Comments identify root cause as `ParagraphStyle` directionality
LTR for mixed text → spaces inserted at the wrong end of Arabic spans.
SkParagraph switch (#39420) was the engine fix vehicle. Engine signals
fire — `engine` label, `team-engine` ownership, references to
SkParagraph and `ParagraphStyle`.

- **Decision:** **skip — engine-level**

**Root cause.** Engine-side BiDi handling in `ParagraphStyle`/SkParagraph
mishandles mixed-direction runs — wrong-end space insertion, opposite-
direction keyboard deletion broken, caret position drifts. Partial
improvements after the SkParagraph migration, but the deletion-with-
opposite-keyboard symptom remained as of last comment.

**Why engine-level.** Bug surface is glyph layout + caret position
inside SkParagraph; framework only forwards strings to dart:ui. No
observable framework state captures "Arabic span deleted all at once"
without an actual rendered paragraph + key-event delivery to the
embedder.

**Dedup scan.** Umbrella issue — many specific RTL/BiDi bugs in the
category sit downstream of this one. Tentative siblings: **#117139**
(incorrect selection area in RTL TextField), **#181759** (RTL +
emoji insert breaks), **#139443** (Windows RTL character deletion),
**#71318** (RTL + LTR + obscureText drawing), **#78864** (text doesn't
draw based on direction), **#144759** (arrow nav stuck at end of RTL
on Samsung). Held as tentative siblings; will revisit when those are
processed.

**Cross-category siblings.** None noted yet.

---

### #40648 — Trailing space doesn't work with TextField with TextAlign.right

- **URL:** https://github.com/flutter/flutter/issues/40648
- **Created:** 2019-09-17 (~6.6 y old) · **Updated:** 2025-01-29
- **Reactions:** 16 (👍 16)
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.5`, `found in release: 2.6`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`

**Layer check (C1).** Comment summary cites a Skia bug filed at
`bugs.chromium.org/p/skia/issues/detail?id=11933` (accepted) and a
SkParagraph `CodeUnitFlag 0x0006` observation about `\r` as soft line
break. Skia/engine signals dominate.

- **Decision:** **skip — engine-level**

**Root cause.** SkParagraph excludes trailing whitespace from the
measured paragraph width. With `TextAlign.right` (or `.center`), the
text is right-aligned to that *measured* width, leaving the trailing
space outside the rendered region — invisible to the user. The framework
just paints what `Paragraph.layout()` reports. A workaround using
`IntrinsicWidth` inside a `Row` was suggested but is layout-fragile.

**Why engine-level.** No framework-side knob to override which characters
contribute to the measured line width; SkParagraph owns that decision.
`TextWidthBasis.longestLine` and `.parent` both compute width from
SkParagraph's outputs, which already exclude trailing whitespace.
Framework-level tests can't observe a "wider than measured" paragraph
without instrumenting the engine.

**Dedup scan.** Canonical of the **TWS-1** cluster (Trailing Whitespace
+ alignment, framework reads engine-computed width). Confirmed
within-category members: **#90058** (TextFormField, same root, same
TextAlign.right symptom). Tentative members pending later batches:
**#86668** (extends to TextAlign.center too), **#99139** (multiline +
trailing whitespace overflows instead of wrapping — same exclusion
manifesting as wrap failure), **#174689** (selection highlight extends
past trailing whitespace — same exclusion making selection rect overhang
the laid-out text).

---

### #78660 — Arrow keys in RTL move the wrong way

- **URL:** https://github.com/flutter/flutter/issues/78660
- **Created:** 2021-03-19 (~5.1 y old) · **Updated:** 2024-03-06
- **Reactions:** 15 (👍 15)
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 2.1`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** Flutter's `LogicalKeyboardKey.arrowLeft` is bound to
`ExtendSelectionByCharacterIntent(forward: false)` — i.e., logical-order
movement. In RTL text the logical-previous character lives visually to
the right of the caret, so an arrow-left press appears to move the caret
right. The reporter's expectation (matching macOS TextEdit) is
visual-order traversal: left arrow → caret moves visually leftward
regardless of logical direction.

**Why proposal.** A Flutter team member (comment #10) explicitly
classified this as planned-but-unimplemented: *"Visual order traversal
support is planned but it has not been implemented yet."* That makes
the current logical-order behavior intentional; the ask is a
behavior-change feature (or a platform-specific override matching macOS
/ iOS conventions while keeping logical order on Linux/Windows/Android
where it is the platform convention). No `c: proposal` label, but the
team's own framing dominates.

**Cross-category siblings.** **Hardware keyboard report** is the natural
home for any visual-order shortcut work — the bindings live in the
shortcuts/intent layer. Recorded under cross-category links below.

**Dedup scan.** **#144759** ("Arrow key navigation gets stuck at the
end of RTL text using Samsung Keyboard") is in the same category but
about an entirely different symptom (stuck nav, Samsung-keyboard
specific) — unrelated. **#54998** ("Directional navigation key binding
defaults should be limited to those…") in this category is about
directional traversal in widget focus, not text-caret movement —
unrelated. No within-category duplicate.

---

### #36854 — Feature request: Setting paragraph distance in Text and TextField

- **URL:** https://github.com/flutter/flutter/issues/36854
- **Created:** 2019-07-24 (~6.8 y old) · **Updated:** 2024-03-06
- **Reactions:** 12 (👍 12)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `a: typography`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** No regression. The body asks for paragraph-spacing
control on `Text`/`TextField`, currently absent.

**Why proposal.** `c: new feature` labeled. No comments worth
summarizing. Pure API request.

**Dedup scan.** Tight cluster within category — **#177408** ("framework
should provide a mechanism to change the paragraph spacing") and
**#177953** ("framework should apply `paragraphSpacingOverride`") are
both 2025 follow-ups on the same feature gap. **PSP-1** (Paragraph
Spacing) cluster started; canonical is **#36854** (oldest, most
reactions). Will confirm members when batch 5 reaches #177408 / #177953.

---

### #39755 — Selection of any justified-text is inaccurate in non-latin languages

- **URL:** https://github.com/flutter/flutter/issues/39755
- **Created:** 2019-09-03 (~6.6 y old) · **Updated:** 2024-03-06
- **Reactions:** 10 (👍 9, 👀 1)
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`

**Layer check (C1).** Comment summary mentions
`selectionHeightStyle`/`selectionWidthStyle` (framework knobs) only
*partially* helping — most of the symptom is at the rect-computation
layer, which is `Paragraph.getBoxesForRange` (dart:ui → SkParagraph).
Engine signals dominate.

- **Decision:** **skip — engine-level**

**Root cause.** Selection highlight rectangles are misaligned with
glyphs for Korean, Arabic, Hebrew, and Persian (but not Cyrillic). The
selection *range* is correct; the *rendered rect* lies in the wrong
place. Comments confirm the issue persists across all `textAlign`
modes for RTL scripts (not actually justified-text-specific despite
title), and that font choice (e.g. Amiri for Arabic) helps for
pure-RTL but mixed Latin+RTL stays broken even with a script-correct
font.

**Why engine-level.** Highlight rects come from
`Paragraph.getBoxesForRange`, which is computed by SkParagraph. The
framework has no vantage point to observe glyph-level placement
mismatches — it draws `RRect`s at the offsets dart:ui returns. Fixing
the rect output for complex scripts requires SkParagraph changes.
`selectionHeightStyle`/`selectionWidthStyle` are framework knobs but
they only adjust *how* the boxes get drawn (stroke vs. tight), not
*where* the boxes are.

**Dedup scan.** Sibling within category: **#117139** ("Incorrect
selection area in RTL TextField") — same root surface (selection rect
in RTL), separate report. Tentative cluster **SLR-1** (Selection
Layout Rects in complex scripts) started — canonical #39755 (oldest,
broader scope), member #117139. Will confirm in batch 2.

---

### #90058 — TextFormField with textAlign: TextAlign.right whitespace doesn't show unless text is entered

- **URL:** https://github.com/flutter/flutter/issues/90058
- **Created:** 2021-09-14 (~4.6 y old) · **Updated:** 2025-08-13
- **Reactions:** 6 (👍 6)
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.5`, `found in release: 2.6`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **likely-duplicate** of #40648 (TWS-1 cluster member)

**Root cause.** Identical to #40648 — `TextAlign.right` plus a trailing
space; the space is in the controller's value but not painted, because
SkParagraph excludes trailing whitespace from the measured width that
right-alignment uses as its anchor. Reproduced on web, macOS, Android,
Windows on stable and master per comments.

**Why duplicate.** Same symptom (no rendered trailing space with
`TextAlign.right`), same root layer (SkParagraph trailing-whitespace
exclusion). #40648 is older (2019 vs 2021), has more reactions
(16 vs 6), and is owned by team-framework rather than team-design.
Canonical: **#40648**. Recommend merging the workaround details from
#90058 (transparent overlay hack) into #40648 for completeness.

**Cluster.** **TWS-1** member.

**Dedup scan.** See #40648 above for the broader TWS-1 cluster scan.

---

### #71083 — TextFormField (and TextField) widgets do not wrap text correctly

- **URL:** https://github.com/flutter/flutter/issues/71083
- **Created:** 2020-11-23 (~5.4 y old) · **Updated:** 2024-03-06
- **Reactions:** 5 (👍 5)
- **Labels:** `a: text input`, `framework`, `f: material design`, `dependency: skia`, `a: typography`, `P2`, `team-design`, `triaged-design`
- **Ownership:** `team-design`

**Layer check (C1).** Label `dependency: skia` is the strongest signal.
Body describes Flutter wrapping at the closest preceding word boundary
when a long unbreakable run (e.g., a long URL) doesn't fit, instead of
breaking the run mid-character — i.e., a line-break-algorithm policy
disagreement with Chrome's `overflow-wrap: break-word` semantics.

- **Decision:** **skip — engine-level**

**Root cause.** Line-break decisions live in dart:ui → SkParagraph
(via Skia's ICU line-break tables). Flutter currently uses
break-on-word-boundary semantics; the requested behavior is
break-anywhere when no word boundary fits, which Skia would expose as
a policy flag (analogous to CSS `overflow-wrap: break-word` /
`word-break: break-all`). The framework has no `TextStyle` property
that could pass such a policy through today.

**Why engine-level.** Two coupled gaps: SkParagraph would need a
break-policy hook, and the framework would need a `TextStyle` knob to
pass it through. The first is the gating fix; the second is mechanical
plumbing. Holding as engine-level since the framework alone cannot
implement the change.

**Dedup scan.** **#51258** (above in batch) is the related framework
*proposal* asking for an API to find break points — different shape
(API request vs. behavior bug), same underlying primitive gap.
Tentative cluster **LBW-1** (Line-Break Wrap, long unbreakable runs)
with canonical **#71083** (concrete bug) and member **#51258**
(adjacent proposal). Will revisit if more issues in later batches
fit.

---

### #91738 — [Proposal] Add support for automatically switching text input to RTL or LTR based on first character typed

- **URL:** https://github.com/flutter/flutter/issues/91738
- **Created:** 2021-10-13 (~4.6 y old) · **Updated:** 2023-09-15
- **Reactions:** 5 (👍 4, ❤️ 1)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `a: internationalization`, `c: proposal`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** No regression. Body asks for an `auto` text-direction
mode mirroring HTML's `dir="auto"` so multilingual fields can flip
RTL/LTR based on the first strong-direction character typed (WhatsApp
behavior).

**Why proposal.** `c: proposal` + `c: new feature` labeled. Comments
note `package:intl/bidi.dart` already exposes a `Bidi` class that uses
ICU's `ubidi` API; a public `TextDirection.auto` wired through
`TextField`/`Directionality`/`TextPainter` would close the gap. Pure
API ask.

**Dedup scan.** No within-category duplicate. Adjacent: #34610
(umbrella RTL/LTR mixing bugs) is bug-shaped, not API-shaped.

---

### #91010 — `dart:ui.LineMetrics` should include the line boundaries

- **URL:** https://github.com/flutter/flutter/issues/91010
- **Created:** 2021-09-30 (~4.6 y old) · **Updated:** 2023-09-19
- **Reactions:** 4 (👍 3, 👀 1)
- **Labels:** `a: text input`, `engine`, `a: typography`, `c: proposal`, `P3`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — feature/proposal**

**Root cause.** No regression. SkParagraph's `LineMetrics` already
holds line text-range data internally; the dart:ui binding strips it
on the way out. Workaround per comments: drive
`Paragraph.getPositionForOffset` line-by-line, which is indirect.
Cited as a TODO in PR #90684 (vertical caret movement work).

**Why proposal.** Labeled `c: proposal`. The ask is a pure API
expansion — add `TextRange`-shaped fields to `dart:ui.LineMetrics`
and pass through what SkParagraph already computes. No bug.

**Dedup scan.** Tentative cluster **LM-1** (Line Metrics API gap)
started here. In-category candidates pending later batches:
**#133930** ("No good way to get line metrics for `Text`/`TextField`
widgets" — framework-side consumer) and **#75572** ("Let
`RenderEditable` use LineMetrics instead of assuming every line has…"
— framework-side consumer). All three sit on the same dart:ui surface
gap; #91010 is the engine-side root.

---

### #41324 — TextField/TextFormField labelText and hintText should be right-aligned with TextDirection.rtl

- **URL:** https://github.com/flutter/flutter/issues/41324
- **Created:** 2019-09-25 (~6.6 y old) · **Updated:** 2026-02-16
- **Reactions:** 3 (👍 3)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `a: internationalization`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** `InputDecoration.labelText` follows ambient
`Directionality`, not the host `TextField.textDirection`. When a user
sets `textDirection: TextDirection.rtl` on the field while the
ambient `Directionality` stays LTR, the input flows RTL but the
floating label stays LTR-aligned. Per body, `hintText` and the input
itself work; only the label is "stuck" LTR.

**Why proposal.** Labeled `c: new feature`. The current behavior is
deliberate — `TextField.textDirection` is a per-instance override for
the *input glyph flow*, not a cascade through the decoration widgets.
Making the label inherit `TextField.textDirection` is an API/behavior
change, not a regression fix. Comments say a community workaround
exists but no upstream PR.

**Dedup scan.** No within-category duplicate. Tentative siblings:
**#71318** (RTL + obscureText cursor side) and **#78864** (text
doesn't draw based on direction) — both processed in this batch — are
about RTL *rendering* not InputDecoration alignment. Different layer.

---

### #93934 — [Desktop] TextField with pasted CRLF endings has invisible CR char

- **URL:** https://github.com/flutter/flutter/issues/93934
- **Created:** 2021-11-19 (~4.4 y old) · **Updated:** 2024-06-07
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `framework`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.5`, `found in release: 2.6`, `found in release: 2.8`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **write-test** → **fail-as-expected** (framework lacks paste-time CRLF normalization)

**Root cause.** Native desktop clipboards (Windows, macOS) deliver
CRLF (`\r\n`) line endings verbatim on paste. `EditableText.pasteText`
forwards the raw clipboard payload into the controller without
normalization (`packages/flutter/lib/src/widgets/editable_text.dart`
around line 2841). Downstream, SkParagraph treats `\r` as a
zero-width line-separator code unit, so the character is invisible
but still present — caret navigation around it becomes inconsistent
(arrow-left lands the caret between `\r` and `\n`; arrow-right then
skips both).

**Test approach.**
- Mock `SystemChannels.platform` clipboard channel with the standard
  `MockClipboard` shape (inlined to keep imports framework-only).
- Pump a `MaterialApp` + `Material` + `TextField`.
- Seed the clipboard with `'hello\r\nworld'`.
- Focus the field and call
  `EditableTextState.pasteText(SelectionChangedCause.keyboard)`
  directly — `Actions.invoke(PasteTextIntent)` from the
  `EditableText` element's context fails because the action is
  registered below it.
- Assert the controller's text contains no `\r` and equals
  `'hello\nworld'`.

**Test:** [`issue_93934_paste_crlf_preserves_invisible_cr_test.dart`](../regression_tests/i18n_bidi/issue_93934_paste_crlf_preserves_invisible_cr_test.dart)

**Test outcome.** Fails as expected: `controller.text.contains('\r')`
is `true` after paste — the framework preserves `\r`. Confirms the
bug is framework-observable and the paste handler is the right fix
site for a normalization workaround. The deeper engine-side
behaviors (zero-width `\r` rendering, caret-stop computation) remain
even after a framework fix; the framework fix mostly removes the
user-facing damage.

**Dedup scan.** No within-category duplicate. Search terms: `crlf`,
`\\r`, `carriage`, `paste` — only #93934 surfaces with this shape in
the category. No related issues in i18n/bidi.

**Cross-category siblings.** Adjacent — Hardware keyboard report
covers caret-movement bugs but not paste normalization; if a future
"clipboard handling" cleanup category exists, this is its
poster-child.

---

### #117139 — Incorrect selection area in RTL TextField

- **URL:** https://github.com/flutter/flutter/issues/117139
- **Created:** 2022-12-15 (~3.4 y old) · **Updated:** 2023-07-08
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`

**Layer check (C1).** Comment summary explicitly cites SkParagraph's
`getRectsForRange` as the root, with Skia bug
`bugs.chromium.org/p/skia/issues/detail?id=14035` filed. Engine
signals dominate.

- **Decision:** **skip — engine-level**

**Root cause.** In an RTL multiline TextField, double-clicking a word
that ends in a "." followed by a newline produces a selection
highlight rectangle that doesn't match the word's painted bounds.
SkParagraph's `getRectsForRange` returns geometry that ignores the
script-direction × punctuation × line-boundary interaction.

**Why engine-level.** Highlight rectangles are computed by
SkParagraph; framework only consumes them. A workaround inserting a
trailing whitespace was suggested but is fragile.

**Cluster.** Confirmed member of **SLR-1** (Selection Layout Rects
in complex / RTL scripts) — joins canonical #39755 from batch 1.
Distinct Skia bug numbers (14035 here vs. #39755's broader script
coverage) hint at multiple engine fixes; the framework-level surface
is one and the same (`getBoxesForRange`).

**Dedup scan.** Same category sweep for selection-rect-in-RTL: no
other duplicates beyond the SLR-1 pair. Adjacent: #39755 (canonical),
#34610 (umbrella).

---

### #181759 — RTL TextField breaks when inserting emojis between existing emojis

- **URL:** https://github.com/flutter/flutter/issues/181759
- **Created:** 2026-01-31 (~0.2 y old) · **Updated:** 2026-03-06
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `platform-android`, `framework`, `f: material design`, `platform-macos`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`

**Layer check (C1).** Comment summary cites embedder-level
exception (`wstring_convert::to_bytes`) on macOS/Linux, plus
"cannot be fixed in the framework and requires fixes in each
affected embedder" from #183112. Engine/embedder signals are
overwhelming.

- **Decision:** **skip — engine-level**

**Root cause.** Switching `TextField.textDirection` while an IME
composing region is active triggers a `wstring_convert::to_bytes`
exception in the macOS/Linux embedders (built `-fno-exceptions`,
which translates the throw into an abort). On Android the IME
composing state is invalidated and produces `?` replacement
characters. iOS and web do not reproduce. Crash log shows engine
decoding an invalid JSON surrogate pair — half of an emoji surrogate
pair survived the direction switch and broke the platform-channel
JSON encoder.

**Why engine-level.** Each embedder owns its IME plumbing and the
JSON-encoding round-trip; the framework can only deliver the
`textDirection` change. The linked comment in #183112 makes this
explicit.

**Dedup scan.** No within-category duplicate. Tentative sibling at
the "RTL × IME × surrogate-pair" surface, but no other category
issues hit that intersection.

---

### #41641 — [web] Support line height + word spacing in text fields

- **URL:** https://github.com/flutter/flutter/issues/41641
- **Created:** 2019-09-30 (~6.6 y old) · **Updated:** 2024-03-06
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `platform-web`, `P3`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — feature/proposal**

**Root cause.** `TextInput.setStyle` (the framework→engine platform
channel that reports the editable's text style to the embedder for
overlay-input rendering) does not carry line-height or word-spacing
fields. On web the hidden contenteditable / `<textarea>` overlay
therefore can't match the framework's painted style on those axes.

**Why proposal.** Labeled `c: new feature`. Pure API expansion —
add fields to the platform channel + matching plumbing in the web
embedder.

**Dedup scan.** No within-category duplicate. Adjacent: #36854
(paragraph-spacing API gap, PSP-1) is the same shape (missing
typography knob) but at the framework public API, not the
platform channel.

---

### #71318 — TextField RTL input problem with LTR letters/numbers while obscureText is true

- **URL:** https://github.com/flutter/flutter/issues/71318
- **Created:** 2020-11-27 (~5.4 y old) · **Updated:** 2024-07-11
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `engine`, `f: material design`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-design`, `triaged-design`
- **Ownership:** `team-design`

**Layer check (C1).** `engine` label, comment summary linking #47745
/ #50098 / #54099 (older obscureText/RTL bugs), root cause involves
paragraph-direction resolution by SkParagraph from character class.
Engine signals.

- **Decision:** **skip — engine-level**

**Root cause.** When `obscureText: true` replaces input with bullet
characters, SkParagraph's BiDi resolution sees an all-bullet (LTR
character class) string and resolves the paragraph direction LTR even
though `Directionality` (and `TextField.textDirection`) say RTL. The
caret then visually appears on the LTR side during typing, even
though the underlying value is correct (per reporter and comments).

**Why engine-level.** The fix is either (a) SkParagraph honoring an
explicit `textDirection` override regardless of resolved-from-content
direction, or (b) framework substitutes a bullet character with
intrinsic-RTL class when `obscureText && textDirection == rtl`.
Option (b) is hacky and font-dependent. The clean fix is engine-side
direction-override semantics.

**Dedup scan.** Adjacent siblings in category: **#34610** (umbrella
RTL/LTR mix), **#78864** (RTL rendering of formatted dates),
**#181759** (RTL+emoji embedder crash). Same broad area but each has
a distinct trigger; no outright duplicate.

---

### #78864 — Text does not draw correctly based on text direction

- **URL:** https://github.com/flutter/flutter/issues/78864
- **Created:** 2021-03-23 (~5.1 y old) · **Updated:** 2025-07-22
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 2.1`, `team-design`, `triaged-design`
- **Ownership:** `team-design`

**Layer check (C1).** Body describes formatted strings (e.g.
`06 PM`, `PM 06`) rendering identically when `Directionality` is
flipped — i.e., paragraph BiDi reordering producing the same glyph
order. SkParagraph BiDi territory.

- **Decision:** **skip — engine-level**

**Root cause.** Mixed Latin + ambient-direction text reorders glyphs
during BiDi resolution; the displayed visual order can collapse two
intentionally-different strings ("06 PM" with explicit ordering vs.
"PM 06" written backwards) to the same glyph sequence after BiDi
applies. Same SkParagraph layer as #34610.

**Why engine-level.** No framework lever to override BiDi
reordering for runs of strong directional characters.

**Dedup scan.** Sub-case of #34610 umbrella. Held as separate
because the specific repro (date-format strings) is distinct, but
recommend cross-linking in any RTL strategy roll-up.

---

### #84317 — Share code between RenderParagraph and RenderEditable

- **URL:** https://github.com/flutter/flutter/issues/84317
- **Created:** 2021-06-10 (~4.9 y old) · **Updated:** 2023-07-08
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `a: typography`, `P2`, `c: tech-debt`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal** (tech-debt refactor)

**Root cause.** No regression. Body proposes refactoring `RenderEditable`,
`RenderParagraph`, and the `SelectableText`/`SelectionArea` rendering
path to share WidgetSpan-handling code rather than maintain three
near-duplicate codebases. Originated from PR #83537 review feedback.

**Why proposal.** `c: tech-debt` labeled. Pure refactor; no
user-visible bug. Treating tech-debt refactors as
feature/proposal-bucket per the spec — no regression surface.

**Dedup scan.** No within-category duplicate. Cross-cat sibling
**#38474** (referenced in the body) is about WidgetSpan support in
SelectableText — outside our taxonomy categories likely.

---

### #86668 — TextField doesn't handle trailing space as characters if textAlign is TextAlign.right/TextAlign.center

- **URL:** https://github.com/flutter/flutter/issues/86668
- **Created:** 2021-07-19 (~4.8 y old) · **Updated:** 2024-09-26
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.2`, `found in release: 2.4`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **likely-duplicate** of #40648 (TWS-1 cluster member)

**Root cause.** Same SkParagraph trailing-whitespace exclusion as
#40648 / #90058. The novelty of #86668 is documenting that the
behavior also applies to `TextAlign.center`, not only `.right`.
Confirmed via triager video; no separate root-cause path.

**Why duplicate.** Pure scope expansion of #40648's symptom — no new
mechanism or fix surface. A single SkParagraph change retires #40648,
#90058, and #86668 simultaneously.

**Cluster.** **TWS-1** confirmed member.

**Dedup scan.** Per #40648 above; no other category issues match the
"alignment + trailing space" scope.

---

### #103705 — letterSpacing in TextField with monospace font is only applied to right side of the first character

- **URL:** https://github.com/flutter/flutter/issues/103705
- **Created:** 2022-05-13 (~3.9 y old) · **Updated:** 2023-07-08
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `engine`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.0`, `found in release: 3.1`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **likely-stale (signal-based)**

**Root cause.** SkParagraph applied `letterSpacing` only to the
trailing edge of a single-character monospace run. A Skia patch
(`https://skia-review.googlesource.com/c/skia/+/541978`) was submitted
and merged in mid-2022. Last comment confirms the fix in master and
notes the issue was kept open pending stable promotion of the Skia
roll.

**Basis for stale signal.** Skia fix landed three years ago; current
stable is several Skia rolls past the merge. No comments since
mid-2023. Verification: real-device repro on current stable; if
non-reproducing, close with pointer to the Skia change.

**Dedup scan.** No within-category duplicate. Solely about a
single-character monospace edge case in SkParagraph letter-spacing.

---

### #133930 — No good way to get line metrics for `Text`/`TextField` based widgets

- **URL:** https://github.com/flutter/flutter/issues/133930
- **Created:** 2023-09-03 (~2.7 y old) · **Updated:** 2024-08-23
- **Reactions:** 1 (👍 1)
- **Labels:** `framework`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.13`, `found in release: 3.14`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** No regression. The reporter constructs a `TextPainter`
to compute line counts but doesn't apply the same `TextStyle` that
the `TextField` ends up rendering with (Material theme + decoration
merging). Per @dnfield: even
`controller.buildTextSpan(context: context, withComposing: false)`
does not reliably carry the same composed style.
@LongCatIsLooong proposed a future framework-level
`onTextLayoutChanged` callback that would expose immutable layout
metrics — explicitly noting `TextEditingController` is the wrong
home (one controller can serve many fields).

**Why proposal.** No bug — the existing API works; the gap is a
missing first-class API for *"give me the line count / line metrics
for this exact rendered TextField"*. Pure API ask.

**Cluster.** **LM-1** confirmed member (joins canonical #91010 from
batch 2). Sibling #75572 (this batch) is also LM-1.

**Dedup scan.** Within-category cluster pass already done (LM-1).

---

### #174689 — App highlights / selects trailing whitespaces in a multi-line textfield

- **URL:** https://github.com/flutter/flutter/issues/174689
- **Created:** 2025-08-29 (~0.7 y old) · **Updated:** 2025-09-18
- **Reactions:** 1 (👀 1)
- **Labels:** `a: text input`, `platform-android`, `platform-ios`, `a: desktop`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.35`, `found in release: 3.36`
- **Ownership:** `team-text-input`

**Layer check (C1).** Comment notes "Native Android and iOS apps do
not highlight trailing whitespace" — i.e., the OS-side selection
rendering excludes trailing whitespace, while Flutter's Skia-driven
selection includes it. Routed to @LongCatIsLooong without a root cause.
Engine signals (Skia/SkParagraph trailing-whitespace selection rect).

- **Decision:** **skip — engine-level**

**Root cause.** Cross-platform: Flutter's selection highlight rect
extends past the visible text into the trailing-whitespace region of
a multiline TextField. Native iOS/Android editors trim the highlight
at the last visible glyph. Same SkParagraph trailing-whitespace
exclusion as TWS-1, manifesting on the *selection-rect* output side
instead of the alignment-anchor side: SkParagraph excludes trailing
whitespace from measured width but `getRectsForRange` returns the
full text-range geometry, so the rect overhangs the laid-out edge.

**Why engine-level.** Same SkParagraph layer as TWS-1 root. Held as
its own issue (rather than likely-duplicate of #40648) because the
user-visible symptom is distinct enough that maintainers will want
to verify each axis (alignment, wrap, selection rect) separately
when the engine fix lands.

**Cluster.** **TWS-1** member (root-cause cluster, not merge-target).

**Dedup scan.** TWS-1 covered in batch 1. No other multiline-
selection-rect issues in the category beyond SLR-1 / TWS-1 axes.

---

### #184240 — Vertical baseline alignment mismatch between Text and collapsed TextField when changing TextLeadingDistribution

- **URL:** https://github.com/flutter/flutter/issues/184240
- **Created:** 2026-03-27 (~0.1 y old) · **Updated:** 2026-04-02
- **Reactions:** 1 (❤️ 1)
- **Labels:** `framework`, `f: material design`, `has reproducible steps`, `team-text-input`
- **Ownership:** `team-text-input`

**Layer check (C1).** Body cites `TextLeadingDistribution.even` vs
`.proportional` and `InputDecoration.collapsed`. Both
`leadingDistribution` and the collapsed-decoration size flow through
RenderEditable + RenderParagraph. Framework signals dominate, but
the actual baseline placement comes from dart:ui paragraph metrics.

- **Decision:** **skip — engine-level**

**Root cause.** Putting a `Text('X')` and a collapsed-decoration
`TextField` with the same `TextStyle` (including explicit
`leadingDistribution`) into a `Row` produces a vertical baseline
mismatch — the field sits high or low relative to the Text depending
on the leading distribution. Recent issue (March 2026), routed to
@LongCatIsLooong, no root-cause analysis yet. Likely RenderEditable
applies leading distribution differently than RenderParagraph (the
two render objects share little code per #84317), or the collapsed
`InputDecoration` adds vertical metric overhead the matching `Text`
doesn't.

**Why engine-level.** The bug surface straddles RenderEditable /
RenderParagraph layout (framework) and dart:ui paragraph baselines
(engine). Without the maintainer's first-pass root cause, holding
as engine-level is the conservative call. **Framework-test
candidate** for a future pass: pump matched Text + collapsed
TextField, assert `getDistanceToBaseline(TextBaseline.alphabetic)`
matches. Skipped now to avoid pre-empting the active investigation.

**Dedup scan.** Adjacent: **#84317** (this category, share code
between RenderParagraph and RenderEditable) — same divergence is the
likely root mechanism.

---

### #13468 — TextSelection.isDirectional is not respected, make it do something useful

- **URL:** https://github.com/flutter/flutter/issues/13468
- **Created:** 2017-12-09 (~8.4 y old) · **Updated:** 2024-05-09
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `c: proposal`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** `TextSelection.isDirectional` exists as a field but
is "not wired up anywhere." Body proposes either making it drive the
behavior currently in `DefaultTextEditingShortcuts` (per-platform
selection direction logic) or removing the field.

**Why proposal.** `c: proposal` labeled. Pure design / API
hygiene — no observable bug. Comments confirm the
`DefaultTextEditingShortcuts` is the place where `isDirectional`
*could* drive behavior.

**Dedup scan.** No within-category duplicate. Adjacent:
**#54998** (this batch) is about default focus-direction key bindings
on macOS — same ballpark (directional selection behavior) but
different surface (focus traversal vs. text-selection field
semantics).

---

### #33858 — Unicode input should be indicated

- **URL:** https://github.com/flutter/flutter/issues/33858
- **Created:** 2019-06-04 (~6.9 y old) · **Updated:** 2024-12-13
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `platform-windows`, `platform-linux`, `a: desktop`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** No regression. Linux's Ctrl+Shift+U Unicode-entry
mode normally renders an underlined "u" in the field as a hint that
Unicode entry is in progress. Flutter accepts the keystrokes
correctly but doesn't display the IME-entry indicator. Windows
behavior assumed similar; macOS doesn't have the equivalent.

**Why proposal.** `c: new feature` labeled. The IME composition state
that drives the "u" indicator is owned by the OS / IBus / IME, and
Flutter would need to surface it in the text-input plumbing
(framework) plus render the visual hint in EditableText (also
framework). New API + new visual.

**Dedup scan.** No within-category duplicate. Cross-cat: IME/CJK
report's composing-state work might intersect (the "u" hint is a
composing-region rendering style).

---

### #38503 — TextField doesn't appear within a direction:Axis.vertical Wrap

- **URL:** https://github.com/flutter/flutter/issues/38503
- **Created:** 2019-08-14 (~6.7 y old) · **Updated:** 2024-12-11
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal**

**Root cause.** `Wrap(direction: Axis.vertical)` provides unbounded
horizontal width to its children. `InputDecorator` (the Material
chrome around `TextField`) asserts a bounded width and throws.
Currently a hard assertion failure rather than a silent visual
issue.

**Why proposal.** No `c: proposal`/`c: new feature` label, but the
fix is behavior-change shaped: either add intrinsic-width support to
TextField/InputDecorator (so it gracefully sizes to a sensible
default in unbounded contexts) or upgrade the assertion to a more
helpful FlutterError pointing at `SizedBox` as the workaround.
Either way it's a deliberate API/UX choice, not a regression. Held
as feature/proposal.

**Dedup scan.** No within-category duplicate. Tangentially relevant
to the broader "TextField rendering, layout, and visual bugs"
taxonomy category, but that's outside our scan scope.

---

### #54998 — Directional navigation key binding defaults should be limited to those platforms that use it

- **URL:** https://github.com/flutter/flutter/issues/54998
- **Created:** 2020-04-16 (~6.0 y old) · **Updated:** 2024-07-22
- **Reactions:** 0
- **Labels:** `framework`, `platform-macos`, `a: desktop`, `a: devtools`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **likely-stale (signal-based)**

**Root cause.** Default directional-focus key bindings in
`app.dart` were enabled on macOS (and possibly Linux) where they
shouldn't be platform-defaults — arrow keys traversed focus and
scrolled in DevTools when custom widgets had their own arrow-key
handlers. Comment summary indicates the bindings *were* intended
to be removed at the top level and re-added per-widget (e.g.,
`ListView`); the issue stayed open with stale labels.

**Basis for stale signal.** "Status: partially addressed; the
default bindings were intended to be removed but the issue remained
open with stale labels." Six years old, no recent comments,
described as partially fixed with workarounds (`Shortcuts` +
`Intent.doNothing`). Verification: grep current `app.dart` for
`DirectionalFocusIntent` defaults on macOS — if the bindings are
already conditional on platform / removed, close with pointer to
the change.

**Cross-category siblings.** **Hardware keyboard report** owns
shortcut/intent bindings. Recorded in cross-category section.

**Dedup scan.** Adjacent: **#13468** (this batch) is about
`TextSelection.isDirectional`, conceptually nearby but a separate
field. **#78660** (batch 1, RTL arrow keys) is also about arrow-key
handling — but that's about caret movement direction, not focus
traversal. Distinct.

---

### #75572 — Let RenderEditable use LineMetrics instead of assuming every line has the same height

- **URL:** https://github.com/flutter/flutter/issues/75572
- **Created:** 2021-02-07 (~5.2 y old) · **Updated:** 2026-03-05
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `f: material design`, `P2`, `c: tech-debt`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal** (tech-debt refactor; LM-1 cluster member)

**Root cause.** `RenderEditable` computes vertical caret movement
under the assumption that all lines have the same height — broken
when `WidgetSpan` or per-line `TextStyle` changes produce
varying-height lines. Up/down-arrow movement may skip a line
entirely. The fix is to thread `LineMetrics` through the vertical-
movement path. Cross-references the per-line height code in
`editable.dart:864-873`.

**Why proposal.** `c: tech-debt` labeled. Refactor to use
`LineMetrics` for caret movement — depends on the `LineMetrics`
API expansion (LM-1 cluster: #91010 engine surface, #133930
framework-consumer). Updated as recently as 2026-03 — issue is
considered live but no fix in flight.

**Cluster.** **LM-1** confirmed member.

**Dedup scan.** Within-category cluster pass done. No other vertical-
caret-movement issues in the category beyond #91010 / #133930.

---

### #87536 — BIDI text painting skipped tests

- **URL:** https://github.com/flutter/flutter/issues/87536
- **Created:** 2021-08-03 (~4.7 y old) · **Updated:** 2023-07-08
- **Reactions:** 0
- **Labels:** `a: text input`, `c: contributor-productivity`, `framework`, `a: internationalization`, `P2`, `c: tech-debt`, `team: skip-test`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal** (tech-debt tracking)

**Root cause.** No bug. Tracking issue for re-enabling skipped tests
in `packages/flutter/test/painting/text_painter_rtl_test.dart` (lines
37, 169, 327, 360, 415, 481, 563 per body links). Each skip should
either be turned back on or marked intentional with a comment.

**Why proposal.** Pure tech-debt cleanup — un-skipping framework
tests is its own workstream, distinct from the per-issue cleanup
audit this report runs. Re-enabling each skip needs case-by-case
investigation; bundling that work here would balloon scope.

**Dedup scan.** No within-category duplicate. Cross-cat: this is the
canonical home for "BIDI text painting tests skipped" tech debt;
related issues might live under the broader skipped-tests audit
(#86396 cited in body) but that's outside our taxonomy.

---

### #92507 — Document "ghost run" and its interaction with `Paragraph.getBoxesForRange`

- **URL:** https://github.com/flutter/flutter/issues/92507
- **Created:** 2021-10-26 (~4.5 y old) · **Updated:** 2023-08-04
- **Reactions:** 0
- **Labels:** `a: text input`, `engine`, `d: api docs`, `a: typography`, `P2`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — feature/proposal** (docs request; canonical TWS-1 explainer)

**Root cause.** No regression. Body asks for public documentation of
the "ghost run" mechanism in SkParagraph (per the source comment at
`flutter/engine/.../paragraph_txt.cc:742-752`): trailing whitespace
gets a non-layout-affecting run that *is* visible through
`getRectsForRange`. So `getRectsForRange` can return rects outside
the paragraph's bounding box — surprising for code that assumes
otherwise.

**Why proposal.** `d: api docs` labeled. Pure documentation request.

**Cluster relevance.** This is the **canonical engine-side
explanation of TWS-1**. Every TWS-1 symptom (#40648, #90058, #86668,
#99139, #174689) is a downstream consequence of the documented
ghost-run behavior. Worth surfacing #92507 in any TWS-1 strategy
discussion as the *intent* statement: the engine's current behavior
is deliberate and documented (in code only). Whether to keep that
intent or revise it (so trailing whitespace contributes to measured
width / layout) is the strategic question for TWS-1.

**Dedup scan.** No within-category duplicate. Adjacent: TWS-1
cluster issues all derive from this mechanism.

---

### #99139 — [MacOS] Trailing whitespace in multiline TextField overflows and doesn't go to newline

- **URL:** https://github.com/flutter/flutter/issues/99139
- **Created:** 2022-02-25 (~4.2 y old) · **Updated:** 2024-06-20
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.10`, `found in release: 2.11`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`

**Layer check (C1).** Comment summary: "Attributed to Skia-level
text layout behavior." Engine signals — same SkParagraph
trailing-whitespace exclusion as TWS-1.

- **Decision:** **skip — engine-level**

**Root cause.** In a multiline TextField on macOS desktop, typing a
long stretch of trailing whitespace doesn't cause line wrap — the
whitespace overflows the field width. iOS/mobile shows the same
no-wrap behavior with a different downstream symptom (subsequent
characters start a new line). Sublime Text and other native editors
do wrap at trailing-whitespace overflow.

**Why engine-level.** SkParagraph excludes trailing whitespace from
the measured line width, so the wrap-decision logic (also in
SkParagraph) never sees the overflowing whitespace as
overflowing. Same root as the rest of TWS-1; the user-facing
symptom is wrap failure rather than alignment misplacement or
selection overhang.

**Cluster.** **TWS-1** member (root-cause cluster, not
merge-target — distinct symptom from canonical #40648).

**Dedup scan.** Per TWS-1 above; no other multiline-wrap-on-
trailing-whitespace issues in category.

---

### #110470 — `canvas.drawLine()` does not paint correctly on Samsung Galaxy Note 20 Ultra

- **URL:** https://github.com/flutter/flutter/issues/110470
- **Created:** 2022-08-29 (~3.7 y old) · **Updated:** 2024-09-26
- **Reactions:** 0
- **Labels:** `a: text input`, `e: device-specific`, `platform-android`, `framework`, `engine`, `f: material design`, `dependency: skia`, `c: rendering`, `P2`, `e: samsung`, `team-android`, `triaged-android`, `found in release: 3.19`
- **Ownership:** `team-android`

**Layer check (C1).** Labels `dependency: skia`, `engine`,
`e: samsung`, `c: rendering`. Body: bug reproduces on Samsung GT-I9500
(Galaxy S4, 2013, Android 5.0.1) with `UnderlineInputBorder`
painting. Engine signals dominate.

- **Decision:** **skip — engine-level**

**Root cause.** `canvas.drawLine()` (used inside `UnderlineInputBorder`
painting) misrenders on Samsung GT-I9500 specifically. Other Samsung
devices (Tab A7, Android 11/12) don't reproduce per triagers. Title
mentions Note 20 Ultra but body identifies Galaxy S4 — title is
misleading. A related issue #145872 was closed in favor of this one.

**Why engine-level.** Hardware-/Skia-specific rendering bug on
discontinued ancient Android (5.0.1, 2013). No framework lever.
Category placement is loose (`UnderlineInputBorder` paints with
`drawLine`, hence text-layout-adjacent), but the bug isn't really
about i18n/bidi/text-layout — it's a Skia-on-old-Samsung-GPU issue.

**Dedup scan.** No within-category duplicate. Probably belongs to a
different category (rendering / device-specific) but locked in here
by the categorization pass.

---

### #113228 — Provide an API to detect if a TextPosition is located at a soft word wrap

- **URL:** https://github.com/flutter/flutter/issues/113228
- **Created:** 2022-10-10 (~3.5 y old) · **Updated:** 2024-03-06
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `platform-ios`, `framework`, `c: proposal`, `P3`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal**

**Root cause.** No regression. Body proposes a `RenderEditable` API
returning whether a given `TextPosition` lies at a soft word-wrap.
Use case: iOS toolbar toggle behavior — when tap is at a word-wrap,
show/hide based on `TextAffinity`; otherwise toggle regardless.

**Why proposal.** `c: proposal` + `c: new feature` labeled. Pure API
ask. Closely related to LM-1 (line-metrics gap) — line boundary
information would expose word-wrap positions, but the ask here is
a more specific boolean predicate.

**Dedup scan.** Adjacent: LM-1 cluster (line-metrics gap) overlaps
in scope. Could be addressed by a richer LineMetrics surface +
helper, or as a standalone API.

---

### #119684 — Extending to paragraph/word boundary on macOS should default to the `downstream` position when at a word wrap

- **URL:** https://github.com/flutter/flutter/issues/119684
- **Created:** 2023-02-01 (~3.2 y old) · **Updated:** 2024-06-06
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `platform-macos`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Behavior policy. On macOS, shift+option+arrow extends
selection to the next paragraph/word boundary. When the original caret
sits at a soft word-wrap and the selection inverts back to its base,
the resulting collapsed selection inherits `selection.base.affinity`
— but per the reporter's macOS-native reference video, it should
default to `downstream`. Comments point to PR #116549 for context.

**Why proposal.** Behavior-policy choice on which `TextAffinity`
collapses inverted selections at word wraps. No `c: proposal` label,
but the change is a deliberate macOS-shortcut policy tuning — not a
regression. Narrow scope, 0 reactions.

**Dedup scan.** Adjacent: **#113228** (this batch, soft-wrap
detection API) is the same conceptual area (caret/word-wrap
interaction) — both are macOS/iOS desktop-shortcut polish work.
No exact duplicate.

---

### #139443 — [Windows] Incorrect character deletion in right-to-left texts

- **URL:** https://github.com/flutter/flutter/issues/139443
- **Created:** 2023-12-03 (~2.4 y old) · **Updated:** 2025-08-21
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `platform-windows`, `has reproducible steps`, `P3`, `found in release: 3.16`, `found in release: 3.18`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`

**Layer check (C1).** Comment summary identifies "the cursor offset
reported by the framework is incorrect for RTL text in multiline mode
on Windows" with manually-typed text containing CRLF (paste works
correctly). Linked to #140739 with suspected CRLF connection. A
commenter notes the bug also affects Android with custom fonts.
Framework-side caret offset reporting + Windows IME line-ending
handling.

- **Decision:** **skip — engine-level**

**Root cause.** On Windows, manually typing Enter in a multiline
TextField with RTL Persian/Farsi text inserts a line ending that the
framework then mis-counts when computing caret offsets. Backspace
deletes the wrong character (visually-left instead of visually-right).
Pasting the same text doesn't reproduce. Workaround: explicitly
insert `\r\n` instead of `\n` on Enter.

**Why engine-level.** The Windows embedder's IME Enter handling
seems to deliver a different character mix than the framework
expects. The framework's caret-offset calculation then misaligns for
RTL text. The deepest fix is in the Windows embedder + framework
caret-offset logic for RTL multiline; both layers are involved.
Holding as engine-level since the embedder fix is the gating one.

**Cluster.** Tentative new cluster **CRLF-1** (CRLF / desktop
line-ending handling). Members: **#93934** (batch 2, paste of CRLF
preserves \r) and **#139443** (this issue, Windows manual-typed
Enter mishandled in RTL caret offsets). Both are about \r/\n
disagreement between the embedder and the framework's text
processing.

**Dedup scan.** Adjacent siblings within category:
**#34610** (umbrella RTL/LTR mixing — deletion across mixed-
direction keyboards remained broken per comments), **#181759** (RTL
emoji embedder crash) — both engine/embedder-side RTL bugs but
distinct triggers.

---

### #144759 — Arrow key navigation gets stuck at the end of RTL text using Samsung Keyboard

- **URL:** https://github.com/flutter/flutter/issues/144759
- **Created:** 2024-03-07 (~2.1 y old) · **Updated:** 2024-03-07
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 3.19`, `team-text-input`, `triaged-text-input`, `found in release: 3.21`
- **Ownership:** `team-text-input`
- **Decision:** **likely-duplicate** of #78660 (VOR-1 cluster)

**Root cause.** Comment summary makes it explicit: "Samsung keyboard
ignores the left-arrow key when the cursor is already at the visual
left end of RTL text, because Flutter uses logical order for arrow
key navigation while Samsung keyboard uses visual order. ... On
native, arrow key navigation moves in visual order which Flutter
does not currently support; a commenter notes this is a long-
standing architectural gap." Same architectural gap as #78660.

**Why duplicate.** Same root cause (Flutter logical-order vs.
visual-order navigation), different surfacing trigger (Samsung
keyboard's visual-order arrow semantics expose a no-op when Flutter
hasn't moved logically). One fix (visual-order traversal, planned
per #78660 comment #10) closes both.

**Cluster.** Tentative new cluster **VOR-1** (Visual Order RTL
navigation) — canonical **#78660**, member **#144759**. Both
processed in this audit. Worth recording: #144759 adds the
device-specific data point that Samsung's keyboard makes the gap
visible even where Gboard hides it.

**Cross-category siblings.** **Hardware keyboard report** owns
arrow-key shortcut bindings (same as for #78660 in batch 1). Cross-
linked.

**Dedup scan.** Within-category sibling **#78660** found and
classified as canonical. No other arrow-key + RTL stuck-cursor
issues in category.

---

### #155919 — Error where possible null is being asserted in rendering paragraph

- **URL:** https://github.com/flutter/flutter/issues/155919
- **Created:** 2024-09-30 (~1.6 y old) · **Updated:** 2024-10-23
- **Reactions:** 0
- **Labels:** `framework`, `a: error message`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`

**Layer check (C1).** Stack trace cites
`packages/flutter/lib/src/rendering/paragraph.dart:348` and `:1278`
(`RenderParagraph.text` getter; `debugDescribeChildren`). Framework-
side null assertion in the diagnostics-tree serialization path.

- **Decision:** **skip — engine-level** (deferred-test marker; framework-side fix but no minimal repro)

**Root cause.** Reporter triggered an assertion failure by spamming
async redraws (macOS window resize) of a Text element inside a
collapsed Row+Expanded layout (BoxConstraints width → 0). Workaround:
wrap both Row children in Expanded. PR #155920 was filed but the
issue was noted as still needing a fix. No minimal reproducer was
produced.

**Why "engine-level" (despite framework root).** The fix lives in
the framework (likely a null guard in `RenderParagraph.text` or
`debugDescribeChildren`), but no minimal reproducer exists — the
trigger is a race during async layout + diagnostics serialization
on window resize. Following the precedent set by Scrolling
containers' `#177453` ("Decision: skip — engine-level (PR in
review)"), classifying as `skip — engine-level` with a deferred-
test marker. Reclassify if a minimal reproducer surfaces.

**Dedup scan.** No within-category duplicate. Adjacent: this is
genuinely a `RenderParagraph` lifecycle bug, not really an
i18n/bidi/text-layout issue — categorization is loose.

---

### #165204 — Unicode characters not being rendered correctly in goldens test

- **URL:** https://github.com/flutter/flutter/issues/165204
- **Created:** 2025-03-14 (~1.1 y old) · **Updated:** 2025-03-27
- **Reactions:** 0
- **Labels:** `a: tests`, `a: text input`, `framework`, `has reproducible steps`, `P3`, `team-text-input`, `triaged-text-input`, `found in release: 3.29`, `found in release: 3.31`
- **Ownership:** `team-text-input`
- **Decision:** **likely-stale (signal-based)**

**Root cause.** Per comment: golden tests use the Ahem fallback
font by default, which doesn't include the U+25CF bullet glyph
(used by `obscuringCharacter`). The bullet renders as a tofu
box. Workaround documented in comment: call `loadAppFonts()`
properly so a real font with the bullet glyph is available.

**Basis for stale signal.** The issue has a documented cause and
a documented workaround. It's a test-harness behavior question
(Ahem font deliberately doesn't include most Unicode glyphs),
not a runtime bug. Recommend closing with a pointer to
`loadAppFonts()` and the Ahem-font caveat in golden testing
docs.

**Dedup scan.** No within-category duplicate. Cross-cat: this is
a golden-test docs issue, not really i18n/bidi/text-layout.

---

### #167466 — Ellipsis not working properly when a text overflows via constrained height instead of max lines

- **URL:** https://github.com/flutter/flutter/issues/167466
- **Created:** 2025-04-21 (~1.0 y old) · **Updated:** 2025-12-21
- **Reactions:** 0
- **Labels:** `framework`, `a: typography`, `c: rendering`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.29`, `found in release: 3.32`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** When a `Text` with `overflow: TextOverflow.ellipsis`
and `maxLines: null` (or large) is clipped by the parent's
constrained *height* (rather than by `maxLines` count), the ellipsis
doesn't render — the text just gets visually clipped past the parent
height bound. Reproducible on stable 3.29 and master 3.32 cross-
platform per comments. A commenter noted it may be working as
intended.

**Why proposal.** SkParagraph's ellipsis machinery only fires when
constrained by `maxLines`; *how many lines fit in this height* is a
framework-side computation that currently isn't done. The workaround
(LayoutBuilder + TextPainter to compute visible lines and pass them
as `maxLines`) is what the framework would need to do internally.
Adding "ellipsis-on-height-overflow" is a behavior addition, not a
regression fix. No `c: proposal` label, but the change is feature-
shaped.

**Dedup scan.** No within-category duplicate. Adjacent: **#61069**
(batch 1, missing `overflow` parameter on TextField) is the same
broad theme (overflow handling gaps) but at the TextField API
surface, not the height-overflow rendering path.

---

### #177408 — The framework should provide a mechanism to change the paragraph spacing of text

- **URL:** https://github.com/flutter/flutter/issues/177408
- **Created:** 2025-10-22 (~0.5 y old) · **Updated:** 2026-01-06
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `a: accessibility`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal** (PSP-1 cluster member)

**Root cause.** No regression. Body proposes adding
`TextStyle.paragraphSpacing` member (parallel to `letterSpacing`,
`wordSpacing`) — a per-style override for inter-paragraph spacing
between `\n`-terminated runs. Use case: WCAG accessibility
requirements.

**Why proposal.** `c: new feature` + `a: accessibility` labeled.
Pure API surfacing.

**Cluster.** **PSP-1** confirmed member (joins canonical #36854 from
batch 1; sibling #177953 below).

**Dedup scan.** Within-category cluster pass already done (PSP-1).

---

### #177953 — The framework should apply `paragraphSpacingOverride` to its text

- **URL:** https://github.com/flutter/flutter/issues/177953
- **Created:** 2025-11-03 (~0.5 y old) · **Updated:** 2026-01-02
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `a: accessibility`, `platform-web`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal** (PSP-1 cluster member)

**Root cause.** No regression. Per body, PR #172915 introduced
`MediaQueryData.paragraphSpacingOverride` /
`MediaQuery.maybeOfParagraphSpacingOverride` for accessibility, but
the framework's own components (`Text`, button labels, headers)
don't consume the override. Proposal: have framework Text-painting
honor it (with carve-outs for buttons, navigation chrome, etc.).

**Why proposal.** `c: new feature` + `a: accessibility` labeled.
Pure framework consumer-side wiring of an API that already exists.

**Cluster.** **PSP-1** confirmed member.

**Dedup scan.** Within-category cluster pass done.

---

### #183571 — iOS: NSJSONSerialization crash when deleting SMP characters

- **URL:** https://github.com/flutter/flutter/issues/183571
- **Created:** 2026-03-12 (~0.1 y old) · **Updated:** 2026-03-19
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-ios`, `P1`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`

**Layer check (C1).** Body and comment summary cite
`engine/src/flutter/shell/platform/darwin/common/framework/Source/FlutterCodecs.mm`
as the fix site. Engine signals dominate.

- **Decision:** **skip — engine-level**

**Root cause.** Deleting Supplementary Multilingual Plane (SMP)
characters (emoji-shaped non-BMP code points) on iOS via
`UITextInput.deleteBackward` leaves orphaned UTF-16 surrogates in
the NSString. The platform-channel JSON encoder
(`NSJSONSerialization`) rejects strings containing lone surrogates
and crashes the app with "Invalid JSON message, encoding failed:
(null)".

**Why engine-level.** Fix is in `FlutterCodecs.mm` — sanitize JSON
object trees before serialization (drop lone surrogates, preserve
valid pairs and BMP chars, remap text-editing cursor indices). A
contributor has implemented the fix on a fork; team member
redirected to monorepo PR submission. Pre-triage suspected it may
also implicate iOS's own `UITextInput.deleteBackward`.

**Cluster.** Tentative new cluster **SUR-1** (Surrogate-pair
embedder JSON crashes). Members: **#181759** (batch 2, RTL+IME
emoji insert breaks via macOS/Linux `wstring_convert` and
Android composing-state) and **#183571** (iOS SMP delete crash via
`NSJSONSerialization`). Both involve unpaired UTF-16 surrogates
producing embedder-side JSON encoding failures, with platform-
specific fix sites in each darwin/linux/android embedder.

**Dedup scan.** Within-category sibling: **#181759** found
(SUR-1 cluster). Body cross-references **#142327** which is outside
our taxonomy. No other surrogate-pair JSON-crash issues in the
category.

## Duplicate clusters

### TWS-1 — Trailing Whitespace + alignment / wrap / selection (framework reads engine-computed width)

- **Canonical:** **#40648** — Trailing space doesn't work with TextField with TextAlign.right (16 reactions, 2019, P2, team-framework).
- **Confirmed merge-targets (likely-duplicate):**
  - **#90058** — TextFormField + TextAlign.right whitespace doesn't show (6 reactions, P2, team-design) · **processed**.
  - **#86668** — extends symptom to TextAlign.center (1 reaction, P2, team-text-input) · **processed**.
- **Same-root-cause but distinct symptom (skip-engine, kept open):**
  - **#174689** — selection highlight extends past trailing whitespace (1 reaction, P2, team-text-input) · **processed**.
  - **#99139** — multiline TextField, trailing whitespace overflows instead of wrapping (0 reactions, P2, team-text-input) — pending batch 4.
- **Shared root cause.** SkParagraph excludes trailing whitespace from
  the measured paragraph width. This single exclusion manifests as:
  invisible trailing space when right/center-aligned (#40648, #90058,
  #86668), wrap failure when the trailing whitespace would overflow a
  multiline (#99139), and selection rect overhang past the laid-out
  text (#174689).
- **Coordination.** A Skia bug
  (`bugs.chromium.org/p/skia/issues/detail?id=11933`) was filed and
  accepted years ago. Worth surfacing the cluster in any future i18n /
  layout strategy doc as one engine fix that retires three-to-five
  GitHub issues. Two distinct merge candidates (#90058, #86668) can
  close immediately as duplicates; #174689 / #99139 should be
  verified independently after the engine fix because their
  user-visible symptoms differ from the canonical's.

### PSP-1 — Paragraph Spacing API gap

- **Canonical:** **#36854** — Feature request: Setting paragraph distance in Text and TextField (12 reactions, 2019, P3, team-framework) · **processed**.
- **Confirmed members:**
  - **#177408** — framework should provide a mechanism to change paragraph spacing (0 reactions, 2025, team-text-input) · **processed**.
  - **#177953** — framework should apply `paragraphSpacingOverride` to its text (0 reactions, 2025, team-text-input) · **processed**.
- **Shared root cause.** No public API on `TextStyle`/`Text`/`TextField`
  to set inter-paragraph (post-newline) spacing distinct from line
  height. PR #172915 already added the engine-side
  `paragraphSpacingOverride` via `MediaQueryData` for accessibility;
  what remains is (a) `TextStyle.paragraphSpacing` member (#177408,
  #36854) and (b) framework consumption of the MediaQuery override
  in built-in components (#177953).
- **Coordination.** A two-part PR (TextStyle field + MediaQuery
  consumption with carve-outs for buttons/headers) closes all three
  GitHub issues simultaneously.

### SLR-1 — Selection Layout Rects in complex / RTL scripts

- **Canonical:** **#39755** — Selection of any justified-text inaccurate in non-Latin (10 reactions, 2019, P2, team-framework).
- **Confirmed members:**
  - **#117139** — Incorrect selection area in RTL TextField (2 reactions, 2022, team-framework) · **processed**.
- **Shared root cause.** `Paragraph.getBoxesForRange` /
  `getRectsForRange` returns misaligned rectangles in Korean /
  Arabic / Hebrew / Persian (and possibly other complex shaping
  cases). Framework just paints what dart:ui hands back. Same
  engine-side rect-computation root.
- **Coordination.** Both engine-level. Distinct Skia bugs filed
  (#39755 has none; #117139 cites
  `bugs.chromium.org/p/skia/issues/detail?id=14035`) — fixes may
  ship independently. Unifying repro across scripts on a single
  test page would help triage when SkParagraph rect computation is
  next touched.

### LM-1 — Line Metrics API gap

- **Canonical (engine):** **#91010** — `dart:ui.LineMetrics` should include line boundaries (4 reactions, 2021, P3, team-engine) · **processed**.
- **Confirmed members:**
  - **#133930** — No good way to get line metrics for `Text`/`TextField` (1 reaction, 2023, team-text-input) — framework consumer · **processed**.
  - **#75572** — Let `RenderEditable` use LineMetrics instead of assuming every line has same height (0 reactions, 2021, team-design) — framework consumer · **processed**.
- **Shared root cause.** SkParagraph internally tracks per-line
  `TextRange` and rich line metrics, but dart:ui's `LineMetrics`
  surface elides several useful fields. Downstream framework code
  (#75572, #133930) works around the gap with imprecise
  approximations or `getPositionForOffset` line-walks.
- **Coordination.** A single dart:ui change unblocks both
  framework-side issues. PR #90684 (vertical caret movement) is the
  cited TODO source. @LongCatIsLooong floated a future
  `onTextLayoutChanged` callback on the framework side as the
  natural consumer surface.

### LBW-1 — Line-Break Wrap, long unbreakable runs

- **Canonical:** **#71083** — TextFormField widgets do not wrap text correctly (5 reactions, 2020, P2, team-design, `dependency: skia`).
- **Tentative members (in batch 1):**
  - **#51258** — Need to find how much of a long word fits in a line (28 reactions, 2020, P3, `c: proposal`, team-framework).
- **Shared root cause / theme.** Both touch the same Skia line-break
  primitive but from opposite ends — #71083 reports the *current
  behavior* (break at last word boundary, leave long run hanging) is
  wrong; #51258 asks for an *API* so apps can custom-handle long
  unbreakable runs. A SkParagraph break-policy hook (analogous to CSS
  `overflow-wrap: break-word`) plus a `TextStyle` knob would address
  both.
- **Coordination.** #71083 is the bug-shaped framing useful for
  triage; #51258 captures the API ask.

### VOR-1 — Visual Order RTL navigation

- **Canonical:** **#78660** — Arrow keys in RTL move the wrong way (15 reactions, 2021, P2, team-framework) · **processed**.
- **Confirmed merge-target (likely-duplicate):**
  - **#144759** — Arrow key nav stuck at end of RTL text using Samsung Keyboard (0 reactions, 2024, P2, team-text-input) · **processed**.
- **Shared root cause.** Flutter's
  `LogicalKeyboardKey.arrowLeft`/`arrowRight` are bound to
  `ExtendSelectionByCharacterIntent(forward: …)` — i.e., **logical-
  order** navigation. macOS / iOS / Samsung Keyboard expect
  **visual-order** navigation in RTL text. Flutter team has explicitly
  classified visual-order traversal as planned-but-unimplemented
  (per #78660 comment #10).
- **Coordination.** Both feature/proposal-shaped per the team's
  framing. Adding a visual-order traversal mode (likely a
  per-platform default, with a framework `Intent` extension or a
  new `arrow_visual_left/right` binding) closes both. The Hardware
  keyboard report is the natural cross-cat home for the binding
  work.

### CRLF-1 — CRLF / desktop line-ending handling (tentative)

- **Members (both processed):**
  - **#93934** — TextField with pasted CRLF endings has invisible CR char (2 reactions, 2021, P2, team-windows) · **write-test, fail-as-expected**.
  - **#139443** — Windows incorrect character deletion in RTL texts (manual-typed CRLF mishandled) (0 reactions, 2023, P3, team-text-input) · **skip-engine**.
- **Shared root cause / theme.** \r/\n disagreement between the
  desktop embedder/clipboard layer and the framework's text/caret
  processing. #93934 is the paste-side surfacing (clipboard
  delivers \r\n, framework stores it raw, downstream rendering and
  caret behavior breaks). #139443 is the manual-input-side
  surfacing (Windows IME Enter delivers a line-ending mix the
  framework's RTL caret-offset code mis-counts).
- **Coordination.** A framework-side normalization layer in
  `EditableText.pasteText` (and possibly the `TextInputAction.newline`
  handler on Windows) would address both — strip `\r` or normalize
  `\r\n` → `\n` on receive. The downstream engine-side `\r`
  handling (zero-width rendering, caret stops) is a separate
  question worth not-fixing if the framework normalizes upstream.
  No within-category sibling — both members already in this cluster.

### SUR-1 — Surrogate-pair embedder JSON crashes (tentative)

- **Members (both processed):**
  - **#181759** — RTL TextField breaks when inserting emojis between existing emojis (2 reactions, 2026, P2, team-text-input) · **skip-engine** (macOS/Linux `wstring_convert::to_bytes`, Android composing-state).
  - **#183571** — iOS `NSJSONSerialization` crash when deleting SMP characters (0 reactions, 2026, P1, team-text-input) · **skip-engine** (`FlutterCodecs.mm`).
- **Shared root cause / theme.** Unpaired UTF-16 surrogates
  (left over from incomplete emoji / SMP-character text-editing
  operations) break the platform-channel JSON encoder in each darwin
  / linux / android embedder. Each embedder has its own JSON-
  encoding path and its own surrogate-handling story; a shared
  sanitization layer (or framework-side surrogate scrubbing before
  the platform call) would centralize the fix.
- **Coordination.** iOS fix already prototyped on a contributor
  fork (`FlutterCodecs.mm`, branch `fix/ios-surrogate-utf16-crash`)
  pending PR submission. macOS/Linux per-embedder fixes called out
  in #183112 (referenced from #181759). Android composing-state
  invalidation may need a separate fix path. Worth tracking together
  because the conceptual bug is shared even if fix sites are
  per-embedder.

## Likely-stale candidates for closure review

- **#103705** — letterSpacing on monospace single-character TextField
  applied only on right.
  **Basis:** signal-based — Skia patch
  `https://skia-review.googlesource.com/c/skia/+/541978` merged
  mid-2022, reporter confirmed fix in Flutter 3.3 master, issue kept
  open pending stable promotion. Three Skia rolls later there's been
  no further activity.
  **Verification:** real-device repro on current stable; if
  non-reproducing, close with pointer to the Skia change.
- **#54998** — Default directional-focus key bindings on macOS
  conflict with custom widgets.
  **Basis:** signal-based — comment thread says the bindings *were*
  intended to be removed at the top level and re-added per-widget
  (e.g., `ListView`) but the issue stayed open with stale labels.
  Six years old, no recent activity, partial fix described.
  **Verification:** grep current `app.dart` /
  `default_text_editing_shortcuts.dart` for `DirectionalFocusIntent`
  defaults conditional on platform — if already removed for macOS,
  close.
- **#165204** — Unicode bullet (U+25CF) renders as tofu in goldens.
  **Basis:** signal-based — root cause is documented in comment
  (Ahem fallback font lacks U+25CF), workaround documented
  (`loadAppFonts()`). It's a test-harness behavior question, not a
  runtime bug.
  **Verification:** confirm the workaround works, point reporter at
  Ahem-font caveat in golden testing docs, close.

## Cross-category sibling / split-issue links

- **#78660** (i18n/bidi: arrow keys in RTL move wrong way) ↔
  **Hardware keyboard report** — visual-order traversal lives in the
  framework's shortcut/intent layer (`text_editing_intents.dart`
  `forward` boolean per comment #9 of #78660). If visual-order
  traversal lands, the change ripples through Hardware keyboard
  bindings.
- **#54998** (i18n/bidi: directional focus key bindings on macOS) ↔
  **Hardware keyboard report** — `DirectionalFocusIntent` defaults
  in `app.dart` / `default_text_editing_shortcuts.dart`. The
  Hardware keyboard report owns intent/shortcut bindings; this
  issue is a behavioral default question on top of those bindings.
- **#144759** (i18n/bidi: arrow-key nav stuck in RTL via Samsung
  keyboard) ↔ **Hardware keyboard report** — same VOR-1 architectural
  gap as #78660. Cross-link recorded for both members of VOR-1.

## Skipped — engine-level (roll-up)

- **#77023** — CanvasKit lazy CJK font fallback (web)
- **#34610** — Mixing RTL and LTR text bugs (umbrella; SkParagraph BiDi)
- **#40648** — Trailing space + TextAlign.right (TWS-1 canonical; SkParagraph)
- **#39755** — Selection rect inaccuracy in non-Latin scripts (SLR-1 canonical; `getBoxesForRange`)
- **#71083** — Long unbreakable runs not wrapped at character (LBW-1 canonical; SkParagraph break policy)
- **#117139** — RTL selection rect at dot+newline (SLR-1 member; `getRectsForRange`, Skia bug 14035)
- **#181759** — RTL+IME emoji embedder crash (`wstring_convert`, macOS/Linux embedders)
- **#71318** — RTL+obscureText cursor visually wrong (SkParagraph BiDi resolution from bullet character class)
- **#78864** — RTL/LTR formatted text rendering (sub-case of #34610 umbrella; SkParagraph BiDi reorder)
- **#174689** — Selection highlight extends past trailing whitespace (TWS-1 member; `getRectsForRange` overhang)
- **#184240** — Vertical baseline mismatch Text vs collapsed TextField (RenderEditable / RenderParagraph leading-distribution divergence; framework-test candidate deferred)
- **#99139** — Multiline TextField trailing whitespace doesn't wrap on macOS (TWS-1 member; SkParagraph wrap excludes trailing whitespace)
- **#110470** — `canvas.drawLine()` misrenders on Samsung Galaxy S4 (Skia + ancient Android hardware; loose category fit)
- **#139443** — Windows manual-typed CRLF in RTL multiline mishandles caret offset (CRLF-1 cluster; Windows embedder + framework caret RTL interaction)
- **#155919** — `RenderParagraph` null assertion in diagnostics path on macOS resize spam (framework-side; deferred-test marker, no minimal repro)
- **#183571** — iOS NSJSONSerialization crash on SMP delete (SUR-1 cluster; `FlutterCodecs.mm` fix pending PR)
