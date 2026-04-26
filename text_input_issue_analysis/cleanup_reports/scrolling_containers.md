# Scrolling Containers and ensureVisible Cleanup Report

Iterative cleanup audit for the **Scrolling containers and ensureVisible with
text fields** category (24 open issues as of the `text_input_issues.json`
snapshot).

Format and workflow specified in
[`../CLEANUP_REPORT_FORMAT.md`](../CLEANUP_REPORT_FORMAT.md). Processed
**one issue at a time** in batches; order is reactions-descending.

**Category scope (per taxonomy).** Text fields living inside `ListView`,
`ScrollView`, `SingleChildScrollView`, `PageView`, `NestedScrollView`,
reversed lists, slivers, `InteractiveViewer`, `TabBarView`, and drawers:
bringing the caret into view, `keyboardDismissBehavior`, scroll-position
interactions, TextField not gaining focus after scroll, `scrollPadding`,
and scrollbar placement.

**Priors from previous categories (watch for overlap):**
- **#143479** (Selection gestures) — `_bringIntoViewBySelectionState` in
  `editable_text.dart` flicks scroll during handle drag. Directly in this
  category's surface.
- **#89024** (Selection gestures) — selection drag in `ListView` scrolls
  opposite. Same overlap — scroll + selection interaction.
- **#79497** (Hardware keyboard) — ExpansionTile + TextField backspace
  loses focus after scroll. Possible thematic cousin.

## Running summary — **CATEGORY COMPLETE**

