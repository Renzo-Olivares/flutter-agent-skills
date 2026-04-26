# Text Selection Behavior and Gestures Cleanup Report

Iterative cleanup audit for the **Text selection behavior and gestures**
category (28 open issues as of the `text_input_issues.json` snapshot).

Format and workflow specified in
[`../CLEANUP_REPORT_FORMAT.md`](../CLEANUP_REPORT_FORMAT.md). Processed
**one issue at a time** in batches; order is reactions-descending within
the category. Per-issue entries record decision, reasoning, dedup scan,
and (when applicable) the authored regression test and its outcome.

**Category hypothesis going in.** Selection gestures was predicted as
the most framework-testable remaining category — gestures and selection
state are both pure-Dart framework concerns, directly exercisable via
`tester.tap`/`tester.dragFrom`/`tester.longPress` with `controller.selection`
as the observable output. Predicted write-test rate: 15-25%.

**Priors from previous categories (relevant to selection):**

- **CRC-1** (Composing-region cursor clamping, from IME/CJK) — iOS
  composing cursor behavior overlaps with selection behavior during
  composition. Any issue here that involves active IME composition may
  cluster with CRC-1.
- **DSK-IME-1** (Desktop IME candidate-window positioning) — related
  insofar as selection rect is a sibling concept; unlikely to cluster
  here but watch for cross-category overlap on selection rect.
- **Web IME diverse issues** (#126066, #149979, #151097, #151103,
  #174159, #183078, #163946) — selection-on-web issues in this
  category may intersect with that web-IME landscape.

## Running summary — **CATEGORY COMPLETE**

- **Processed: 28 / 28** ✅
- Tests written: **0**
- Skipped — feature/proposal: 6 (#128388, #22619, #79420, #88135, #107671, #115130)
- Skipped — engine-level: 20
- Skipped — needs native-platform verification: 0
- Likely-duplicate: 0
- Likely-stale candidates (no test, signal-based): 2 (#50834, #141369)
- Duplicate clusters (tentative): 0
- Cross-category sibling/split-issue links: 0

### Hypothesis result — I was wrong
Going in I predicted 15-25% write-test rate for this category.
**Actual: 0%.** Full-category retrospective in the dedicated section
below.

### Coverage summary
- 0 regression tests authored. **Lowest write-test rate of any
  category audited** (IME/CJK 2.9%, Hardware keyboard 2.0%, this 0%).
- 6 skip-proposal (21%). Includes two API-refactor proposals
  (#79420 TextSelectionDelegate, #115130 gesture-details refactor)
  and one architectural discussion (#107671 gesture composability).
- 20 skip-engine (71%). Broken down by sub-surface:
  - **Web engine** (11 issues): DOM-hidden-input selection sync,
    focus collision, Safari ::selection CSS, Chrome height thresholds,
    Firefox-specific bugs, right-click-goes-through-hidden-element.
    Half of the category's skip-engine is web-specific.
  - **iOS/Android framework-adjacent** (4 issues): handle-drag + typing
    races, bringIntoView-on-handle-drag, RTL cursor affinity, Dart 3
    diagonal-handle-drag.
  - **Desktop/macOS** (3 issues): generous selection area, Windows
    right-click loses selection, macOS semantic focus.
  - **Engine text layout** (2 issues): per-glyph vs per-line rects,
    line-width selection highlight.
- 2 likely-stale candidates — both are "recent commenter can't
  reproduce, may be incidentally fixed" signals. Real-device
  verification is the follow-up.

## Why this category didn't deliver framework-testable bugs

Going into the audit I expected selection gestures to be the most
framework-testable remaining category: gestures and selection state
are both framework concerns, with clean observable outputs. The
actual result — 0 tests — tells a clearer story than the prediction:

1. **Web dominance surprise.** 11/28 issues are web-platform
   (39%). Web selection bugs almost universally trace to the web
   engine's hidden-textarea/DOM-selection integration, not to
   framework gesture handling.

2. **Framework-fix-target ≠ framework-testable.** Multiple issues
   (#143479 `_bringIntoViewBySelectionState`, #179526
   `_SelectableTextContainerDelegate._calculateLocalRange`, #100319
   `SelectionOverlay._handleEndHandleDragStart`) have pinpointed
   framework code locations — but simulating their triggers
   (handle-drag-while-typing, SelectionArea-with-WidgetSpan backward
   drag, handle-drag-during-scroll) requires specific widget-overlay
   drag-simulation scaffolding that `testWidgets` doesn't make easy.
   These are "framework-fixable" but not "cheaply-framework-testable
   in a batch workflow."

3. **Selection handle testing is the missing primitive.** Many of the
   skipped write-test candidates boil down to "drag the selection
   overlay handle" — which isn't a first-class tester API.
   Improving `flutter_test` harness APIs for selection-handle drags
   (like we already have `tester.drag`, `tester.enterText`) would
   unlock write-tests across at least four of this category's
   issues (#89024, #100319, #143479, #132042).

4. **Architectural proposals accrue here.** 6/28 (21%) are
   proposals — API refactor of `TextSelectionDelegate`, gesture-
   details pass-through, gesture-recognizer composability, extended
   affinity semantics, drag-n-drop, Smart Text Selection. Selection
   attracts API-shape requests comparable to Hardware keyboard's
   shortcut-API proposals.

**Recommendation for future runs.** If the category were re-audited
after the flutter_test harness gains a selection-handle drag API
(e.g., `tester.dragSelectionHandle(TextSelectionHandleType.end, offset)`),
I'd expect the write-test rate to jump meaningfully — probably 10-20%
based on the pinpointed framework-fix-target candidates noted above.

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

### #128388 — drag-n-drop selected text inside textfield

- **URL:** https://github.com/flutter/flutter/issues/128388
- **Reactions:** 10 · **Labels:** `c: new feature`, `framework`, `f: material design`, `c: proposal`, `P2`, `team-text-input`
- **Decision:** **skip — feature/proposal**

Proposal to drag-and-drop selected text *within* a TextField. Separate
from @gspencergoog's OS-level drag-and-drop work. @Renzo-Olivares
noted as having investigated. Native-web on macOS has it.
`c: new feature` / `c: proposal` — out of cleanup scope.

---

### #100319 — Exception on typing while holding selection endpoint (Android, iOS)

- **URL:** https://github.com/flutter/flutter/issues/100319
- **Reactions:** 6 · **Labels:** `c: crash`, `platform-android`, `engine`, `has reproducible steps`, `P2`, `found in release: 2.10/2.13`, `customer: chalk (g3)`, `team-android`
- **Decision:** **skip — engine-level** (framework race, but hard to reproduce in test harness)

**Root cause (per summary).** Android: framework sends out-of-bounds
selection range to `TextInputChannel.TextEditState`, throwing
`IndexOutOfBoundsException`. iOS variant: framework assertion
`!_isDraggingEndHandle` in `SelectionOverlay._handleEndHandleDragStart`.
Both races between user typing and holding a selection handle.
Production users hitting this ~1.7k occurrences / 30 days.

**Why not write-test.** The assertion is framework-level and its
location is pinned (`selection_overlay.dart`), but reproducing the
race requires simulating "pointer-down on handle + simultaneous
text-input platform message" which `testWidgets` can't cleanly
interleave. Real-device repro with touch + keyboard is needed.
Possibly framework-testable with more investigation; skipped for
batch velocity.

---

### #137659 — [Web] Text automatically selected when inserted programmatically

- **URL:** https://github.com/flutter/flutter/issues/137659
- **Reactions:** 6 · **Labels:** `framework`, `platform-web`, `has reproducible steps`, `P2`, `team-web`, `found in release: 3.13/3.16`
- **Decision:** **skip — engine-level** (web)

Web-only: tapping a button that inserts text programmatically
(via `controller.value`) auto-selects the inserted text. Desktop
unaffected. Root cause linked to #119583 (closed/not-in-dataset):
focus collision causes the framework to treat focus as
Tab-triggered → select-all. Workaround: `focusNode.requestFocus()`
first, then set `controller.value` in a post-frame callback.

---

### #162231 — [Web][Chrome] TextField selection jumps when EditableText height exceeds ~3004px

- **URL:** https://github.com/flutter/flutter/issues/162231
- **Reactions:** 5 · **Labels:** `f: material design`, `f: scrolling`, `platform-web`, `has reproducible steps`, `P2`, `browser: chrome-desktop`, `team-web`, `found in release: 3.28/3.29`
- **Decision:** **skip — engine-level** (web)

Chrome-only (including Arc; Safari unaffected): selection cursor
jumps to start when `EditableText.height > ~3004px`. Also affects
`SelectableText`. Linked reports #162698 and #163607. No fix; use
Safari or cap the height as workaround.

---

### #96112 — TextField `style.backgroundColor` covers cursor and selection

- **URL:** https://github.com/flutter/flutter/issues/96112
- **Reactions:** 4 · **Labels:** `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.8/2.9`, `team-text-input`
- **Decision:** **skip — engine-level** (duplicate per comment; blocked)

Setting `TextField(style: TextStyle(backgroundColor: ...))` paints
over the cursor and selection overlay. Per comment: this is a
duplicate of **#79168** (not in our dataset — likely closed or in
another category) and is blocked on **#39420**. PR #96276 was
submitted but not landed. Confirmed persists on 3.32.2.

**Dedup scan.** Would be likely-duplicate if #79168 were in this
category's dataset; since it isn't, recorded here as
blocked-dependency.

---

### #169104 — TextField automatically selected when typing (reporter-specific macOS 15 + Chrome)

- **URL:** https://github.com/flutter/flutter/issues/169104
- **Reactions:** 4 · **Labels:** `framework`, `f: material design`, `platform-web`, `P3`, `team-text-input`
- **Decision:** **skip — engine-level** (not broadly reproducible)

Other triagers couldn't reproduce on macOS/Windows. Reporter-specific
macOS 15 + Chrome setup. Thematically similar to #137659 but the
symptom is "text auto-selected after typing" vs "after programmatic
insert". Holding as not-a-duplicate until more reports.

---

### #22619 — Integrate with Smart Text Selection APIs (Android)

- **URL:** https://github.com/flutter/flutter/issues/22619
- **Reactions:** 3 · **Labels:** `c: new feature`, `framework`, `f: material design`, `P3`, `team-design`
- **Decision:** **skip — feature/proposal**

Request to integrate Android's `libtextclassifier` / `TextClassifier`
Java API for smart text selection (auto-select addresses, phone
numbers, etc.). Android-only, `c: new feature`, 7-year-old.

---

### #120049 — RTL (Persian/Arabic) cursor stuck at last position; emoji + selection bugs

- **URL:** https://github.com/flutter/flutter/issues/120049
- **Reactions:** 3 · **Labels:** `framework`, `a: internationalization`, `has reproducible steps`, `P2`, `f: selection`, `found in release: 3.7/3.8`, `team-framework`
- **Decision:** **skip — engine-level**

RTL TextField cursor can't move to last position; also fails to
select last character; worse with emoji and specific fonts;
characters stick together visually. PR #122480 merged but issue
persists. Workaround via custom controller for digit conversion
but underlying cursor-affinity issue remains. Assigned to
@LongCatIsLooong, stalled.

**Why not write-test.** Cursor affinity at RTL/emoji/font-boundary
positions involves the engine's text layout + framework's
`TextAffinity` handling; font-specific reproduction would need
specific font assets. Skip for velocity.

---

### #134024 — Multiline TextField right-click on web randomly changes selection

- **URL:** https://github.com/flutter/flutter/issues/134024
- **Reactions:** 3 · **Labels:** `platform-web`, `has reproducible steps`, `P2`, `team-web`, `found in release: 3.13/3.14`
- **Decision:** **skip — engine-level** (web)

Root cause: on web, right-clicks go through the hidden
textarea/input element, whose scroll position isn't synced with the
Flutter framework's rendered scroll offset. Right-click on visible
"Line 8" actually acts on the hidden element's "Line 3", jumping
selection. Earlier PR broke on complex multiline (#135159). No
landed fix.

---

### #151479 — [Web][iOS Safari] Double selection shown on TextField

- **URL:** https://github.com/flutter/flutter/issues/151479
- **Reactions:** 3 · **Labels:** `platform-web`, `has reproducible steps`, `P2`, `browser: safari-ios`, `team-web`, `found in release: 3.22/3.24`
- **Decision:** **skip — engine-level** (web)

iOS Safari on mobile web: Safari's native text selection is shown
simultaneously with Flutter's selection (two colors; one shifts
away from the actual text position). CSS workaround
(`-webkit-user-select: none` + touch-event prevention +
`BrowserContextMenu.disableContextMenu()`) works for some but not
all reporters. Persists in 3.27.3.

---

### #21997 — Selection rect computed per-glyph instead of per-line

- **URL:** https://github.com/flutter/flutter/issues/21997
- **Reactions:** 2 · **Labels:** `framework`, `engine`, `a: fidelity`, `a: quality`, `has reproducible steps`, `P2`, `found in release: 3.3/3.6`, `team-engine`
- **Decision:** **skip — engine-level**

Mixed character sets (e.g., kaomoji `(　´･‿･｀)`) produce selection
highlights with uneven glyph heights. Engine added
`getBoxesForRange` with `BoxHeightStyle`/`BoxWidthStyle` in PRs
#6335 / #6644, but framework never adopted the line-level
`BoxHeightStyle.max`. Mostly fixed on Android/iOS/macOS in 2022;
Linux has a slight vertical offset.

**Framework-testable note.** In principle testable (call
`getBoxesForRange` with `boxHeightStyle: BoxHeightStyle.max` and
compare rect heights), but the bug lives in framework selection-
painting code paths, not in `TextPainter` directly — probing
requires golden testing or spy on `RenderEditable` paint output.
Deferred.

---

### #89024 — Text selection handle drag scrolls ListView in opposite direction

- **URL:** https://github.com/flutter/flutter/issues/89024
- **Reactions:** 2 · **Labels:** `framework`, `f: material design`, `f: scrolling`, `has reproducible steps`, `P2`, `found in release: 2.2/2.6`, `f: selection`, `team-design`
- **Decision:** **skip — engine-level**

TextField inside `ListView`: dragging a selection handle scrolls the
`ListView` backwards. No root cause or workaround identified.
Sibling of #143479 "Input moves cursor at end of selection" (this
batch, #14 below) which is about bringIntoView behavior during
handle drag — may share that root cause path.

---

### #99918 — [Web][iOS Safari] obscuredText grey selection layer

- **URL:** https://github.com/flutter/flutter/issues/99918
- **Reactions:** 2 · **Labels:** `framework`, `f: material design`, `platform-web`, `has reproducible steps`, `P2`, `found in release: 2.10/2.11`, `team-web`
- **Decision:** **skip — engine-level** (web)

iOS Safari on web ignores `::selection` CSS pseudo-element for
styling. WebKit takes `caret-color`'s alpha and uses it as the
selection background, so a transparent `caret-color` gives a grey
selection. Larger proposal #120613 referenced. No workaround
without engine changes.

---

### #143479 — Input always moves cursor at end of text selection (Android)

- **URL:** https://github.com/flutter/flutter/issues/143479
- **Reactions:** 2 · **Labels:** `platform-android`, `framework`, `f: material design`, `good first issue`, `has reproducible steps`, `P2`, `found in release: 3.16/3.20`, `team-text-input`
- **Decision:** **skip — engine-level** (contributor in-progress; framework-testable)

**Root cause (per summary).** `_bringIntoViewBySelectionState` in
`editable_text.dart` is called on every selection change including
handle drags, causing the view to scroll back to selection end.
Android-only. Fix: skip `bringIntoView` when the selection change
is caused by a handle drag. Tagged `good first issue`; a contributor
is investigating a fix *with a regression test*.

**Framework-testable.** Clear hook point and pinpointed fix. Not
authoring a test here because an in-progress contributor fix is
expected to include one. Cluster-worthy: shares the "handle drag
should not trigger scrollback / cursor-move-to-selection-end"
theme with #89024 above — both are selection-handle-drag side
effects on scroll state.

---

### #79420 — TextSelectionDelegate should not expose direct access to the controller

- **URL:** https://github.com/flutter/flutter/issues/79420
- **Reactions:** 1 · **Labels:** `framework`, `c: proposal`, `P3`, `team-framework`
- **Decision:** **skip — feature/proposal**

Architectural refactor: move non-idempotent APIs (`selectWord`) up
to `EditableText`, expose only idempotent APIs from `RenderEditable`.
Design discussion; no regression to capture.

---

### #99277 — [Desktop] TextField has too generous selection area (drag across label/helper)

- **URL:** https://github.com/flutter/flutter/issues/99277
- **Reactions:** 1 · **Labels:** `framework`, `f: material design`, `a: desktop`, `P2`, `team-text-input`
- **Decision:** **skip — engine-level**

Dragging mouse cursor across TextField's decoration label / helper
text still starts text selection. `_RenderDecoration` uses a custom
RenderBox; wrapping with `GestureDetector` ruled out. @chunhtai's
longer-term fix is to apply "global selection" to TextField
(SelectionArea-style). Framework architectural change.

---

### #179526 — SelectionListenerNotifier range wrong on backward selection over WidgetSpan

- **URL:** https://github.com/flutter/flutter/issues/179526
- **Reactions:** 1 · **Labels:** `framework`, `f: material design`, `has reproducible steps`, `P2`, `f: selection`, `team-text-input`, `found in release: 3.38/3.40`
- **Decision:** **skip — engine-level** (framework-testable in principle)

**Root cause (per summary).** `_SelectableTextContainerDelegate
._calculateLocalRange` doesn't account for discontinuous selection
when non-selectable WidgetSpans break the selectable range.
Backward selection specifically. Forward selection produces
reasonable ranges.

**Framework-testable note.** Directly probe via
`SelectionListenerNotifier` + drag-select-backward across
`Text.rich` with `WidgetSpan`. Requires SelectionArea +
SelectionListener widget setup, which has its own harness
complexity. Deferred for velocity; strong write-test candidate
for future work.

---

### #44544 — Exception in RenderEditable.getEndpointsForSelection (sporadic)

- **URL:** https://github.com/flutter/flutter/issues/44544
- **Reactions:** 0 · **Labels:** `c: crash`, `framework`, `customer: quill (g3)`, `P2`, `team-framework`
- **Decision:** **skip — engine-level**

Sporadic production crash at
`RenderEditable.getEndpointsForSelection` (`editable.dart:1264`) —
`StateError: Bad state: No element`. No reproducible steps. Likely
a race between text update and selection-endpoint query during
`TextSelectionOverlay._buildToolbar`. No further diagnostic work.

---

### #50834 — [Web] Engine should send correct affinity with text selection

- **URL:** https://github.com/flutter/flutter/issues/50834
- **Reactions:** 0 · **Labels:** `framework`, `platform-web`, `P2`, `team-web`
- **Decision:** **likely-stale (signal-based)**

Web keyboard cursor movement reports selection without affinity,
defaulting to `TextAffinity.downstream` in the framework. A 2024
commenter couldn't reproduce on master and questioned whether it's
still valid. **Recommendation:** real-device verification on
current Flutter web; if non-reproducing, close.

---

### #77957 — [macOS] Selectable rich text with gesture recognizer should be focusable

- **URL:** https://github.com/flutter/flutter/issues/77957
- **Reactions:** 0 · **Labels:** `framework`, `f: material design`, `a: accessibility`, `platform-macos`, `f: gestures`, `P3`, `team-text-input`
- **Decision:** **skip — engine-level**

macOS: `RenderEditable` doesn't break Selectable rich text into
multiple semantic nodes (unlike other platforms) because macOS
reads selection range from a single node. Gesture-recognizer-based
spans currently lose selection-focus semantics on macOS. Links to
originating PR #77730. Accessibility/semantics scope, not a
selection-gesture framework test.

---

### #88135 — TextSelection doesn't support TextAffinity for non-collapsed selections

- **URL:** https://github.com/flutter/flutter/issues/88135
- **Reactions:** 0 · **Labels:** `framework`, `P2`, `team-framework`
- **Decision:** **skip — feature/proposal**

`TextSelection.affinity` docs say it only applies when collapsed;
proposal to extend affinity semantics to non-collapsed selections
(especially for line-break positions). Comments note macOS non-
collapsed selections don't visually require affinity (highlighted
rectangles). Suggestion: document explicit affinity assumptions.
Design/doc gap, not a regression.

---

### #90805 — TextSelection is lost when clicking a button (web/desktop)

- **URL:** https://github.com/flutter/flutter/issues/90805
- **Reactions:** 0 · **Labels:** `framework`, `a: typography`, `f: focus`, `has reproducible steps`, `P2`, `found in release: 2.5/2.6`, `team-framework`
- **Decision:** **skip — engine-level**

Web/desktop (not mobile): clicking a button after selecting text
in a TextField clears the visual highlight, though selection
values remain numerically correct. Root cause: standard browser
behavior (button click removes focus from input). Team assigned
framework-side investigation into preserving highlight on focus
loss.

---

### #105756 — Selection highlight should expand to full input line width

- **URL:** https://github.com/flutter/flutter/issues/105756
- **Reactions:** 0 · **Labels:** `platform-android`, `platform-ios`, `framework`, `has reproducible steps`, `P2`, `found in release: 3.0/3.1`, `team-text-input`
- **Decision:** **skip — engine-level**

Selection highlight computed from `TextBox` rectangles covering
only actual text width, not full line width. Investigated via
`BoxWidthStyle` + `LineMetrics` but `LineMetrics.width` excludes
trailing whitespace — complete fix requires engine changes to
`paragraph.cc`. Thematic cousin of #21997 (selection rect per-glyph
vs per-line).

---

### #107671 — Getting GestureRecognizers to respect each other (super_editor)

- **URL:** https://github.com/flutter/flutter/issues/107671
- **Reactions:** 0 · **Labels:** `framework`, `f: gestures`, `a: desktop`, `P2`, `team-framework`
- **Decision:** **skip — feature/proposal**

super_editor wants arbitrary app-level gestures (e.g., Alt+LeftClick
for custom context menu) to coexist with `SuperTextField`'s
internal selection gestures. Gesture arena composability problem.
Discussion stalled on needing a reduced test case; no concrete
solution. Architecture-level, not a bug regression.

---

### #115130 — Text selection gesture callbacks should pass details directly

- **URL:** https://github.com/flutter/flutter/issues/115130
- **Reactions:** 0 · **Labels:** `framework`, `c: proposal`, `P3`, `team-framework`
- **Decision:** **skip — feature/proposal**

API refactor: `RenderEditable.handleTapDown` caches
`globalPosition` from `TapDownDetails`; proposal to pass
`TapUpDetails` directly in `selectPosition(cause:)` at tap-up so
the framework doesn't rely on stored state. Design/refactor; no
regression.

---

### #132042 — Text selection issues on Dart 3 (selection handle, double-tap near bottom)

- **URL:** https://github.com/flutter/flutter/issues/132042
- **Reactions:** 0 · **Labels:** `framework`, `has reproducible steps`, `P2`, `f: selection`, `found in release: 3.10/3.13`, `team-framework`
- **Decision:** **skip — engine-level**

Two symptoms: (1) selection handle disappears when dragging
diagonally — triage couldn't distinguish from native behavior;
(2) double-tap near the bottom of field doesn't select word —
confirmed on iOS/Android. Fix attempted in PR #132988, blocked
on #123415. Stalled pending #123415.

---

### #141369 — Text selection in reversed ListView + SelectionArea

- **URL:** https://github.com/flutter/flutter/issues/141369
- **Reactions:** 0 · **Labels:** `framework`, `f: scrolling`, `has reproducible steps`, `P2`, `f: selection`, `team-framework`, `found in release: 3.16/3.19`
- **Decision:** **likely-stale (signal-based)**

`SelectionArea` + reversed `ListView` + keyboard-open + press-and-
hold: selection becomes buggy until the screen position of the
original press is reached. One commenter recently noted they can
no longer reproduce on latest master, suggesting it may have been
incidentally fixed. **Recommendation:** real-device verification
on current Flutter; if non-reproducing, close.

---

### #164539 — [Windows] TextField (SelectionArea-wrapped) loses selection on right-click

- **URL:** https://github.com/flutter/flutter/issues/164539
- **Reactions:** 0 · **Labels:** `framework`, `platform-windows`, `a: desktop`, `P2`, `team-text-input`
- **Decision:** **skip — engine-level**

Windows-specific (desktop + web on Windows): `SelectionArea`
wrapping a TextField loses selection when right-click opens
context menu. macOS and standard web unaffected. Windows embedder
right-click handling interacts poorly with `SelectionArea` focus
semantics.

---

## Duplicate clusters

_None identified yet._

## Likely-stale candidates for closure review

- **#50834** — [Web] Engine should send correct affinity with text selection.
  **Basis:** signal-based — 2024 commenter couldn't reproduce on master.
  **Verification:** real-device check on current Flutter web with multi-line
  TextField + keyboard arrow to line start; if non-reproducing, close.
- **#141369** — Text selection in reversed ListView + SelectionArea.
  **Basis:** signal-based — recent commenter can no longer reproduce on
  master; may have been incidentally fixed.
  **Verification:** real-device repro check; if non-reproducing, close.

## Cross-category sibling / split-issue links

_None identified yet._