- **Processed: 24 / 24** ✅
- Tests written: **2** (retained as framework-level gates)
  - Failed as expected (confirms issue is real): 1 (#58877 requestFocus-on-already-focused skips auto-scroll)
  - Pass-green, exercises bug path (likely-stale): 1 (#87124 mouse drag selects; bug path reached, selection extended)
- Skipped — feature/proposal: 3 (#56159, #97866, #89285)
- Skipped — engine-level: 17
- Skipped — needs native-platform verification: 0
- Likely-duplicate: 0
- Likely-stale candidates (no test, signal-based): 2 (#23198, #95541)
- Duplicate clusters (tentative): 0
- Cross-category sibling/split-issue links: 0

### Coverage summary
- **2 regression tests authored (8.3% write-test rate)** — highest of
  any category audited so far (IME/CJK 2.9%, Hardware keyboard 2.0%,
  Selection gestures 0%, Scrolling containers **8.3%**). Both tests
  run cleanly; one fails-as-expected (framework bug confirmed), one
  passes-green exercising the real bug path (stale signal).
- 3 skip-proposal (13%). Feature-completeness proposals around
  FormField keep-alive, Windows autoscroll semantics, and
  `ReorderableListView` keyboard dismiss.
- 17 skip-engine (71%). Dominated by web-platform (8/17 web issues)
  — scroll-sync between Flutter canvas and hidden textarea, iframe
  scroll isolation, host-page scroll propagation, mobile-browser tap
  jumps. The remaining 9 are split across framework-adjacent bugs
  with engine/embedder-scoped fixes (scrollPadding inside Drawer,
  NestedScrollView bringIntoView, SliverPersistentHeader scroll
  reset, SliverMainAxisGroup `isPinned` flag, iPad multi-finger
  gesture-arena, horizontal edge scrolling, iOS WebView keyboard).
- 2 likely-stale candidates — both with clear verification paths
  (#23198 fixed in 3.24.5+ per 2024 comment, #87124 framework
  gesture works in test).

### Hypothesis re-calibration
Going in I downgraded my per-category write-test predictions after
the two consecutive misses on Hardware keyboard and Selection
gestures. Scrolling containers landed at **8.3% write-test rate** —
meaningfully higher. Two hypotheses for *why* this category yielded
higher testability than the last two:

1. **ScrollController + FocusNode are framework-testable primitives.**
   Both provide direct programmatic inspection (scrollController
   .offset, focusNode.hasFocus) — scroll-into-view bugs are
   observable without gesture simulation. Selection-handle
   drags and hardware-key-event synthesis, by contrast, both required
   simulation primitives that `testWidgets` doesn't provide cheaply.

2. **Smaller web share than selection gestures.** Scrolling has 8/24
   (33%) web-specific issues vs selection gestures' 11/28 (39%).
   Not a huge gap, but the non-web scrolling issues more often have
   observable framework-state outputs than their selection-gesture
   counterparts.

### Framework-testable candidates I deferred
For future passes — each has a clean framework fix target but the
test scaffolding cost was above the per-batch threshold:

- **#62332** PageStorageKey + TextField inner-Scrollable interference
- **#50329** Scrollable.ensureVisible vs keyboard animation timing
- **#130259** SliverPersistentHeader scroll reset on keyboard show
- **#172437** scrollPadding inside Drawer
- **#145839** ScrollbarPainter `_totalTrackMainAxisOffsets` off-by-padding
- **#177453** SliverMainAxisGroup maxScrollObstructionExtent (PR #178809 in flight)

If someone were to invest in them later, I'd expect the per-issue
test to land in ~30-60 minutes each.

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

### #58877 — FocusNode.requestFocus on already-focused TextFormField doesn't auto-scroll

- **URL:** https://github.com/flutter/flutter/issues/58877
- **Reactions:** 16 · **Labels:** `framework`, `f: material design`, `f: scrolling`, `f: focus`, `has reproducible steps`, `P2`, `found in release: 3.3/3.7`, `team-design`
- **Decision:** **write-test** → **fail-as-expected** (bug confirmed)

**Root cause (per summary).** When the focus node already reports
`hasFocus`, Flutter skips the scroll-into-view path. Scenario: form
validation fails, code calls `requestFocus` on the errored field, but
the user has manually scrolled away — nothing scrolls back.

**Test approach.** `testWidgets` puts a `TextFormField` at the top of a
tall `SingleChildScrollView`, focuses it, scrolls ~800 px away via a
`ScrollController`, then calls `focusNode.requestFocus()` again on the
already-focused node. Asserts scroll offset returns near 0.

**Test:** [`issue_58877_requestfocus_already_focused_does_not_autoscroll_test.dart`](../regression_tests/scrolling_containers/issue_58877_requestfocus_already_focused_does_not_autoscroll_test.dart)

**Test outcome.** Fails as expected: `Actual: 800.0` vs `Expected: <50`
— scroll doesn't return. Framework-fixable; aligns with the summary's
root cause.

---

### #56159 — FormField in ListView: validation bypassed and text lost when scrolled out of view

- **URL:** https://github.com/flutter/flutter/issues/56159
- **Reactions:** 15 · **Labels:** `c: new feature`, `framework`, `f: material design`, `f: scrolling`, `has reproducible steps`, `P3`, `found in release: 3.3/3.7`, `team-framework`
- **Decision:** **skip — feature/proposal**

`ListView` disposes off-screen children, so FormField widgets scrolled
out of view are destroyed — their state is lost, their `validator` is
skipped. `SingleChildScrollView` avoids this. Workarounds:
`AutomaticKeepAliveClientMixin`, `KeepAlive` wrapper, switch to
`Column`+`SingleChildScrollView`. Team noted a possible opt-in
keep-alive configuration for form widgets. `c: new feature`-labeled;
design discussion rather than a regression.

---

### #41630 — [web] Support scrolling inside the text field (Flutter/browser out of sync)

- **URL:** https://github.com/flutter/flutter/issues/41630
- **Reactions:** 9 · **Labels:** `framework`, `f: scrolling`, `platform-web`, `P2`, `team-web`
- **Decision:** **skip — engine-level** (web)

Flutter's canvas TextField and the browser's hidden `<textarea>` scroll
independently and drift out of sync (especially Safari, which uses a
different default font than Roboto). Root cause: font mismatch +
framework-engine scroll-position synchronization gap. Prototypes exist
but no merged fix.

---

### #23198 — TextFormField editing cursor "balloon" floats over AppBar/TabBarView when scrolled

- **URL:** https://github.com/flutter/flutter/issues/23198
- **Reactions:** 6 · **Labels:** `framework`, `a: fidelity`, `f: scrolling`, `has reproducible steps`, `P2`, `found in release: 3.7/3.9`, `team-framework`
- **Decision:** **likely-stale (signal-based)**

Selection-handle "balloon" continues painting over AppBar and TabBarView
when the underlying TextFormField is scrolled away. A 2024 commenter
claimed the issue is fixed in Flutter 3.24.5 and newer (unverified by
team). **Recommendation:** real-device verification on current Flutter;
if non-reproducing, close.

---

### #97866 — [Windows] Proposal: missing TextField autoscroll behaviors

- **URL:** https://github.com/flutter/flutter/issues/97866
- **Reactions:** 5 · **Labels:** `c: new feature`, `framework`, `engine`, `platform-windows`, `c: proposal`, `a: desktop`, `a: mouse`, `P3`, `team-windows`
- **Decision:** **skip — feature/proposal**

Roadmap-style proposal enumerating missing behaviors: triple-click
paragraph selection, quad-click whole-field selection, mouse autoscroll
during selection drag, keyboard autoscroll with Shift+Arrow,
Ctrl+Home/End scroll to extremes, and Ctrl+Shift variants. `c: proposal`
/ `c: new feature`; feature-completeness roadmap.

---

### #50329 — Scrollable.ensureVisible can't bring button into view during keyboard show

- **URL:** https://github.com/flutter/flutter/issues/50329
- **Reactions:** 4 · **Labels:** `framework`, `f: scrolling`, `f: focus`, `has reproducible steps`, `P3`, `team-framework`, `found in release: 3.13/3.17`
- **Decision:** **skip — engine-level**

`Scrollable.ensureVisible` resolves immediately and doesn't account for
keyboard-animation delay, so code that tries to keep a Submit button
visible as the keyboard opens fails. A `FocusNode`-listener + `Timer`
delay workaround was tried but deemed unsuitable for production.
Requires embedder-driven keyboard-animation signaling that framework
ensureVisible currently ignores.

---

### #25972 — google_maps_flutter inside ListView with TextField: pinch/drag broken after keyboard dismiss

- **URL:** https://github.com/flutter/flutter/issues/25972
- **Reactions:** 3 · **Labels:** `framework`, `f: scrolling`, `f: gestures`, `p: maps`, `package`, `team-ecosystem`, `has reproducible steps`, `P2`, `found in release: 1.20/2.0/2.2`
- **Decision:** **skip — engine-level**

After TextField loses focus and keyboard dismisses, subsequent
pinch/drag gestures on the Google Maps platform view are not handled.
Workaround: add `EagerGestureRecognizer` to `GoogleMap`. Package-level
interaction (google_maps_flutter PlatformView + ListView + TextField
gesture-arena), firmly engine/ecosystem scope.

---

### #118558 — [Flutter Web][Android Chrome in iframe] ListView freezes after scroll

- **URL:** https://github.com/flutter/flutter/issues/118558
- **Reactions:** 2 · **Labels:** `framework`, `f: scrolling`, `platform-web`, `has reproducible steps`, `P2`, `browser: chrome-android`, `found in release: 3.3/3.7`, `team-web`
- **Decision:** **skip — engine-level** (web)

Flutter web inside an `<iframe>` on Android Chrome: after scrolling a
`ListView`/`SingleChildScrollView`, the scrollable loses gesture
hit-testing — nothing inside the scroll area can be focused. Sibling
widgets outside remain interactive. Workaround: don't embed in an
iframe. Web engine DOM gesture hit-test issue.

---

### #62332 — ListView with PageStorageKey + TextField doesn't keep scroll position

- **URL:** https://github.com/flutter/flutter/issues/62332
- **Reactions:** 1 · **Labels:** `framework`, `f: material design`, `f: scrolling`, `has reproducible steps`, `P2`, `found in release: 3.3/3.7`, `team-design`
- **Decision:** **skip — engine-level** (framework-testable; known workaround)

`TextField` contains an internal `Scrollable`; that inner Scrollable
interferes with `PageStorage`, causing the outer `ListView`'s scroll
position to reset on every other open/close cycle. Workaround:
add a `PageStorageKey` to the `TextField` itself. @xu-baolin referenced
a framework-side improvement; open pending that.

**Framework-testable note.** Directly write-testable: pump a ListView
with PageStorageKey containing a TextField, scroll, rebuild via
navigate-away-and-back, check offset. Deferred for velocity; strong
write-test candidate if revisited.

---

### #64059 — Horizontal edge scrolling broken in TextField

- **URL:** https://github.com/flutter/flutter/issues/64059
- **Reactions:** 1 · **Labels:** `c: contributor-productivity`, `platform-android`, `platform-ios`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `c: tech-debt`, `team: skip-test`, `f: selection`, `found in release: 3.3/3.7`, `team-text-input`
- **Decision:** **skip — engine-level** (known tech-debt; test skipped)

Selection handle dragged to the right edge of a single-line TextField
should autoscroll horizontally; doesn't. Root cause suspected to be
pointer leaving the full-width field's hit-test area, ending the
gesture. Currently `c: tech-debt` with a skipped test
(`team: skip-test` label). Android mostly affected; iOS mostly works.

---

### #89285 — Dismiss keyboard on ReorderableListView drag start

- **URL:** https://github.com/flutter/flutter/issues/89285
- **Reactions:** 1 · **Labels:** `c: new feature`, `framework`, `f: material design`, `c: proposal`, `team-design`
- **Decision:** **skip — feature/proposal**

Proposal to add a `keyboardDismissBehavior`-style option for
`ReorderableListView` drag-start. Linked to #76170. `c: proposal`.

---

### #126900 — [Web mobile] Scrolling IFrameElement with physical keyboard scrolls Scaffold

- **URL:** https://github.com/flutter/flutter/issues/126900
- **Reactions:** 1 · **Labels:** `framework`, `f: scrolling`, `platform-web`, `f: focus`, `has reproducible steps`, `P2`, `browser: safari-ios`, `browser: chrome-android`, `found in release: 3.10/3.11`, `team-web`
- **Decision:** **skip — engine-level** (web)

Flutter web + mobile (Chrome Android, Safari iOS) + physical
keyboard + `IFrameElement`/`Element.html`: scrolling the iframe
scrolls the entire `Scaffold`. Web engine gesture routing.

---

### #130259 — CustomScrollView SliverPersistentHeader TextField scroll reset on keyboard show

- **URL:** https://github.com/flutter/flutter/issues/130259
- **Reactions:** 1 · **Labels:** `framework`, `f: scrolling`, `has reproducible steps`, `P2`, `found in release: 3.10/3.12`, `team-framework`
- **Decision:** **skip — engine-level**

Floating `SliverPersistentHeader` with `TextField` child: tapping the
field activates the keyboard, which resets the header's scroll
position. Android + iOS. @LongCatIsLooong pinged. No fix.

**Framework-testable note.** Could test by pumping
`CustomScrollView` with floating header + TextField, simulating
focus + viewInsets change, asserting scroll position. Deferred —
viewInsets-change simulation in `testWidgets` is tricky.

---

### #159580 — Text overlaps scrollbar in web/desktop TextField

- **URL:** https://github.com/flutter/flutter/issues/159580
- **Reactions:** 1 · **Labels:** `framework`, `f: material design`, `platform-web`, `a: desktop`, `has reproducible steps`, `P2`, `team-text-input`, `found in release: 3.24/3.27`
- **Decision:** **skip — engine-level**

`TextFormField(maxLines: 2, minLines: 1)`: when content exceeds 2
lines the internal scrollbar appears but overlaps the text content.
Text selection also overlaps. Workaround: wrap TextField in
`Scrollbar`. Web + desktop. Still reproducible in 3.38.2.

---

### #172437 — TextField scrollPadding not applied inside Drawer

- **URL:** https://github.com/flutter/flutter/issues/172437
- **Reactions:** 1 · **Labels:** `framework`, `f: material design`, `f: scrolling`, `has reproducible steps`, `P2`, `team-text-input`, `found in release: 3.32/3.33`
- **Decision:** **skip — engine-level**

TextField inside a Drawer's ListView: `scrollPadding` is ignored when
the keyboard opens; keyboard covers the field. Workaround: wrap the
Drawer's ListView in a Padding using `MediaQuery.viewInsetsOf` and
manually handle bottom padding. Framework focus-aware scroll logic
doesn't traverse into Drawers. No PR.

**Framework-testable note.** Could test by pumping Scaffold+Drawer+
ListView+TextField, opening Drawer, focusing TextField with
simulated viewInsets, asserting scroll position respects
scrollPadding. Deferred for the same viewInsets-simulation
complexity as #130259.

---

### #70947 — TextField in NestedScrollView scrolls editing line out of view

- **URL:** https://github.com/flutter/flutter/issues/70947
- **Reactions:** 0 · **Labels:** `framework`, `f: material design`, `f: scrolling`, `has reproducible steps`, `P2`, `found in release: 3.3/3.6`, `team-design`
- **Decision:** **skip — engine-level**

Multiline TextField inside `NestedScrollView` on Android: editing
lines beyond the first scrolls them out of the viewport. Linked to
#37721. Framework bringIntoView interaction with nested scroll
controllers. Stalled.

---

### #87124 — Mouse drag in multiline TextField scrolls instead of selecting

- **URL:** https://github.com/flutter/flutter/issues/87124
- **Reactions:** 0 · **Labels:** `framework`, `a: fidelity`, `f: scrolling`, `has reproducible steps`, `P2`, `found in release: 2.2`, `team-framework`
- **Decision:** **write-test** → **pass-green, exercises bug path (likely-stale candidate)**

**Root cause (per issue).** Vertical mouse drag inside a multiline
TextField should extend a selection — native behavior on macOS
desktop and standard browsers. Flutter was reported as scrolling the
inner viewport instead.

**Test approach.** `testWidgets` on `TargetPlatform.macOS`, multiline
TextField (maxLines=3), focus, then start a mouse-kind gesture
inside the field and drag vertically downward ~40 px. Assert
`controller.selection.isCollapsed` is false after drag.

**Test:** [`issue_87124_mouse_drag_scrolls_instead_of_selecting_test.dart`](../regression_tests/scrolling_containers/issue_87124_mouse_drag_scrolls_instead_of_selecting_test.dart)

**Test outcome.** Passes — selection is non-collapsed after the drag.
The test exercises the real code path (TextSelectionGestureDetector
mouse-pointer handling); a pass-green here is a meaningful staleness
signal, unlike #98720 in IME/CJK where the test bypassed the
embedder-side bug. Recommendation: real-device verification on
macOS desktop and browser-canvas-web builds, then close if
non-reproducing.

---

### #95541 — [Web][iOS 12/13 Safari] TextField delete/scroll broken

- **URL:** https://github.com/flutter/flutter/issues/95541
- **Reactions:** 0 · **Labels:** `platform-ios`, `framework`, `platform-web`, `e: OS-version specific`, `P2`, `browser: safari-ios`, `team-framework`
- **Decision:** **likely-stale (signal-based)**

iOS 12 / iOS 13 on Safari (HTML renderer only; CanvasKit doesn't
work at all on those versions). Deletion and scroll broken.
iOS 12 released 2018 / iOS 13 released 2019 — very old versions.
Labeled P4; team can't reproduce without the devices. Related
#92183. **Recommendation:** close given OS-version age; iOS 14+ is
unaffected.

---

### #133743 — iPad multi-finger gesture-arena lockup on TextFormField inside ListView

- **URL:** https://github.com/flutter/flutter/issues/133743
- **Reactions:** 0 · **Labels:** `framework`, `f: material design`, `f: scrolling`, `P2`, `team-design`
- **Decision:** **skip — engine-level**

iPad-specific (iPhone and Android unaffected). Finger held on
multi-line TextFormField while another finger scrolls outside the
field → gesture arena lockup. Previously assigned to
@Renzo-Olivares, unassigned due to inactivity.

---

### #145839 — Scrollbar doesn't reach bottom of TextField

- **URL:** https://github.com/flutter/flutter/issues/145839
- **Reactions:** 0 · **Labels:** `framework`, `f: material design`, `f: scrolling`, `has reproducible steps`, `P3`, `found in release: 3.19/3.21`, `team-text-input`
- **Decision:** **skip — engine-level** (clear framework fix pinpointed)

Mobile-only (iOS + Android; macOS unaffected). Root cause:
`ScrollbarPainter._totalTrackMainAxisOffsets` uses `padding.vertical`
instead of `0`. Workarounds: `SafeArea` wrap, or `MediaQuery
.removePadding(removeBottom: true)`. Clear framework fix pinpointed;
no PR yet.

---

### #152547 — [iOS][WebView] TextFields covered by keyboard after switching fields

- **URL:** https://github.com/flutter/flutter/issues/152547
- **Reactions:** 0 · **Labels:** `platform-ios`, `f: scrolling`, `has reproducible steps`, `P2`, `team-ios`, `found in release: 3.22/3.24`
- **Decision:** **skip — engine-level**

iOS-only (Android unaffected): inside `webview_flutter`, switching
between text inputs causes the scaffold to resize then reset to full
size, leaving the focused field under the keyboard. SwiftUI native
behavior differs but allows scrolling. Related to #112354. iOS
plugin + WebView scaffold-resize coordination.

---

### #163607 — [Web][mobile Chrome/Safari] Screen jumps to end/middle on TextField tap

- **URL:** https://github.com/flutter/flutter/issues/163607
- **Reactions:** 0 · **Labels:** `platform-web`, `has reproducible steps`, `P2`, `team-web`, `found in release: 3.29/3.30`
- **Decision:** **skip — engine-level** (web)

Mobile Chrome/Safari: tapping a multi-line TextField to activate the
soft keyboard jumps the screen to the end (Chrome) or middle (Safari)
of the text. Narrowed to scroll position × line-count × viewport
interaction. Linked to #124483, #162231 (batch 1 here), #162698.
Web engine soft-keyboard + scroll handling.

---

### #167411 — [Web] Scroll wheel over enabled TextField propagates to host page

- **URL:** https://github.com/flutter/flutter/issues/167411
- **Reactions:** 0 · **Labels:** `f: scrolling`, `platform-web`, `has reproducible steps`, `P2`, `team-web`, `found in release: 3.29/3.32`
- **Decision:** **skip — engine-level** (web)

Flutter web embedded in a `<div>` on a scrollable host page: wheel
scroll events over enabled TextField widgets propagate out and
scroll the host page. Disabling the TextField stops propagation.
Related to #159680, #159358, engine PR #53922. Web engine event-
propagation work.

---

### #177453 — SliverMainAxisGroup breaks showOnScreen from descendant TextField

- **URL:** https://github.com/flutter/flutter/issues/177453
- **Reactions:** 0 · **Labels:** `framework`, `f: scrolling`, `has reproducible steps`, `P2`, `team-framework`, `found in release: 3.35/3.38`
- **Decision:** **skip — engine-level** (PR in review)

**Root cause (per reporter).** `RenderSliverMainAxisGroup` doesn't
report `maxScrollObstructionExtent` in its geometry, so `isPinned`
is false in `getOffsetToReveal`, causing `showOnScreen` to calculate
leading offset as 0 → scrolls to top. Clear framework fix target;
**PR #178809** proposed and awaiting review. Retaining as
skip-engine to avoid redundant test authoring while the PR is in
flight; the PR almost certainly includes a regression test.

**Framework-testable.** Directly write-testable (pump
`CustomScrollView` with `SliverMainAxisGroup` containing a
pinned header sliver with a TextField descendant; trigger tap on
TextField; assert scroll doesn't jump to top). Deferred pending
PR #178809.

---

## Duplicate clusters

_None identified yet._

## Likely-stale candidates for closure review

- **#23198** — TextFormField cursor "balloon" floats over AppBar/TabBarView.
  **Basis:** signal-based — 2024 commenter claimed issue is fixed in Flutter
  3.24.5+. Unverified by team.
  **Verification:** real-device repro on current stable; if non-reproducing,
  close with pointer to the version that fixed it.
- **#87124** — Mouse drag in multiline TextField scrolls instead of selecting.
  **Basis:** test-pass (framework-level `testWidgets` exercises the mouse-drag
  → TextSelectionGestureDetector path; selection IS extended). Unlike earlier
  embedder-below test-passes, this one exercises the bug's actual code path.
  **Verification:** real-device check on macOS desktop and canvas-web builds
  (the two platforms the issue explicitly calls out). If both confirm
  non-reproducing, close.
- **#95541** — [Web][iOS 12/13 Safari] TextField delete/scroll broken.
  **Basis:** signal-based — affects only iOS 12 (2018) and iOS 13 (2019),
  which are ~6 years old. CanvasKit doesn't run on those versions. Labeled
  P4; team lacks devices.
  **Verification:** none practical; close given the OS-version age.

## Cross-category sibling / split-issue links

_None identified yet._
