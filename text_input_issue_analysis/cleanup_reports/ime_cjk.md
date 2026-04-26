# IME/CJK Cleanup Report

Iterative cleanup audit for the **IME, CJK composing, and dead keys/accents**
category (104 open issues as of the `text_input_issues.json` snapshot).

Format and workflow specified in
[`../CLEANUP_REPORT_FORMAT.md`](../CLEANUP_REPORT_FORMAT.md). Processed
**one issue at a time**; order is reactions-descending within the category.
Per-issue entries record decision, reasoning, dedup scan, and (when
applicable) the authored regression test and its outcome.

## Running summary — **CATEGORY COMPLETE**

- **Processed: 104 / 104** ✅
- Tests written: 3 (retained as framework-level gates)
  - Failed as expected (confirms issue is real): 1 (#19584 — also covers #123065 via shared API)
  - Passed green but does not exercise the real bug path: 1 (#98720)
  - Test-error (harness setup): 1 (#92050)
- Skipped — feature/proposal: 9
- Skipped — engine-level: 76
- Skipped — needs native-platform verification: 2 (#9343, #105028)
- Likely-duplicate: 13 (adds #171319 → #92050 [DSK-IME-1])
- Likely-stale candidates (no test, signal-based): 2 — #145887 (Gboard-upstream-fix), #156183 (iOS 18 fixed + Apple-side bug)
  - Watchlist: #149379 possibly fixed by #166291 — needs real-device verification
- Duplicate clusters (tentative): **10** — DK-1 (5 members) · WKI-1 (5 members) · DSK-IME-1 (5 members) · CWB-1 (2) · MCIME-1 (6 members, biggest) · CRC-1 (3) · IHK-1 (3) · AIR-1 (3) · CSR-1 (5 members) · DKD-1 (2)
- Cross-category sibling/split-issue links: 1 (#98720 ↔ #184744)

### Coverage summary
- 10 shared-root-cause / shared-surface clusters cover **38 of 104 issues** (~37%).
- 13 likely-duplicates recommend concrete merge actions.
- 2 likely-stale candidates recommend closure review.
- 76 skip-engine issues have their fix layer clearly identified as engine/embedder; several have specific file/class/method pinpoints documented.
- 3 regression tests authored (1 confirms #19584/#123065 real via TextPainter.getWordBoundary; 1 retained as framework gate for #98720; 1 shell for #92050 pending harness rework).

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
  don't have (e.g. current iOS composing-range style). Deferred.
- **likely-stale (signal-based)** — framework testing not feasible and
  age + inactivity + framework evolution strongly suggest no longer valid.
- **likely-duplicate** — same root cause as another in-category issue;
  canonical identified, merge recommended.

## Processed issues

### #150460 — Expose low level IME interactions

- **URL:** https://github.com/flutter/flutter/issues/150460
- **Created:** 2024-06-18 (~1.8 y old) · **Updated:** 2025-02-18
- **Reactions:** 31 (👍 25, ❤️ 4, 👀 2)
- **Labels:** `a: text input`, `c: proposal`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Reasoning.** The issue is a formal design proposal (`c: proposal` label,
"Use case / Proposal / Open questions" body template, and the comment summary
confirms an in-depth design discussion with @matthew-carroll and @knopp). It
asks for platform-channel IME methods to mirror native platform APIs verbatim
instead of being abstracted in the engine — an architectural direction,
not a bug. There is no regression to capture in a widget test; this belongs
to separate API-design work.

**Dedup scan.** Comment summary cites two related issues: #150068 ("Support
iOS 18 formatting menu") which is in the *Selection toolbar* category and
unrelated, and #150525 ("merged-thread approach") which is not in this
dataset (likely closed or untagged). No duplicate within the IME/CJK
category to merge here.

---

### #19584 — No word-breaks for CJK locales

- **URL:** https://github.com/flutter/flutter/issues/19584
- **Created:** 2018-07-19 (~7.8 y old) · **Updated:** 2024-04-10
- **Reactions:** 11 (👍 11)
- **Labels:** `a: text input`, `engine`, `a: internationalization`, `a: china`, `has reproducible steps`, `P3`, `team-engine`, `triaged-engine`, `found in release: 3.19`, `found in release: 3.22`
- **Ownership:** `team-engine`
- **Decision:** **write-test** → **fail-as-expected** (issue confirmed real)

**Root cause (per comment summary).** Flutter's bundled `icudtl.dat` uses
Chromium's Android ICU build, which omits the CJK dictionary required for
word-break detection. Including it would add ~1.9 MB uncompressed. Proposed
fixes: bundle CJK dictionary, per-platform ICU builds, or delegate to
platform tokenizers (`CFStringTokenizer` / `BreakIterator`).

**Test approach.** Although the fix lands in the engine, the observable
behavior is exercisable from the framework via
`TextPainter.getWordBoundary(TextPosition)` — the same API the framework uses
to resolve long-press/double-tap word selection. Two assertions: Chinese
"你好吗" should group "你好" as one word; Japanese "日本語学校" should group
"学校" as one word.

**Test:** [`issue_19584_no_word_breaks_for_cjk_locales_test.dart`](../regression_tests/ime_cjk/issue_19584_no_word_breaks_for_cjk_locales_test.dart)

**Test outcome.** Both assertions fail — `TextPainter.getWordBoundary`
returns a 1-character range in both cases, confirming the engine's
tokenizer still treats each CJK glyph as its own word. The expected
post-fix behavior (multi-character word ranges) is not reached. Issue
remains real.

**Dedup scan.** No tight duplicates from the comments' cross-references
(the thread is self-contained). Broader category dedup will revisit word-break /
CJK-tokenization issues in aggregate once more are processed.

**Cluster update (post-batch-3).** Identified a tight duplicate:
**#123065** "CJK word boundaries" (ctrl/option+arrow on desktop moves by
char instead of word) — same ICU-CJK-dictionary root cause, same fix.
The regression test here already fails on the shared API
(`TextPainter.getWordBoundary`). New cluster **CWB-1** (CJK word breaks)
formed with this issue as canonical.

---

### #59541 — TextField should support typing accented words with external keyboard

- **URL:** https://github.com/flutter/flutter/issues/59541
- **Created:** 2020-06-16 (~5.8 y old) · **Updated:** 2026-02-06
- **Reactions:** 15 (👍 15)
- **Labels:** `a: text input`, `framework`, `engine`, `f: material design`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 3.7`, `found in release: 3.9`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause (per repro + comment summary).** With an external keyboard set
to a dead-key layout (e.g. Spanish, Portuguese-BR, French-CA, Czech,
Vietnamese), typing a dead key followed by a base letter should emit one
composed character (`à`). On Flutter iOS/Android the embedder does not
combine the events, so two characters surface (`\`` + `à`). A Windows fix
already exists — `CharacterCombiner` in `KeyboardManager.java`
(engine PR flutter/engine#27921) — but was never ported to iOS/Android.

**Why engine-level.** The missing combiner lives in the platform embedder's
key-event pipeline. By the time key events reach the framework
(`HardwareKeyboard`) or text surfaces (`TextInputClient.updateEditingValue`),
they have already been through the embedder. `tester.sendKeyEvent(...)` in a
`testWidgets` bypasses embedder processing entirely, and
`tester.enterText(...)` goes straight to `updateEditingValue` and skips the
key-event path. There is no framework-level vantage point where the
combiner's absence yields observable behavior a `testWidgets` could capture.
A real regression test has to live in the engine repo against
`KeyboardManager` directly.

**Dedup scan.** Strong duplicate candidate within IME/CJK:

- **#146486** — "Composing characters (e.g. Umlauts) using physical keyboard on
  iOS generates two [characters]" (1 reaction). Same symptom, same layer,
  same proposed fix family. Recommend merge into #59541 (older + much higher
  reactions + more detailed discussion history).

Weaker candidates to revisit when we reach them (same broad family but
possibly different sub-causes):

- #103136 (Android Samsung accents via soft keyboard — may be different path)
- #154055, #154160 (dead keys producing wrong characters on desktop)
- #156183 (iOS dead-key delete behavior — different symptom)
- #87257 (iPad soft-keyboard accents)

Status notes: despite the skip here, this is a high-impact issue (15
thumbs-up, 6-year-old, "significant business impact" per reporters) with a
known-good Windows fix ready to port. Worth surfacing to the team-text-input
/ team-engine roadmap outside this cleanup experiment.

---

### #74547 — Support IME reconversion on Windows

- **URL:** https://github.com/flutter/flutter/issues/74547
- **Created:** 2021-01-23 (~5.2 y old) · **Updated:** 2025-10-09
- **Reactions:** 30 (👍 30)
- **Labels:** `a: text input`, `a: internationalization`, `platform-windows`, `a: desktop`, `P2`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **skip — engine-level**

**Root cause / scope.** Unimplemented Win32 functionality in the Windows
embedder. The follow-up patch to engine PR #23853 (IME support) never
handled the `WM_IME_REQUEST` message's three sub-types:
`IMR_RECONVERTSTRING`, `IMR_DOCUMENTFEED`, `IMR_QUERYCHARPOSITION`. These
are the messages IMEs use to (a) feed surrounding document context into the
candidate window, (b) reconvert already-committed text, and (c) place the
candidate window near the caret.

**Why engine-level.** Implementation is pure Win32 message-loop code in the
Windows embedder (C++). The framework has no visibility into
`WM_IME_REQUEST`. A `testWidgets` can't simulate Win32 messages or drive a
real IME's reconversion flow; a meaningful regression would need an engine
unit test or an integration test on Windows hardware with a CJK IME.

**Dedup scan.** No other IME/CJK issue references reconversion,
`WM_IME_REQUEST`, or `IMR_*` messages directly. Standalone feature gap.
(The broader set of Windows-IME issues — Sogou candidate-window positioning,
Japanese/Korean composing bugs, etc. — shares the embedder but not the
specific root cause here.)

---

### #9343 — Multi-step input composing range incorrectly styled on iOS

- **URL:** https://github.com/flutter/flutter/issues/9343
- **Created:** 2017-04-12 (~9.0 y old) · **Updated:** 2024-03-21
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `platform-ios`, `framework`, `a: internationalization`, `a: fidelity`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.5`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip-test — needs native-platform verification**

**What the issue says.** Flutter renders the IME composing region with a
thin black underline; native iOS renders it differently (historically a
light selection-style highlight; more recently, in iOS 17, a thick blue
underline per the comment summary). An `a: fidelity` gap.

**Why not a write-test.** The gap is technically framework-testable — the
composing-region style is framework-rendered and can be probed via a
`testWidgets` that places a `TextField` in composing state and inspects the
painted decoration. What we *cannot* do without further work is encode the
*expected* style. The comment summary itself notes that native iOS's
composing style has drifted over the issue's 9-year lifespan (macOS 14
Sonoma moved closer to Flutter's underline; iOS 17 uses a thick blue
underline). Writing a test now would just serialize a guess. Verifying the
current native iOS (and macOS) composing style against a real device first
is a prerequisite.

**Status.** Likely still valid (comment summary confirms repro on 3.3 and
3.5 with Japanese IME on iOS; no fix landed). Not stale. Deferred for
native-baseline confirmation before a regression test is authored.

**Dedup scan.** Closest cousin is #151097 ("[flutter web] highlight of
characters is incorrect on composing mode") — same general *fidelity*
theme (composing-region styling) but a web-specific root cause, not an
iOS-composing-style duplicate. No tight duplicate within IME/CJK.

**Related thematic thread.** The `a: fidelity` label is a useful signal —
other IME/CJK issues carrying it may be similar "styling parity gap" cases
that also need native baselines before a test can be written.

---

### #98720 — [Android] TextField cursor doesn't move to tapped position after selecting input mode from virtual keyboard

- **URL:** https://github.com/flutter/flutter/issues/98720
- **Created:** 2022-02-18 (~4.2 y old) · **Updated:** 2026-04-08
- **Reactions:** 30 (👍 29, 👀 1)
- **Labels:** `a: text input`, `e: device-specific`, `platform-android`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `e: samsung`, `found in release: 3.0`, `found in release: 3.1`, `f: selection`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level** (revised; see process note below)
  - **Test still authored** as a framework-level regression gate — it
    passes today, but that is consistent with the bug living *below* the
    framework rather than with staleness. Retained for future use.

**Root cause (per #184744 body + #98720 raw comments).** Flutter's Android
embedder class `KeyEmbedderResponder`
(`shell/platform/android/io/flutter/embedding/android/KeyEmbedderResponder.java`)
synthesizes a `ShiftRight` key-down when the on-screen keyboard delivers an
event with a non-zero Shift `metaState` — but does not synthesize the
matching key-up. The framework sees a stuck "shift held" state, so
subsequent taps route through shift-extend-selection. Triggers vary by
keyboard software: older Samsung Keyboard's symbols-pane switch
(original #98720), newer Gboard's shift-to-capitalize / shift-tap feature
(new issue #184744, also regression against Flutter main).

**Fix location.** The synthesization lives in `KeyEmbedderResponder.java`
on the Android embedder. A framework-side sanity check (e.g. force meta-
state synchronization before text events) was discussed as a mitigation
but the authoritative fix is in the embedder's key-event synthesis path.

**Why the framework test passes.**
[`issue_98720_android_textfield_cursor_doesnt_move_to_tapped_position_test.dart`](../regression_tests/ime_cjk/issue_98720_android_textfield_cursor_doesnt_move_to_tapped_position_test.dart)
uses `tester.sendKeyDownEvent(LogicalKeyboardKey.shiftRight)` which pokes
the framework's `HardwareKeyboard` state directly, *bypassing* the
embedder's `KeyEmbedderResponder` synthesis step. So the test simulates a
scenario (framework has stuck shift state) and verifies Flutter's current
tap-in-TextField behavior doesn't mis-extend under it. It never touches
the real buggy path. A meaningful regression test has to live in the
engine repo against `KeyEmbedderResponder` directly.

**Strong cross-category sibling:** **#184744** — "[Android] Tapping Shift
gets stuck into change-selection state" (P1, `c: regression`, `team-android`,
created 2026-04-08). Filed by @gnprice from #98720 comment [49] as an
explicit split for the Gboard variant, naming `KeyEmbedderResponder` as
the fix target. It was classified into the **"Hardware keyboard, key
events, and shortcuts"** category — outside this cleanup's IME/CJK scope.
Our per-category dedup scan did not find it.

**Process learnings from this issue:**

1. **Summary compression can erase layer/owner signals.** The raw
   comments on #98720 were explicit that event synthesis is "done on the
   engine side" (comment [41]) and named `KeyEmbedderResponder.java`. The
   summary captured the mechanism (stuck shift, metaState synchronization)
   but did not preserve the engine-side framing — which caused me to
   initially classify this as framework-testable. *Going forward: when
   discussion in the summary mentions `metaState`, `keycode`, or platform
   files by name, check raw comments before committing to a framework
   classification.*

2. **Per-category dedup misses cross-category siblings.** The same root
   cause can land in different taxonomy categories depending on how each
   reporter framed the repro (#98720 "after selecting input mode from
   virtual keyboard" → IME/CJK; #184744 "[Android] Tapping Shift gets
   stuck" → Hardware keyboard). *Observation only for now:* the cleanup
   pass is scoped to one category at a time, so this gap is accepted.
   Cross-category sibling links we stumble on (like this one) are captured
   in the Cross-category links section below. A dedicated cross-category
   dedup pass is out of scope for the per-category workstream.

**Other IME/CJK neighbors (unchanged from earlier scan, kept for future
review):** #103136, #120351, #125765 — Samsung/Android keyboard-adjacent
issues with different symptoms; not siblings of this one.

---

### #140739 — When entering Korean, the text cursor is behind single space

- **URL:** https://github.com/flutter/flutter/issues/140739
- **Created:** 2023-12-29 (~2.3 y old) · **Updated:** 2026-04-14
- **Reactions:** 10 (👍 10)
- **Labels:** `a: text input`, `engine`, `a: internationalization`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 3.16`, `found in release: 3.18`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **skip — engine-level**

**Root cause (per comment summary + labels).** A Windows-specific, Korean-
specific regression first seen in 3.16. Korean IME on Windows composes
characters in-place (vs the buffered composition other CJK IMEs use), and
the Windows embedder's IME message handling miscalculates the composing-
caret offset so the caret is drawn one position ahead of where it should
be. The text content itself is correct; only the visual caret x-position
is wrong during composing.

**Why engine-level.** The bug only manifests on Windows (not web, not
macOS) and only with Korean IME (Japanese and Chinese are fine). The
platform × IME fingerprint is a clear embedder tell — the fix has to be in
the Windows embedder's IME handling code (how it reports the composing
region / caret position via platform-channel updates to the framework).
The framework merely renders the caret at the offset the embedder hands
it. A framework `testWidgets` cannot drive the Windows IMM32/Korean IME
composition pipeline; any regression test has to live in the engine's
Windows embedder tests or be a Windows device integration check.

**Dedup scan — Windows Korean IME family.** There is a cluster of five
Windows + Korean IME issues that share the same embedder surface but have
distinct symptoms:

- **#140739** (this issue) — composing caret drawn one position ahead
- **#121376** (6 reactions) — "Editable Text after clear has issue with
  buffer korean input"; referenced as related from #140739's comments
- **#130559** (5 reactions) — backspace + maxLength with Korean IME
- **#140537** (0 reactions) — 3-set Korean keyboard, space-bar ignored
- **#166400** (1 reaction) — Korean-to-Hanja conversion on Windows

Not tight duplicates (different symptoms). Likely a **shared-root-cause
cluster**: all touch the Windows embedder's Korean IME code paths
(composing region state, caret offset computation, conversion handling).
One fix pass on the Windows embedder's IME handling could plausibly
address multiple. Captured below as a tentative cluster; will tighten as
the other four are processed.

---

### #92050 — [Windows, IME] Sogou input dropdown is mispositioned after committing

- **URL:** https://github.com/flutter/flutter/issues/92050
- **Created:** 2021-10-19 (~4.5 y old) · **Updated:** 2025-10-09
- **Reactions:** 7 (👍 7)
- **Labels:** `a: text input`, `engine`, `a: internationalization`, `a: fidelity`, `platform-windows`, `a: desktop`, `a: annoyance`, `from: china`, `P2`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **write-test** → **test-error (harness setup)** — bug diagnosis pinpointed to framework code; test needs platform-channel interception rework before it can distinguish buggy-vs-fixed behavior.

**Root cause (per C1 raw-comment review — comment [13]).** Pinpointed in
`packages/flutter/lib/src/widgets/editable_text.dart` line 5021:
```dart
final int offset = composingRange.isValid ? composingRange.start : 0;
```
When `composingRange` is invalid — which is always the case with Sogou,
since it composes in its own window and never populates Flutter's
composing range — the fallback offset is `0`, putting the rect at the
top-left of the field. Sogou listens near commit events to position its
candidate window, so it plants the window at whatever rect Flutter last
sent, which is always the previous field's origin. Proposed fix
(community): use `selection.baseOffset` when `composingRange.isValid` is
false, so the rect tracks the caret.

**Test approach.** Mock `SystemChannels.textInput`, focus a TextField with
non-empty text, place caret at a non-zero offset, pump frames to trigger
the periodic post-frame callback that calls `_updateComposingRectIfNeeded`,
capture the `TextInput.setComposingRect` call, compare its x-coordinate
against caret-at-end vs caret-at-offset-0.

**Test:** [`issue_92050_sogou_input_dropdown_mispositioned_test.dart`](../regression_tests/ime_cjk/issue_92050_sogou_input_dropdown_mispositioned_test.dart)

**Test outcome.** `test-error`. The `setComposingRect` platform call was
never emitted during the test. Hypothesis: mocking the text-input channel
suppresses the connection state that triggers
`_schedulePeriodicPostFrameCallbacks`, so the code path under test never
runs. A future investigator should try letting `TextInput.setClient` /
`setEditingState` flow through to a stub while still intercepting
`setComposingRect`, or explicitly drive the input connection via a
helper rather than relying on the framework's post-frame callback cycle.
Bug diagnosis stands; test shell retained as a starting point.

**Dedup scan.** Close sibling within IME/CJK: **#79933** (below) — same
Sogou candidate-window-positioning root cause, earlier and more general
form. New cluster **DSK-IME-1** (Desktop IME candidate-window positioning)
formed from this pair.

---

### #142894 — [iOS] Unexpected delta deletion range with a Korean keyboard when the IME replaces a character

- **URL:** https://github.com/flutter/flutter/issues/142894
- **Created:** 2024-02-04 (~2.2 y old) · **Updated:** 2024-08-15
- **Reactions:** 7 (👍 7)
- **Labels:** `a: text input`, `platform-ios`, `framework`, `engine`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 3.16`, `found in release: 3.19`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause (per body + summary).** On a physical iOS device with Korean
keyboard, when the IME replaces a character, the reported
`TextEditingDeltaDeletion.deletedRange` starts one character too early
(start=1 instead of 2 for the example). The framework receives incorrect
deltas from the iOS text input plugin; the delta translation happens in
the iOS embedder when UITextInput replace events are converted into
`TextEditingDelta*` messages. The framework faithfully applies what it's
handed.

**Why engine-level.** Correct delta generation requires the iOS text
input plugin to translate UITextInput's replace behavior (including the
super_editor invisible-prefix edge case in the body) into the right
(oldText, deletedRange, selection, composing) tuple. A framework
`testWidgets` can synthesize any delta sequence it wants, but that
doesn't exercise the translation that's actually broken.

**Dedup scan.** No iOS-Korean-delta-specific duplicate in IME/CJK.
Loosely adjacent to broader IME-delta consistency issues (#128565
`isComposingRangeValid` cross-platform, #174159 web/macOS composing
wrong results, #97775 Android IME delta restarts), which target
different delta-consistency problems on different platforms.

---

### #79933 — [desktop] sogou input window can't track textfield cursor position

- **URL:** https://github.com/flutter/flutter/issues/79933
- **Created:** 2021-04-07 (~5.0 y old) · **Updated:** 2024-06-07
- **Reactions:** 6 (👍 6)
- **Labels:** `a: text input`, `engine`, `a: internationalization`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.0`, `found in release: 2.1`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **likely-duplicate** of #92050

**Root cause.** The IME candidate window (Sogou on Windows, similar IMEs
on macOS) doesn't track the caret, staying at a fixed position
(macOS: lower-left of screen; Windows: below the field). Flutter does not
communicate caret position to the OS IME usefully when there's no active
composing region. This is the same root cause as #92050 — one and the
same plumbing path (`setComposingRect` with offset=0 when composing is
invalid).

**Why duplicate.** #79933 is the older and more general framing (desktop
candidate-window doesn't follow caret, on multiple IMEs). #92050 is a
specific instance with the Sogou after-commit symptom and a
pinpointed fix path (editable_text.dart:5021). Fixing the root cause
addresses both. Recommend merging #92050's fix-path diagnosis into
#79933 as the cluster home for coordination; or designate #92050 as
canonical since it has the concrete fix lead. Either works.

**Cluster.** **DSK-IME-1** (Desktop IME candidate-window positioning) —
new tentative cluster formed with #92050.

**Dedup scan.** Other candidate-window-position bugs in the category
(#113944 Japanese prompt window on Windows, #128323 Chinese candidate
flicker on Windows, #152729 suggestion window offset first-character,
#171319 suggestion window stuck external keyboard) are all desktop-IME
positioning issues but on different IMEs / different triggers. Plausibly
the same plumbing path at root; flagged as potential cluster members but
held as tentative until each is processed.

---

### #121376 — Editable Text after clear has issue with buffer korean input

- **URL:** https://github.com/flutter/flutter/issues/121376
- **Created:** 2023-02-24 (~3.2 y old) · **Updated:** 2025-10-09
- **Reactions:** 6 (👍 6)
- **Labels:** `a: text input`, `engine`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 3.7`, `found in release: 3.8`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **skip — engine-level** (member of cluster **WKI-1**)

**Root cause (per summary).** Windows (and Linux) IME keeps an internal
composition buffer. `TextEditingController.clear()` does not signal the
embedder to reset that buffer, so stale buffer state injects spurious
characters on subsequent input until focus is manually cycled. Workaround
is `focusNode.unfocus()` → `requestFocus()` in a post-frame callback.
Confirmed on Linux as well.

**Why engine-level.** The composition buffer is embedder-internal; the
framework's controller has no API to signal "break composition" explicitly.
Proper fix sits at one of two points: the framework could emit a
composition-reset signal when `clear()` is called (design/behavior change
with ripple effects on formatters etc.), or the embedder could
auto-reset its buffer when its composing region collapses to empty. The
latter is pure embedder work; the former requires text-input team
design review.

**Cluster.** **WKI-1** — confirmed member.

---

### #118547 — [desktop] Chinese characters cannot be input when TextField is surrounded by ToolTip

- **URL:** https://github.com/flutter/flutter/issues/118547
- **Created:** 2023-01-16 (~3.3 y old) · **Updated:** 2024-06-06
- **Reactions:** 5 (👍 5)
- **Labels:** `a: text input`, `engine`, `platform-macos`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 3.7`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Wrapping a TextField in a `Tooltip` breaks
Chinese IME input on desktop (macOS / Windows), specifically when the
mouse hovers autocomplete suggestions. Regression introduced between
3.3.8 and 3.3.9; removing the Tooltip restores behavior.

**Why engine-level.** Very platform-specific (desktop only), IME-specific
(Chinese only), hover-gesture-sensitive. The interaction is between
Tooltip's hover handling (framework-side mouse region / focus behavior)
and the desktop IME composition state (engine-side). The summary notes
this is stalled with no root-cause analysis. Without the specific layer
locked in, a `testWidgets` covering "Tooltip doesn't steal focus" is
trivially green — it wouldn't exercise the IME-state corruption. The
authoritative fix requires engine-side investigation of how IME state
responds to focus/hover events Tooltip introduces.

**Dedup scan.** No tight duplicate within IME/CJK. Weakly related to
broader IME-composition-state-on-focus-change issues; distinct enough
to stand alone.

---

### #130559 — keyboard cursor move to zero when press backspace on TextField with set maxLength (Korean, Windows 10)

- **URL:** https://github.com/flutter/flutter/issues/130559
- **Created:** 2023-07-14 (~2.8 y old) · **Updated:** 2025-10-09
- **Reactions:** 5 (👍 5)
- **Labels:** `a: text input`, `framework`, `engine`, `a: internationalization`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 3.10`, `found in release: 3.13`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **skip — engine-level** (member of cluster **WKI-1**)

**Root cause (per summary).** Windows-specific, Korean-IME-specific:
typing Korean past `maxLength` then pressing Backspace jumps the cursor
to offset 0. Delete, Space, and Backspace-after-move do not reproduce.
Not reproducible on macOS. Web has a related but distinct problem where
Korean exceeds `maxLength` entirely.

**Why engine-level.** The specific 4-way combination (Windows × Korean
IME × `LengthLimitingTextInputFormatter` × Backspace) points at the
Windows embedder's Korean in-place composition handling wiring together
wrongly with framework-enforced length limits. Framework-side formatter
compensation is possible in principle, but the deltas/selection the
embedder forwards are what's misrepresented — any fix that doesn't
correct the embedder's state handling is a compensation hack.

**Cluster.** **WKI-1** — confirmed member.

---

### #149979 — [Web] IME's conversion target background display and caret display position is misaligned

- **URL:** https://github.com/flutter/flutter/issues/149979
- **Created:** 2024-06-09 (~1.9 y old) · **Updated:** 2025-10-09
- **Reactions:** 5 (👍 5)
- **Labels:** `a: text input`, `a: internationalization`, `platform-web`, `has reproducible steps`, `P2`, `team-web`, `triaged-web`, `found in release: 3.22`, `found in release: 3.23`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level** (Flutter web engine)

**Root cause (per summary).** Chrome desktop + non-English (Japanese)
keyboard in Flutter web. During composing, the IME's conversion-target
highlight background and the rendered caret are at misaligned screen
positions. English input is fine. Native iOS build works correctly
(not a framework-shared bug).

**Why engine-level.** Only `platform-web` and `team-web` labels — no
`engine`/`framework` split. Flutter web's DOM text-input integration
(HTML input overlay + visual caret overlay) lives in the web engine.
A `testWidgets` cannot exercise web DOM IME behavior; the fix lives in
Flutter web's IME handling code.

**Dedup scan.** No other web-IME-visual-misalignment issue in IME/CJK.
Other web-IME issues in the category (#126066 web Chinese display wrong
text, #134092 Safari compound characters, #174159 web composing wrong
results, #183078 Korean IME assertion on blur) target different paths.

---

### #102101 — Add integration tests for IME input

- **URL:** https://github.com/flutter/flutter/issues/102101
- **Created:** 2022-04-18 (~4.0 y old) · **Updated:** 2024-07-22
- **Reactions:** 4 (👍 4)
- **Labels:** `a: tests`, `a: text input`, `engine`, `platform-macos`, `platform-windows`, `platform-linux`, `a: desktop`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Scope.** Proposal to add integration-test coverage for IME-based input
(CJK) on desktop. Suggests a custom testing IME with a controllable
interface plus coverage for composing-across-focus-switches, backspace,
Escape, and candidate-menu navigation.

**Why skip.** No regression to capture — this is test infrastructure
work, not a bug. Worth flagging to the team-text-input roadmap: the
lack of IME integration tests is a direct reason so many issues in this
category stay stalled (it's hard to validate fixes without platform-level
tests). Outside this cleanup's scope, but a strong candidate for the
text-input strategy document.

---

### #81314 — TextFormField → TextEditingValue → oldValue.selection and oldValue.composing are wrong with Gboard

- **URL:** https://github.com/flutter/flutter/issues/81314
- **Created:** 2021-04-27 (~5.0 y old) · **Updated:** 2025-12-18
- **Reactions:** 3 (👍 3)
- **Labels:** `a: text input`, `platform-android`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level** (with framework-compensation possible)

**Root cause (per summary).** On Android with `TextInputType.number`
and Gboard, with `autofocus: true` only, Gboard's InputConnection sends
`oldValue.selection` already offset by one before backspace is
processed. `TextInputFormatter.formatEditUpdate` (framework) then
computes a wrong cursor position. Doesn't reproduce with SwiftKey or
without autofocus.

**Why engine-level.** Gboard's InputConnection sequencing is the
non-standard behavior; the Android embedder forwards it as-is. The
authoritative fix is to either normalize oldValue.selection in the
Android embedder's InputConnection adapter (upstream of the framework),
or get Gboard to emit standard sequences. Framework-side compensation
in `formatEditUpdate` is possible but fragile against other IME
variations and would be a workaround, not a fix.

**Dedup scan.** No IME/CJK tight duplicate — Gboard-specific
InputConnection mis-sequencing. Shares a broader "Android embedder
forwards IME quirks unchanged" pattern with #98720/#184744 (stuck
ShiftRight from keyboard software), but different mechanism.

---

### #86471 — [iOS] TextField can't delete or insert character in the middle of pinyin

- **URL:** https://github.com/flutter/flutter/issues/86471
- **Created:** 2021-07-15 (~4.8 y old) · **Updated:** 2024-03-06
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `platform-ios`, `framework`, `f: material design`, `a: internationalization`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 2.4`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** With an active composing underline (pinyin
mid-composition) and the caret moved to the middle of the composing
region, subsequent typing inserts at the end of the composing region
rather than at the caret. Safari / `UITextField` handles this correctly.

**Why engine-level.** iOS IME composition state is owned by UITextInput
and the iOS embedder. Correct mid-composing insertion requires the
embedder to emit the right `TextEditingDelta*` sequence when the caret
moves inside the composing range; today it doesn't. A `testWidgets` can
construct any TextEditingValue at will but can't exercise UITextInput's
mid-composing-insert behavior. Parity with Safari lives in the iOS
embedder's text input plugin.

**Dedup scan.** Related but distinct: #108016 "Can't move caret within
composing region on iOS" (moves caret but not the insert case), #122490
"Moving cursor while composing should stay in composing region"
(cursor-movement angle). A future "iOS composing-region cursor behavior"
cluster could bundle these. Not triggered on three cases; revisit if
more appear.

---

### #91798 — [Linux Desktop - TextField] Can't input text with iBus/fcitx enabled

- **URL:** https://github.com/flutter/flutter/issues/91798
- **Created:** 2021-10-14 (~4.5 y old) · **Updated:** 2024-06-27
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `framework`, `engine`, `a: desktop`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** With iBus or fcitx enabled on Linux
desktop, physical-keyboard input to TextField doesn't reach the field.
Delete works; IME-composed chars appear; space/letters don't. A
`KeyUpEvent` assertion error surfaces in the logs, indicating the Linux
embedder forwards a key event stream that the framework's HardwareKeyboard
state machine can't reconcile. Linked to #87391 (out of this dataset).

**Why engine-level.** The Linux embedder's interaction with GTK's
iBus/fcitx integration is what produces the malformed key event stream.
A `testWidgets` with `sendKeyDownEvent`/`sendKeyUpEvent` can reproduce
the assertion shape trivially (see #98720 precedent), but that's testing
the framework's response to any unpaired event, not the specific iBus
trigger. The fix needs to land in the Linux embedder's GTK key-event
handling (or in iBus itself).

**Dedup scan.** Same *family* as the mobile stuck-shift cluster (#98720
IME/CJK, #184744 Hardware keyboard) — embedder forwards non-standard
key-event stream, framework asserts. Different platform (Linux vs
Android) and different IME software (iBus/fcitx vs Samsung/Gboard), so
not a tight duplicate; shared pattern.

---

### #108016 — Can't move caret within composing region on iOS, though it appears to move

- **URL:** https://github.com/flutter/flutter/issues/108016
- **Created:** 2022-07-20 (~3.8 y old) · **Updated:** 2024-03-26
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `platform-ios`, `framework`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 3.0/3.1/3.9`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** On iOS, after using floating-cursor (long-
press space) to move the caret into the middle of a composing region,
the iOS text input plugin keeps treating the caret as being at the end
of the composing region. Backspace deletes the end char; subsequent
input appends at end. Also a `int → double` cast error during floating-
cursor updates. Affects Chinese pinyin and Japanese kana. "A radar was
filed with Apple since the fix may require a secret UITextInput method
call."

**Why engine-level.** Floating cursor state and composing-region mid-
caret handling live in the iOS text input plugin (UITextInput bridge).
The "secret UITextInput method" note confirms the fix path involves
Apple-private APIs at the embedder. A `testWidgets` can't drive
floating-cursor gesture events through to UITextInput.

**Dedup scan.** Close thematic sibling of #86471 "[iOS] TextField can't
delete or insert in the middle of pinyin" and #122490 "Moving cursor
while composing should stay in composing region". All three describe
iOS composing-region mid-cursor behavior failures. Three distinct
cases — could form an "iOS composing-region cursor" cluster; holding
tentative until #122490 is processed.

---

### #110647 — [iPadOS] External keyboard arrow keys don't control Chinese IME candidate list

- **URL:** https://github.com/flutter/flutter/issues/110647
- **Created:** 2022-08-31 (~3.6 y old) · **Updated:** 2025-08-12
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `e: device-specific`, `platform-ios`, `engine`, `a: internationalization`, `a: fidelity`, `has reproducible steps`, `P2`, `found in release: 3.3/3.4`, `team-ios`, `triaged-ios`
- **Ownership:** `team-ios`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** On iPadOS with an external hardware
keyboard, arrow keys (↑↓←→) don't navigate Chinese IME candidate lists;
only `+`/`-` work. Native iOS apps navigate candidates with arrows.

**Why engine-level.** The iOS text input plugin currently doesn't
forward hardware-arrow events into the IME candidate window. Routing
them requires UITextInput-level work in the embedder (probably
intercepting `pressesBegan` for candidate-window-active states and
forwarding appropriately). Framework has no vantage point.

**Dedup scan.** Distinct symptom — no IME/CJK duplicate. Broader iOS
external-keyboard + CJK IME surface (#110647, #115903 tab cycle through
conversion window, #102647 physical-keyboard Japanese on iPad) is a
potential iPadOS hardware-keyboard IME cluster; holding tentative until
more are processed.

---

### #123065 — CJK word boundaries

- **URL:** https://github.com/flutter/flutter/issues/123065
- **Created:** 2023-03-20 (~3.1 y old) · **Updated:** 2024-10-10
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 3.7/3.9`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **likely-duplicate of #19584** — same ICU-CJK-dictionary root cause

**Root cause.** `ctrl/option + arrow` word navigation on CJK text moves
one character at a time on desktop, not one word. Summary: "Flutter web
already handles CJK word breaking correctly (uses the engine's
`word_breaker.dart` which implements full Unicode TR29 rules); macOS/
Windows/Linux move only one character at a time." Same underlying
capability gap as #19584 — the engine's bundled ICU data lacks the CJK
word-segmentation dictionary, so `TextPainter.getWordBoundary` (used by
both long-press word selection and modifier-arrow word navigation)
returns single-character ranges.

**Why duplicate.** Same root cause, same fix. The #19584 regression
test [`issue_19584_no_word_breaks_for_cjk_locales_test.dart`](../regression_tests/ime_cjk/issue_19584_no_word_breaks_for_cjk_locales_test.dart)
fails today with `Actual: <1>` — exactly the symptom #123065 describes
for cursor navigation. Fixing one fixes both.

**Cluster.** New tentative cluster **CWB-1** (CJK word breaks). Canonical
= #19584 (older, more reactions, already has a passing regression test
authored).

**Dedup scan.** No other word-break-specific duplicates in IME/CJK
discovered so far. The broader CJK-tokenization surface is narrow; most
CJK issues are about IME composing/selection, not word segmentation.

---

### #126066 — [Web] TextField displays wrong text when entering Chinese

- **URL:** https://github.com/flutter/flutter/issues/126066
- **Created:** 2023-05-04 (~3.0 y old) · **Updated:** 2024-03-06
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `platform-web`, `has reproducible steps`, `P2`, `found in release: 3.7/3.11`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level** (web engine)

**Root cause (per summary).** macOS Chrome/Edge + system Chinese input +
HTML renderer: composing region is committed mid-input, breaking the
typing flow. Not reproducible on iPhone native. Root cause "shared with
#120557 (composing region incorrectly committed mid-input)"; triagers
already marked #120557 as a duplicate of this one, keeping #126066 as
canonical.

**Why engine-level.** Web Flutter's HTML/DOM text-input integration
handles composingstate in the web engine. `canvaskit` renderer has a
separate edge case with `InputFormatter`. No framework vantage.

**Dedup scan.** #120557 already merged into this by triage. No other
web-Chinese-premature-commit duplicates in IME/CJK. The web IME family
surface (#126066 here, #149979 caret misalignment, #151097 highlight
misalignment, #174159 composing wrong results web, #183078 Korean IME
assertion on blur, #134092 Safari compound chars) is broad enough that
a dedicated "Web IME" cluster could form, but the individual root
causes differ. Holding tentative.

---

### #145122 — Add support to macOS text replacements

- **URL:** https://github.com/flutter/flutter/issues/145122
- **Created:** 2024-03-14 (~2.1 y old) · **Updated:** 2024-03-14
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `c: new feature`, `platform-macos`, `c: proposal`, `a: desktop`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Scope.** Proposal to implement macOS system-wide text replacements in
`TextField` — a user-configured mapping that triggers a popover
suggestion after typing the configured trigger string.

**Why skip.** Clearly `c: proposal` / `c: new feature`. No regression.
Requires macOS embedder work to surface system text-replacement events,
plus framework UI for the popover. Outside this cleanup's scope.

---

### #149379 — macOS Japanese: characters duplicated on confirm

- **URL:** https://github.com/flutter/flutter/issues/149379
- **Created:** 2024-05-31 (~1.9 y old) · **Updated:** 2025-12-29
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `platform-macos`, `a: internationalization`, `a: desktop`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.22/3.23`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level** (possibly-stale signal noted; needs verification)

**Root cause (per summary).** macOS-only: with Live Conversion disabled
and Google Japanese IME (or system IME on longer sentences), pressing
Enter to confirm duplicates part of the text. Root cause per summary:
"the engine incorrectly committing the composing region in
`FlutterTextInputPlugin.mm`". The explicit `.mm` file reference confirms
engine-level scope (macOS text input plugin).

**Possibly-stale signal.** The summary notes the issue is "related to
#142493 and possibly resolved by #166291 via #160935. [...] possibly
fixed by a related PR, needs verification." A later commenter suggested
`DeltaTextInputClient` as a workaround. Recommend: real-device
verification on latest stable before any close action; if confirmed
fixed, close with a pointer to the resolving PR.

**Why engine-level.** Pinpointed to `FlutterTextInputPlugin.mm`. No
framework vantage point.

**Cluster.** New tentative cluster **MJIME-1** (macOS Japanese IME
composing state). Co-member: #153065 (delta state inconsistency on
macOS Japanese suggestion panel). Shared surface: `FlutterTextInputPlugin.mm`
composing-region handling for macOS Japanese IME.

---

### #151097 — [flutter web] Composing-mode character highlight is incorrect

- **URL:** https://github.com/flutter/flutter/issues/151097
- **Created:** 2024-07-01 (~1.8 y old) · **Updated:** 2025-10-09
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `a: internationalization`, `platform-web`, `has reproducible steps`, `P2`, `team-web`, `triaged-web`, `found in release: 3.22/3.23`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level** (web engine)

**Root cause (per summary).** Composing-underline highlight misalignment
on Flutter web across Android Chrome, iOS Safari, desktop macOS Chrome.
Does not reproduce on native Android/macOS apps. Also happens with
fixed `maxLines`, causing the suggestion list to render at the wrong
position.

**Why engine-level.** Cousin of #9343 (iOS composing style) but
manifesting on Flutter web — web-specific visual integration between the
DOM input overlay and Flutter's rendered text. No framework vantage.

**Dedup scan.** Thematic cousin of #9343 ("iOS composing style") under
an "IME composing visual fidelity" umbrella; different platforms,
different implementations. Holding as cousin not duplicate.

---

### #153065 — [macOS] Japanese IME suggestion panel produces incorrect results

- **URL:** https://github.com/flutter/flutter/issues/153065
- **Created:** 2024-08-08 (~1.7 y old) · **Updated:** 2024-12-28
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `platform-macos`, `a: internationalization`, `a: desktop`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.24`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level** (MJIME-1 cluster member)

**Root cause (per summary).** macOS + Japanese (Kana) IME: typing then
using the down-arrow to navigate the suggestion panel produces a delta
whose `oldText` doesn't match the resulting text from the previous
delta. The macOS engine text input plugin emits inconsistent delta
state between consecutive messages. The error is loggable via
`DeltaTextInputClient`: `"old text from delta doesn't match resulting
text from previous delta"`.

**Why engine-level.** Delta generation lives in the macOS text input
plugin (`FlutterTextInputPlugin.mm`). A `testWidgets` can synthesize
any delta sequence, but that doesn't validate the plugin's generator.

**Cluster.** **MJIME-1** (macOS Japanese IME composing state) —
confirmed co-member alongside #149379. Shared surface:
`FlutterTextInputPlugin.mm`.

---

### #68547 — Active subrange within composing range should be visually highlighted

- **URL:** https://github.com/flutter/flutter/issues/68547
- **Created:** 2020-10-20 (~5.5 y old) · **Updated:** 2024-11-07
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `engine`, `a: internationalization`, `a: desktop`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level** (text-input protocol + framework rendering)

**Root cause / scope (per summary).** Multi-step input (Japanese
ateji, longer names) has two ranges — the overall composing range
*and* an active subrange within it. Flutter currently doesn't
represent the active subrange at all: no text-input protocol field to
carry it, no framework highlighting. Native apps show the active
subrange (e.g., aqua-green highlight on Android). Engine PR #49314
partially fixed macOS; issue reopened after partial fix.

**Why engine-level.** The engine-to-framework text input protocol
doesn't carry an "active subrange" field. Adding it requires protocol
design + engine-side plumbing for each platform + framework-side
rendering. The blocking layer is the protocol extension, which is
engine-scope. Once the protocol carries the field, framework rendering
is straightforward and testable.

**Why not skip-proposal.** This is nominally a missing-feature request,
but it's a P2 fidelity gap (a real bug users see as "text input is
broken") — engine work is already partially done. Classification as
skip-engine matches the blocking layer more honestly than skip-proposal.

**Dedup scan.** No tight duplicates in IME/CJK. Adjacent fidelity
cousin of #9343 (composing style) but different mechanism (active
subrange is a distinct protocol concept, not just styling).

---

### #68843 — Flutter Linux Desktop Japanese input switch

- **URL:** https://github.com/flutter/flutter/issues/68843
- **Created:** 2020-10-23 (~5.5 y old) · **Updated:** 2024-06-07
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `platform-linux`, `a: desktop`, `P2`, `team-linux`, `triaged-linux`
- **Ownership:** `team-linux`
- **Decision:** **skip — engine-level**

**Root cause.** On Fedora/Wayland with `ibus-kkc`, switching between
Japanese input methods doesn't take effect until the Flutter app's state
changes (e.g., a counter increment). Works when forcing GDK backend to
`x11` via `gdk_set_allowed_backends("x11")` in the embedder's `main.cc`.
Wayland-specific GDK backend issue in the Linux embedder.

**Why engine-level.** Linux embedder's GDK backend selection and its
interaction with ibus under Wayland is pure embedder C code. Framework
has no vantage.

**Dedup scan.** Loose thematic neighbor of #91798 (iBus/fcitx on Linux
can't input text). Both Linux + ibus surface, different sub-symptoms;
not tight duplicates.

---

### #91861 — [macOS] IME backspace fails to ignore decorational spaces

- **URL:** https://github.com/flutter/flutter/issues/91861
- **Created:** 2021-10-14 (~4.5 y old) · **Updated:** 2025-10-09
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `platform-macos`, `a: desktop`, `P2`, `team-macos`, `triaged-macos`
- **Ownership:** `team-macos`
- **Decision:** **skip — engine-level** (MCIME-1 cluster member)

**Root cause (per body).** macOS Chinese Pinyin IME inserts decorational
spaces in the precompose text; backspace in Flutter doesn't ignore them,
so each backspace takes 2 presses (5 backspaces to clear `w w w` instead
of 3). Native macOS handles it correctly.

**Why engine-level.** Composing-region backspace handling for IME on
macOS lives in `FlutterTextInputPlugin.mm` — same surface as
#149379/#153065. Framework receives whatever the plugin emits.

**Cluster.** **MCIME-1** (renamed from MJIME-1 to cover macOS CJK IME
more broadly) — confirmed member.

---

### #97775 — IME deltas on Android trigger input method restarts when they shouldn't

- **URL:** https://github.com/flutter/flutter/issues/97775
- **Created:** 2022-02-04 (~4.2 y old) · **Updated:** 2023-10-24
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `platform-android`, `P2`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause (per body + summary).** Android embedder restarts the IME
whenever the composing region changes — a prior fix to a different
bug — but when the framework wants to delete into the composing region
(via DeltaTextInputClient + held backspace), each restart aborts the
delete. The body links directly to the offending code in the Android
embedder's Java source.

**Why engine-level.** Fix requires the Android embedder to distinguish
composing-changes-that-need-restart from composing-changes-that-don't,
which depends on metadata the framework currently doesn't send. Also
requires a protocol extension for the framework to signal "this
composing change came from a key event, don't restart". Framework-only
fix isn't possible without engine work.

**Dedup scan.** Thematically related to Android IME delta / batch-edit
handling (#120351 Samsung batch-edit + key event ordering, also
processed this batch). Different mechanism; held as separate.

---

### #102142 — Keyboard must be dismissed twice (Android / SwiftKey)

- **URL:** https://github.com/flutter/flutter/issues/102142
- **Created:** 2022-04-19 (~4.0 y old) · **Updated:** 2024-03-06
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `platform-android`, `framework`, `has reproducible steps`, `P2`, `found in release: 2.10/2.13`, `team-android`, `triaged-android`
- **Ownership:** `team-android`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** On Android with Microsoft SwiftKey,
when the cursor teardrop (selection handle) is visible, dismissing the
keyboard requires two back-button presses instead of one. Specific to
SwiftKey's InputConnection / back-key behavior.

**Why engine-level.** SwiftKey's InputConnection state handling diverges
from standard Android IMEs, and the Android embedder forwards its events
as-is. The framework-side handle-visible state subscribes to keyboard
open/close signals; fixing requires either the embedder to normalize
SwiftKey's dismiss semantics or to expose more state to the framework.

**Dedup scan.** Related "Android embedder forwards non-standard IME
behavior" pattern (#98720/#184744 Samsung/Gboard shift-stuck, #120351
Samsung batch-edit, #81314 Gboard off-by-one selection). Each is a
different IME and a different non-standard behavior; not tight duplicates.

---

### #102239 — Flashing composing underline while typing on Android with physical keyboard

- **URL:** https://github.com/flutter/flutter/issues/102239
- **Created:** 2022-04-20 (~4.0 y old) · **Updated:** 2024-03-06
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `platform-android`, `framework`, `f: material design`, `a: fidelity`, `a: quality`, `has reproducible steps`, `P2`, `found in release: 2.10/2.13`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** On Android with a physical/hardware
keyboard, the composing underline flashes off/on at each keypress
instead of smoothly expanding (as native Android does). Soft keyboard is
fine. No root-cause analysis in comments; looks like a repaint-timing
mismatch between the embedder's per-key composing-region updates and the
framework's paint cycle.

**Why engine-level.** "Only with physical keyboard" is the diagnostic
signal: the hardware-key → composing-region update path on Android
differs from the IME path, and the timing of those updates is set by
the embedder. Fixing is in the Android embedder. A `testWidgets` has no
meaningful simulation of per-keypress composing-region blink timing
against a real IME surface.

---

### #105028 — TextField toolbar button text doesn't match native iOS/macOS in Japanese

- **URL:** https://github.com/flutter/flutter/issues/105028
- **Created:** 2022-05-31 (~3.9 y old) · **Updated:** 2024-03-06
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `platform-ios`, `framework`, `platform-macos`, `a: internationalization`, `a: fidelity`, `has reproducible steps`, `P2`, `found in release: 3.0/3.1`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip-test — needs native-platform verification**

**Root cause (per summary).** Flutter's Cupertino/Material Japanese
localizations go through Translation Console, producing strings like
"翻訳 切り取り コピー 取り付け" where native iOS expects
"翻訳 カット コピー ペースト". A fidelity gap — the strings are
semantically correct but not the platform-idiomatic localizations.

**Why not write-test.** Technically framework-testable — the Cupertino
localizations `CupertinoLocalizations.pasteButtonLabel` (etc.) for `ja`
can be asserted against any string. But pinning them to specific values
requires a confirmed *current* reference from native iOS / macOS; Apple
ships strings that can change across OS versions (cf. #9343 style
drift). Deferred pending a native-baseline check on current
iOS 17/18 / macOS Sonoma/Sequoia.

**Dedup scan.** Second "needs-native-platform-verification" entry in
the category (first: #9343 iOS composing style). Both are
`a: fidelity`-labeled. Nascent pattern: `a: fidelity` frequently maps
to needs-native-verification.

---

### #117642 — Problems with TextInputAction.send + TextInputType.multiline (Sogou)

- **URL:** https://github.com/flutter/flutter/issues/117642
- **Created:** 2022-12-26 (~3.3 y old) · **Updated:** 2024-03-06
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `platform-ios`, `engine`, `a: internationalization`, `dependency: skia`, `has reproducible steps`, `P2`, `found in release: 3.3/3.7`, `team-ios`, `triaged-ios`
- **Ownership:** `team-ios`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** iOS + `TextInputType.multiline` +
`TextInputAction.send` + Sogou (and similar Chinese third-party)
keyboards: the line-feed key inserts a space instead of a newline.
Flutter's engine detects newlines by looking for `\n`; Sogou emits
`\r\r` (two carriage returns); SkParagraph treats `\r` as a soft line
break. Proposed workaround: `FilteringTextInputFormatter` replacing
`\r` with `\n`.

**Why engine-level.** The newline-detection logic is in the engine's
iOS text input + SkParagraph path. A `FilteringTextInputFormatter` at
the framework level is a workaround, not a fix — the underlying SkParagraph
behavior is still wrong.

---

### #117771 — TextInputConnection should let objects listen for IME connection closure

- **URL:** https://github.com/flutter/flutter/issues/117771
- **Created:** 2022-12-29 (~3.3 y old) · **Updated:** 2024-09-01
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `c: proposal`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Scope.** Proposal to add an attachment-change listener to
`TextInputConnection`, so consumers that use the connection independently
from the `TextInputClient` can react to closure. PR #118283 was proposed
for this.

**Why skip.** `c: proposal` / `c: new feature`. API-design request.

---

### #120351 — Samsung keyboard: Japanese-to-symbols conversion produces bad state

- **URL:** https://github.com/flutter/flutter/issues/120351
- **Created:** 2023-02-09 (~3.2 y old) · **Updated:** 2024-02-20
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `e: device-specific`, `platform-android`, `a: internationalization`, `has reproducible steps`, `P2`, `e: samsung`, `found in release: 3.7/3.8`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Samsung keyboard emits a batch edit with
two operations: (1) `commitText` replacing the composing region, (2) a
`KEYCODE_DPAD_LEFT` key event to position the cursor inside the
resulting brackets. The Android embedder doesn't treat the key event
as part of the batch edit, so the left-arrow reaches the framework
before the text replacement, corrupting state. Investigated by
@Renzo-Olivares then handed to @LongCatIsLooong for a non-trivial
refactor.

**Why engine-level.** The Android embedder's batch-edit handling needs
to preserve the (commitText, key-event) ordering within a batch.
Framework receives the out-of-order stream; compensation would be a
workaround.

**Dedup scan.** Earlier (in #98720 processing) I flagged #120351 as a
tentative weak-related candidate to Samsung shift-stuck cluster. On
processing: distinct mechanism (batch-edit ordering vs phantom key
event), both Samsung-Android but different underlying bugs. Not a
duplicate. Leaving as: "Android embedder forwards non-standard Samsung
behavior" thematic pattern, not a tight cluster.

---

### #122490 — Moving cursor while composing should stay in composing region

- **URL:** https://github.com/flutter/flutter/issues/122490
- **Created:** 2023-03-12 (~3.1 y old) · **Updated:** 2024-03-06
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `platform-android`, `platform-ios`, `framework`, `a: internationalization`, `a: fidelity`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level** (CRC-1 cluster canonical)

**Root cause (per summary).** In a composing region, the caret should
clamp within the composing region — native iOS does (with one edge
case); Android/Gboard shows the cursor wrong visually but internally
keeps it within the composing region. Flutter doesn't match either.

**Why engine-level.** On iOS, the clamp is enforced by UITextInput at
the embedder level (see #108016). On Android, the embedder receives
and forwards gestures that produce the wrong visual state. Both paths
need embedder-side handling; framework-level cursor clamping would need
to know the "visible" vs "internal" cursor positions which are
platform-specific.

**Cluster.** New tentative cluster **CRC-1** (Composing-region cursor
clamping). Members: #86471 iOS pinyin mid-composing insert, #108016 iOS
floating-cursor-in-composing-region, #122490 (this one, canonical —
most general framing covering both iOS and Android).

---

### #128315 — [iOS] Suggestion text is auto-filled in Japanese keyboard

- **URL:** https://github.com/flutter/flutter/issues/128315
- **Created:** 2023-06-06 (~2.9 y old) · **Updated:** 2024-03-06
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `platform-ios`, `engine`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 3.10/3.11`, `team-ios`, `triaged-ios`
- **Ownership:** `team-ios`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** When text is programmatically replaced via
`TextEditingController.text` + `.selection` while a composing region is
active, the iOS Japanese IME continues to show the suggestion overlay and
auto-inserts it on the next keypress. Team suggested setting the full
`TextEditingValue` (including composing region) in one step as a
workaround. Linked to #126263 (Windows) and #125765 (iOS web) — same
family of "programmatic text replacement leaves IME state stale".

**Why engine-level.** The IME suggestion state is owned by the iOS text
input plugin; a programmatic text replacement that doesn't explicitly
reset `markedText:selectedRange:` in UITextInput leaves the suggestion
state alive. Framework-side workaround (set the full value) papers over
this; the authoritative fix is in the iOS plugin to reset the marked
range whenever the framework replaces text.

---

### #128323 — When TextField enters Chinese in Windows 10, the candidate list will flicker

- **URL:** https://github.com/flutter/flutter/issues/128323
- **Created:** 2023-06-06 (~2.9 y old) · **Updated:** 2024-07-29
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `engine`, `a: internationalization`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 3.10/3.11`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **likely-duplicate of #92050** (DSK-IME-1 cluster member)

**Root cause (per summary).** Chinese IME on Windows 10: candidate list
flickers because it briefly appears at 0,0 for one frame before jumping
to the correct position. Proposed fix: throttle repositioning to
commit / new-line events rather than every keystroke.

**Why duplicate.** The "appears at 0,0 for one frame" is the same
`setComposingRect(offset=0)` bug #92050 pinpointed in
`editable_text.dart:5021` — when composingRange is invalid (or briefly
becomes invalid between keystrokes), the rect defaults to the field's
top-left. Sogou / Windows IME candidate window follows, producing the
flash. One fix (use caret position when composingRange invalid)
addresses both the persistent-wrong-position #92050 symptom and the
per-keystroke flicker here. Proposed throttling in this thread is a
different (and arguably less correct) remediation.

**Cluster.** **DSK-IME-1** (Desktop IME candidate-window positioning) —
confirmed member.

---

### #132551 — [iOS][iOS 17] IME shows at the wrong place with hardware keyboard

- **URL:** https://github.com/flutter/flutter/issues/132551
- **Created:** 2023-08-15 (~2.7 y old) · **Updated:** 2023-08-21
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `platform-ios`, `engine`, `a: internationalization`, `e: OS-version specific`, `has reproducible steps`, `P2`, `found in release: 3.10/3.14`, `team-ios`, `triaged-ios`
- **Ownership:** `team-ios`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** iPhone + iOS 17 + hardware keyboard +
IME (Chinese): candidate window shows in the wrong place. Engine PR
#44779 (autocorrection fix) partially improved position but didn't
fully resolve. Does not affect iPhone on older iOS or Mac.

**Why engine-level.** IME candidate window placement is owned by the
iOS text input plugin and the coordinates it sends to UITextInput. An
iOS 17 change in how UITextInput handles hardware-keyboard IME updates
shifted the behavior. Fix is in the iOS plugin.

**Dedup scan.** Similar conceptual family as DSK-IME-1 (wrong IME
candidate position) but different platform (iOS, not desktop) and
different root cause (iOS 17 OS-version behavior change, not
setComposingRect). Not a cluster member.

---

### #132638 — TextField doesn't work properly with iOS device's text replacement function

- **URL:** https://github.com/flutter/flutter/issues/132638
- **Created:** 2023-08-16 (~2.7 y old) · **Updated:** 2023-08-18
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `platform-ios`, `framework`, `f: material design`, `a: fidelity`, `a: typography`, `has reproducible steps`, `P3`, `team-design`, `triaged-design`, `found in release: 3.13/3.14`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** iOS system-wide text-replacement shortcut
(Settings → Keyboard → Text Replacement) is intermittent in Flutter
TextField: works on initial install, stops working after some usage.
Reverting to 3.7.10 restores behavior. The team could not find a
consistent repro trigger. Only iOS; Android uses a different flow.

**Why engine-level.** Text-replacement is a UITextInput mechanism.
The regression between 3.7.10 and 3.10 indicates an engine-side
change altered how Flutter interacts with UITextInput's
text-replacement; fix needs iOS plugin investigation. Framework has
no vantage.

---

### #134330 — [Desktop app] Cannot restrict candidate list on password field

- **URL:** https://github.com/flutter/flutter/issues/134330
- **Created:** 2023-09-09 (~2.6 y old) · **Updated:** 2024-06-14
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `engine`, `a: internationalization`, `a: desktop`, `has reproducible steps`, `P3`, `found in release: 3.13/3.14`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** On desktop (macOS/Windows), setting
`obscureText: true` + `keyboardType: TextInputType.visiblePassword`
does not force the OS IME to English mode on password fields, so
Chinese IME candidate list still appears. Native Qt / Objective-C
apps auto-switch. Web and mobile behave correctly.

**Why engine-level.** The macOS/Windows embedder needs to tell the OS
IME "this is a password field, suppress composing" — a one-call
handshake on the macOS TSM API / Windows IMM32. Framework already
passes `TextInputType.visiblePassword`; embedder doesn't translate that
into OS IME suppression on desktop.

---

### #135406 — Word Candidate Window has problem when typing Chinese with hardware keyboard (iOS)

- **URL:** https://github.com/flutter/flutter/issues/135406
- **Created:** 2023-09-25 (~2.6 y old) · **Updated:** 2024-07-05
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `platform-ios`, `a: internationalization`, `has reproducible steps`, `P2`, `team-ios`, `triaged-ios`, `found in release: 3.13/3.15`
- **Ownership:** `team-ios`
- **Decision:** **likely-duplicate of #110647**

**Root cause (per summary).** iOS + Chinese IME + hardware keyboard:
arrow and tab keys are consumed by Flutter's key handling and don't
reach the IME candidate window, so the user can't navigate candidates
with the keyboard. Affects Magic Keyboard / Bluetooth keyboards.

**Why duplicate.** Same root cause as #110647 (processed batch 4):
iOS text input plugin doesn't forward hardware-arrow/tab key events
into the IME candidate window's selection logic. #110647 is the older
filing with slightly richer discussion; this one narrows to hardware
keyboards specifically. Both fixes live in the iOS plugin.

**Cluster.** New tentative cluster **IHK-1** (iOS hardware-keyboard
IME candidate navigation). Canonical = **#110647** (older, slightly
richer). Members: #110647, #135406.

---

### #142882 — Under certain conditions TextInput does not correctly handle backspaces on Android

- **URL:** https://github.com/flutter/flutter/issues/142882
- **Created:** 2024-02-04 (~2.2 y old) · **Updated:** 2024-03-14
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `platform-android`, `has reproducible steps`, `P3`, `team-android`, `triaged-android`, `found in release: 3.16/3.20`
- **Ownership:** `team-android`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** On Android with `enableSuggestions: false`,
the underlying `InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD` flag
causes the IME to route backspace via a hardware-key path
(`DeleteCharacterIntent`) rather than the `MethodChannel` text-update
path. A custom `TextInputClient` never receives a `updateEditingValue`
for the deletion. Workaround: intercept `DeleteCharacterIntent` via
`FocusableActionDetector`. Separate but related bug #143364 on
number-entry.

**Why engine-level.** The Android embedder's mapping between InputType
flags and its two delete paths is the root cause. Framework-side
workaround (intercept the Intent) is viable for app developers but
isn't a fix.

---

### #146486 — Composing characters (e.g. Umlauts) using physical keyboard on iOS generates two characters

- **URL:** https://github.com/flutter/flutter/issues/146486
- **Created:** 2024-04-09 (~2.0 y old) · **Updated:** 2026-03-31
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `platform-ios`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 3.19/3.22`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **likely-duplicate of #59541** (DK-1 cluster confirmed member)

**Root cause (per summary).** iOS physical keyboard + dead-key composing
(ALT-u + u for ü, ALT-u + a for ä, etc.) produces two characters
instead of one. Root cause pinpointed:
`[FlutterTextInputView insertText:]` does not replace the composing
range set by `setMarkedText:selectedRange:`, leaving the dead-key
character alongside the composed character.

**Why duplicate.** Same symptom family as #59541 (batch 1's skip-engine
with DK-1 cluster formed): mobile embedder does not combine dead-key +
base-letter events into one composed character, so two characters
surface. Here the pinpoint is the iOS-specific path
(`FlutterTextInputView.insertText`); #59541 discussed the Android
`CharacterCombiner` fix that was ported from Windows. Both are the
same family: mobile embedder key-event combining is missing.
@LongCatIsLooong is working on a broader iOS text-input prototype that
will likely cover this.

**Cluster.** **DK-1** (Dead-key composition on mobile) — confirmed
member (previously tentative). Adds the explicit iOS `insertText` /
`setMarkedText` pinpoint as a fix target.

---

### #151103 — [flutter web] ATOK Japanese hiragana→kanji display distorted

- **URL:** https://github.com/flutter/flutter/issues/151103
- **Created:** 2024-07-01 (~1.8 y old) · **Updated:** 2025-10-09
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `a: internationalization`, `a: fidelity`, `platform-web`, `P2`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level** (Flutter web engine)

**Root cause (per summary).** Flutter web + Chrome Android + ATOK
Japanese IME: hiragana→kanji conversion shows doubled characters. Not
reproducible on Android native with ATOK, nor on web with Gboard.
Commenter noted doubled character also appears in a different font,
suggesting a font-fallback interaction.

**Why engine-level.** Web-specific visual rendering issue during IME
conversion. No framework vantage; fix lives in the web engine's IME
handling or text layout.

**Dedup scan.** Joins a growing set of web-IME visual issues (#126066
web Chinese wrong text, #149979 web caret misalignment, #151097 web
composing highlight misalignment) — related but distinct root causes
within Flutter web's IME integration. Not tight duplicates; a future
"Web IME visual fidelity" cluster could form but the individual root
causes still diverge too much today.

---

### #166400 — [Windows] Issue with converting Korean to Hanja on Windows 10

- **URL:** https://github.com/flutter/flutter/issues/166400
- **Created:** 2025-04-02 (~1.1 y old) · **Updated:** 2025-09-18
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `a: internationalization`, `platform-windows`, `a: desktop`, `e: OS-version specific`, `P3`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **skip — engine-level** (WKI-1 cluster confirmed member)

**Root cause (per body + summary).** On Windows 10 (not Windows 11),
pressing the Hanja key while composing Korean should show a list of
Hanja (Chinese-character equivalents) to pick from. On Flutter the
list doesn't appear / selection doesn't work. Reporter notes a previous
issue #74819 was claimed fixed based on Windows-11-only testing;
Windows 10 still broken. Team has only Windows 11 available for
verification.

**Why engine-level.** Windows 10 vs 11 IME behavior diverges in how
Hanja key press is delivered; the Windows embedder's IME handling
doesn't surface the Hanja request consistently on Windows 10. Fix in
the Windows embedder. Framework has no Windows-version-specific
vantage.

**Cluster.** **WKI-1** (Windows Korean IME family) — confirmed member.

---

### #176055 — [Android 17] Improve CJKV physical keyboard accessibility

- **URL:** https://github.com/flutter/flutter/issues/176055
- **Created:** 2025-09-25 (~0.6 y old) · **Updated:** 2026-04-07
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `platform-android`, `a: accessibility`, `P2`, `team-android`, `triaged-android`
- **Ownership:** `team-android`
- **Decision:** **skip — engine-level**

**Root cause / scope.** Android 17 added new `AccessibilityEvent`
text-change types (`TEXT_CHANGE_TYPE_IN_COMPOSITION`,
`TEXT_CHANGE_TYPE_COMMITTED_BY_IME`,
`TEXT_CHANGE_TYPE_CONVERSION_SUGGESTION_SELECTED_BY_IME`) for CJKV
input. Flutter's `AccessibilityBridge.createTextChangedEvent` (pinpointed
by the body at `engine/src/flutter/shell/platform/android/io/flutter/view/AccessibilityBridge.java#L2091`)
needs to call `setTextChangeTypes` with the right value.

**Why engine-level.** Explicitly named engine file;
`AccessibilityBridge.java` is Android-embedder Java. Framework has no
vantage. Fix is pure embedder work to adopt the new Android 17 APIs.

---

### #24955 — Ability to Integration Test Marked Text

- **URL:** https://github.com/flutter/flutter/issues/24955
- **Created:** 2018-12-04 (~7.4 y old) · **Updated:** 2025-06-30
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `tool`, `t: flutter driver`, `P3`, `team-tool`, `triaged-tool`, `tool-still-valid`
- **Ownership:** `team-tool`
- **Decision:** **skip — feature/proposal**

**Scope.** Request to enable programmatic typing of marked text in
integration/driver tests, so iOS-specific composing-region behaviors
(e.g., the engine crash that motivated flutter/engine#6989) can be
covered by automated tests. Currently driver tests can't set a marked
region.

**Why skip.** `c: new feature`; test-infrastructure work, not a bug.
Thematically adjacent to #102101 "Add integration tests for IME input"
(processed batch 2) — both are tooling gaps that would make IME/CJK
dramatically more attackable if closed. Out of scope for this cleanup.

---

### #55343 — [IME] Android InputMethodService onViewClicked not invoked on TextField tap

- **URL:** https://github.com/flutter/flutter/issues/55343
- **Created:** 2020-04-22 (~6.0 y old) · **Updated:** 2024-03-06
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-android`, `framework`, `c: proposal`, `P3`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal**

**Scope.** Third-party Android IME developer request: add a
`TextInput.onclicked` method to `TextInputChannel` so IMEs can observe
when the user taps the input area, mirroring native
`InputMethodService.onViewClicked`. Not currently exposed because the
TextField's onTap runs in a different process than the IME.

**Why skip.** `c: proposal` — new API surface. Engine-side change to
expose platform-channel event + IME adoption. Out of cleanup scope.

---

### #68549 — Linux: Emoji insertion via Ctrl-Shift-E incorrectly positions completions

- **URL:** https://github.com/flutter/flutter/issues/68549
- **Created:** 2020-10-20 (~5.5 y old) · **Updated:** 2024-06-07
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-linux`, `a: desktop`, `P2`, `team-linux`, `triaged-linux`
- **Ownership:** `team-linux`
- **Decision:** **skip — engine-level**

**Root cause (per body).** On Linux with multi-step input (Ctrl-Shift-U
codepoint, Ctrl-Shift-E emoji), the completion window is positioned
incorrectly when not in composing mode. Body pinpoints the fix path:
notify the GTK embedder of every cursor-position change (even when not
composing), and remove specific lines in
`shell/platform/linux/fl_text_input_plugin.cc#L324-L327`.

**Why engine-level.** Explicitly named engine file; Linux GTK embedder
C code. Framework has no vantage.

**Dedup scan.** Positioning bug thematic cousin of DSK-IME-1 (desktop
IME candidate-window positioning) but Linux-specific and with a distinct
pinpoint (`fl_text_input_plugin.cc` vs `editable_text.dart`). Not a
cluster member.

---

### #77461 — Keyboard shortcuts not working with fcitx

- **URL:** https://github.com/flutter/flutter/issues/77461
- **Created:** 2021-03-06 (~5.1 y old) · **Updated:** 2024-03-06
- **Reactions:** 0
- **Labels:** `a: text input`, `engine`, `a: accessibility`, `platform-web`, `platform-linux`, `has reproducible steps`, `P2`, `found in release: 2.0/2.1`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** On Linux web, after typing through fcitx
and committing Chinese text, subsequent `Alt+K` (and similar shortcut)
presses no longer trigger the Flutter shortcut handler. Linked to
#77048 as potentially related. Engine-labeled.

**Why engine-level.** Web engine's key-event delivery after IME commit
is the affected path — the commit action leaves key events in a state
the engine doesn't dispatch to the framework shortcut system. Framework
has no web-specific IME commit vantage.

**Dedup scan.** Loose neighbor of #91798 "Linux iBus/fcitx can't input
text" (processed batch 4), but different environment (web vs Linux
desktop) and different symptom (shortcuts not dispatched vs text not
reaching field). Not a duplicate.

---

### #80667 — [Web][TextField] ESC during IME suggest closes dialog too

- **URL:** https://github.com/flutter/flutter/issues/80667
- **Created:** 2021-04-18 (~5.0 y old) · **Updated:** 2024-06-27
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-web`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.10/2.13`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level** (web engine)

**Root cause (per summary).** In a TextField inside a Dialog on web:
Japanese IME shows suggest popover; pressing ESC to cancel the IME
suggest also closes the Dialog. macOS desktop was fixed on master (not
stable); web version still broken. The ESC key event propagates through
to the Dialog's cancel handler despite IME composition.

**Why engine-level.** Web engine delivers key events to the Flutter
framework after the browser processes IME composition; on web the
boundary between "IME consumed the ESC" and "Flutter handles it" is
different from native platforms. The macOS fix presumably landed
engine-side; web needs its own fix.

---

### #87257 — TextField accented word writing problem using soft keyboard on iPad

- **URL:** https://github.com/flutter/flutter/issues/87257
- **Created:** 2021-07-29 (~4.7 y old) · **Updated:** 2024-03-06
- **Reactions:** 0
- **Labels:** `a: text input`, `e: device-specific`, `platform-ios`, `framework`, `engine`, `a: tablet`, `P2`, `team-ios`, `triaged-ios`
- **Ownership:** `team-ios`
- **Decision:** **likely-duplicate of #59541** (DK-1 cluster)

**Root cause (per summary).** iPad Pro 12.9" (4th gen) with French /
Spanish soft keyboard: typing dead-key + base letter produces two
characters (e.g. ` `` + à` instead of `à`). Device-specific to iPads
with the dedicated-accent-keys soft-keyboard layout.

**Why duplicate.** Same symptom as #59541 / #146486: dead-key + letter
produces two characters instead of one combined character. The
mechanism is identical to the DK-1 cluster root cause (iOS plugin
doesn't combine dead-key + letter events into one composed character);
this case surfaces on iPad soft keyboards specifically because they
expose a literal dead-key glyph button. Fix family: same
`FlutterTextInputView` / `setMarkedText:` path.

**Cluster.** **DK-1** (Dead-key composition on mobile) — upgraded from
tentative-weak-candidate to confirmed member.

---

### #95410 — IME lifecycle not working well in TextField (Android)

- **URL:** https://github.com/flutter/flutter/issues/95410
- **Created:** 2021-12-16 (~4.4 y old) · **Updated:** 2024-03-06
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-android`, `engine`, `P2`, `team-android`, `triaged-android`
- **Ownership:** `team-android`
- **Decision:** **likely-duplicate of #97775**

**Root cause (per summary).** Android IME's `onStartInput` is called on
every space press. Root cause: Flutter's Android text input plugin
calls `InputMethodManager.restartInput` whenever the framework changes
the composing region — which happens when the built-in single-line
input formatter strips `\n` characters. Native `EditText` doesn't apply
such formatters so doesn't trigger restarts. Specific to
`TextInputType.text`; `emailAddress` and `visiblePassword` don't
reproduce.

**Why duplicate.** Same underlying mechanism as #97775 (processed
batch 4): Android embedder restarts the IME on every composing-region
change, which is triggered here by framework-side input formatters.
#97775 framed it in terms of delta deletion; this one frames it in
terms of IME lifecycle callbacks. One fix (suppress restart when
composing change originates framework-side, not from IME) addresses
both. New cluster **AIR-1** (see clusters section).

---

### #96092 — [TextField] Cannot use Japanese keyboard (ATOK) on Android

- **URL:** https://github.com/flutter/flutter/issues/96092
- **Created:** 2022-01-04 (~4.3 y old) · **Updated:** 2024-11-07
- **Reactions:** 0
- **Labels:** `a: text input`, `e: device-specific`, `platform-android`, `framework`, `a: internationalization`, `P2`, `team-android`, `triaged-android`
- **Ownership:** `team-android`
- **Decision:** **likely-duplicate of #97775** (AIR-1 cluster)

**Root cause (per summary).** Super ATOK ULTIAS Japanese keyboard on
Fujitsu Android devices: second keypress deletes the previous
character; switching keyboards is disabled. Device-specific (regular
ATOK on other devices works fine). **Removing `FilteringTextInputFormatter`
resolves the problem**, identifying the formatter-triggered composing-
region change as the root cause. A commenter links the pattern to
#139143 (non-English keyboard + `enableSuggestions: false`).

**Why duplicate.** Same "FilteringTextInputFormatter → framework mutates
composing region → Android embedder calls `restartInput` → IME loses
state" mechanism as #97775 and #95410. The Fujitsu-ATOK device angle
is incidental; the formatter-driven restart is the shared root cause.

**Cluster.** **AIR-1** — member.

---

### #98573 — iPadOS 15.1 Chinese Pinyin: TextField cursor doesn't update on tap

- **URL:** https://github.com/flutter/flutter/issues/98573
- **Created:** 2022-02-16 (~4.2 y old) · **Updated:** 2026-01-14
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-ios`, `framework`, `f: material design`, `a: tablet`, `e: OS-version specific`, `P2`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** iPadOS 15.1 and 15.3.1 physical devices +
Pinyin Chinese IME: tapping to move the caret doesn't move it. Not
reproducible on simulator with iOS 15.2 or English input. Debug
tracing: gesture detection in `text_selection.dart` receives
`onTapDown` but never `onTapUp`.

**Why engine-level.** The missing `onTapUp` at the framework-gesture
layer indicates the iOS embedder (UIKit pointer translation) isn't
delivering the up-phase of the touch when Pinyin IME is active on
these specific iPadOS versions. Very narrow OS-version × IME × device
combination pointing at a UIKit-level behavior the iOS text input
plugin doesn't handle. Framework's gesture layer receives only what
the embedder forwards.

**Dedup scan.** Superficial resemblance to #98720 (Samsung shift stuck
→ tap extends selection on Android), but different mechanism: that was
a key-event state bug, this is a pointer-event delivery bug. Different
clusters.

---

### #99511 — [Windows] TextField caret position inconsistent with Chinese text (CRLF)

- **URL:** https://github.com/flutter/flutter/issues/99511
- **Created:** 2022-03-03 (~4.1 y old) · **Updated:** 2024-06-07
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.10/2.11`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Chinese text pasted from Windows editors
contains `\r\n` line endings. Flutter treats `\r` inconsistently —
caret moves wrong, click-into-blank-line doesn't register, copy-paste
shows character blocks. Workaround: normalize `\r\n` → `\n`.

**Why engine-level.** `\r` handling bleeds into SkParagraph / Skia text
layout (cf. #117642 where SkParagraph treats `\r` as soft line break
for Sogou line-feed). Correct fix either at Skia text-layout level or
at framework InputFormatter auto-normalization — fix scope still under
discussion, but the buggy path is engine-side.

---

### #101222 — [Web] Composing Candidates incorrect vertical offset after refocus

- **URL:** https://github.com/flutter/flutter/issues/101222
- **Created:** 2022-04-02 (~4.1 y old) · **Updated:** 2024-03-06
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `platform-macos`, `a: internationalization`, `a: fidelity`, `platform-web`, `has reproducible steps`, `P2`, `found in release: 2.10/2.13`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level** (web engine)

**Root cause (per summary).** Flutter web on Chrome: unfocusing a
TextField with Japanese input, then refocusing in the middle of
existing text, causes the IME candidate box to appear at the wrong
vertical offset (far from the caret or overlapping text). No root-cause
analysis; web-only.

**Why engine-level.** Web engine's IME candidate positioning on
refocus — equivalent to DSK-IME-1's `setComposingRect` issue but on the
web engine's DOM/overlay path rather than desktop embedders.

**Dedup scan.** Thematic cousin of DSK-IME-1 (desktop IME candidate
window positioning) but web-specific. Join a future "Web IME" cluster
if more gather.

---

### #102647 — iPad physical keyboard: Japanese suggestion field shifts and covers characters

- **URL:** https://github.com/flutter/flutter/issues/102647
- **Created:** 2022-04-27 (~4.0 y old) · **Updated:** 2024-03-06
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-ios`, `engine`, `a: desktop`, `P2`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — engine-level**

**Root cause (per @cbracken in summary).** Pinpointed: the iOS engine's
`firstRectForRange` returns a zero-height `markedRect`, and the code
only adjusts width (not height) when the caret rect is received in
place of the composing rect — so the IME candidates view positions at
the top of the character. Likely a race in the async composing-rect
update.

**Why engine-level.** Explicit engine pinpoint (`firstRectForRange` in
the iOS plugin). Framework has no vantage.

**Dedup scan.** Cousin of DSK-IME-1 (desktop IME candidate-window
positioning) but iOS-specific with a distinct pinpoint. Shares the
broader theme "IME candidate window positioning via rect updates."

---

### #102988 — Composing region does not extend while typing on Android emulator

- **URL:** https://github.com/flutter/flutter/issues/102988
- **Created:** 2022-05-03 (~4.0 y old) · **Updated:** 2024-03-06
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-android`, `framework`, `P2`, `team-android`, `triaged-android`
- **Ownership:** `team-android`
- **Decision:** **skip — engine-level**

**Root cause (per body).** Typing into the front of an existing word on
Android: the composing region only covers the newly typed text; native
Android extends the composing region to cover the whole word. Both
software and hardware keyboard reproduce.

**Why engine-level.** Composing-region extension is driven by Android
IME + the embedder's InputConnection handling. The framework receives
whatever composing range the embedder sends. No framework vantage.

---

### #103136 — [Android][Samsung] Accents âôê don't work with TextInputType.visiblePassword

- **URL:** https://github.com/flutter/flutter/issues/103136
- **Created:** 2022-05-05 (~4.0 y old) · **Updated:** 2024-03-06
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-android`, `framework`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 2.10`, `e: samsung`, `found in release: 2.13`, `team-android`, `triaged-android`
- **Ownership:** `team-android`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Samsung keyboard (not Gboard): holding a
letter key and selecting an accented variant produces no input (and no
onChanged) when `keyboardType: TextInputType.visiblePassword`. Long-
press-to-select-accent is the trigger; the selection event doesn't reach
the TextField at all.

**Why engine-level.** Samsung-specific InputConnection behavior with
Android's visiblePassword input type. The Android embedder forwards
what Samsung emits; this particular long-press variant selection path
isn't handled for the password-variant input type. Fix is Android-
embedder scope.

**Dedup scan.** Shares "visiblePassword + Android embedder forwards
non-standard IME behavior" family with #142882 (visiblePassword
backspace) but different trigger. Earlier (in #59541 processing) I
noted this as a weak-related candidate for DK-1 (mobile dead-key
composition); on processing: the symptom is "no input at all" rather
than "two characters" — different mechanism. Not a DK-1 duplicate.

---

### #104950 — Unexpected backspace behavior via IME with composing character (macOS)

- **URL:** https://github.com/flutter/flutter/issues/104950
- **Created:** 2022-05-30 (~4.0 y old) · **Updated:** 2025-10-09
- **Reactions:** 0
- **Labels:** `a: text input`, `engine`, `platform-macos`, `a: internationalization`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 3.0/3.1`, `team-macos`, `triaged-macos`
- **Ownership:** `team-macos`
- **Decision:** **skip — engine-level**

**Root cause (per body).** macOS opt+u creates a composing diacritic
(`¨`). Pressing backspace should clear it; Flutter needs two
backspaces. Affects both super_editor and regular TextField.

**Why engine-level.** The macOS text input plugin doesn't translate
"backspace on composing character" into a clear-the-composing-range
signal on the first press. Engine-side fix in `FlutterTextInputPlugin.mm`.

**Dedup scan.** Shares thematic territory with MCIME-1 (macOS CJK IME
composing state) and DK-1 (mobile dead-key composition), but distinct:
MCIME-1 focuses on CJK-IME-specific composing; DK-1 is about dead-key
+letter → 2 chars on mobile; this one is macOS + macOS-system-level
dead-key (not CJK IME) backspace handling. Not a tight cluster member.

---

### #105244 — [Firefox] Composing down to single char doesn't replace until next event

- **URL:** https://github.com/flutter/flutter/issues/105244
- **Created:** 2022-06-02 (~4.0 y old) · **Updated:** 2024-03-06
- **Reactions:** 0
- **Labels:** `a: text input`, `engine`, `platform-web`, `browser: firefox`, `P2`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level** (Flutter web engine, Firefox-specific)

**Root cause (per summary).** Firefox sends a null composing region in
the same message as the committed text; Chrome sends two separate
updates. When composing goes from multiple characters to one composed
symbol in Firefox, Flutter's delta model doesn't replace until the next
keypress. Related to engine PR flutter/engine#33590 but not resolved.

**Why engine-level.** Firefox-specific DOM composition event sequencing
that the Flutter web engine's composing handler needs to accommodate.
Framework has no vantage.

---

### #108256 — [Desktop] Incorrect backspace handling with combined Khmer Unicode characters

- **URL:** https://github.com/flutter/flutter/issues/108256
- **Created:** 2022-07-25 (~3.7 y old) · **Updated:** 2025-10-09
- **Reactions:** 0
- **Labels:** `a: text input`, `engine`, `platform-macos`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 3.0/3.1`, `team-macos`, `triaged-macos`
- **Ownership:** `team-macos`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** After engine PR #115900, Flutter's
framework uses `CharacterRange.at()` (grapheme-cluster boundary) for
backspace deletion. For combined Khmer characters (consonant + vowel),
this deletes the whole grapheme cluster instead of one code point.
Not reproducible on mobile/web. Proposed fix direction: delete by
code point when no composing range active, delegate to IME when
composing. Notes that iOS's keyboard manager decomposes precomposed
Hangul and deletes jamo-at-a-time, suggesting platform delegation is
preferable.

**Why engine-level.** Although `CharacterRange.at()` is framework code,
the fix requires platform-specific delegation logic for desktop
embedders (iOS/Android already delegate to IME). The framework change
to code-point-based deletion for desktop is simple; the harder part is
defining when to delegate — a design decision that hasn't been made.

**Framework-testable note.** A framework test could assert backspace on
a Khmer grapheme cluster deletes one code point — but the assertion
encodes a design choice (code-point vs grapheme) that's unresolved.
Deferred. If the design decision firms up as "code-point always when
composing is empty", a regression test is straightforward.

---

### #113944 — Windows Japanese prompt window produces "100100100" (inputFormatter dup)

- **URL:** https://github.com/flutter/flutter/issues/113944
- **Created:** 2022-10-24 (~3.5 y old) · **Updated:** 2025-10-09
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `platform-windows`, `has reproducible steps`, `P3`, `found in release: 3.3/3.5`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Windows Japanese IME + a regex
`FilteringTextInputFormatter` (decimal pattern): selecting "100" from
the prompt window produces "100100100". Proposed fix: include
`composing: newValue.composing` when building the new `TextEditingValue`
in the formatter.

**Why engine-level.** The fix IS framework-side (in a formatter's
update path) and is clearly identified — but confirming it requires
driving the Windows Japanese IME commit flow in a test. The test
harness gap parallels #92050 (setComposingRect not emitted in mocked
channel). Categorized as skip-engine because the repro is embedder-
driven; future work can author the test once the setComposingRect-style
harness issue is solved.

**Dedup scan.** Thematic relative of the AIR-1 cluster (Android IME
restart on composing-region change) — both involve formatters
disturbing composing-region state. This one is Windows-side in a
single-commit rather than a restart loop; not a cluster member.

---

### #115903 — [iPadOS] Tab key doesn't cycle conversion window with physical keyboard

- **URL:** https://github.com/flutter/flutter/issues/115903
- **Created:** 2022-11-23 (~3.4 y old) · **Updated:** 2024-03-06
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-ios`, `framework`, `a: tablet`, `a: fidelity`, `has reproducible steps`, `P2`, `found in release: 3.3/3.6`, `team-ios`, `triaged-ios`
- **Ownership:** `team-ios`
- **Decision:** **likely-duplicate of #110647** (IHK-1 cluster)

**Root cause (per summary).** iPad physical keyboard + Japanese IME:
pressing Tab to cycle through IME candidates instead moves focus to
the next TextField. Flutter's keyboard shortcut handling intercepts
Tab before the platform can route it to IME candidate cycling.
Suggested fix: disable the Tab shortcut when the active text input is
composing (similar to the delete/backspace fix in #115900).

**Why duplicate.** Same root-cause family as #110647 / #135406 (IHK-1):
iOS hardware-keyboard key events consumed by Flutter's shortcut system
before reaching the IME candidate window. Different key (Tab vs
arrows), same underlying mechanism and same fix family (disable the
shortcut during composing).

**Cluster.** **IHK-1** (iOS hardware-keyboard IME candidate navigation)
— confirmed member.

---

### #120763 — Input methods get interrupted when TextField constraints change (web)

- **URL:** https://github.com/flutter/flutter/issues/120763
- **Created:** 2023-02-15 (~3.2 y old) · **Updated:** 2024-03-06
- **Reactions:** 0
- **Labels:** `a: text input`, `engine`, `platform-web`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 3.7/3.8`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — engine-level** (web engine)

**Root cause (per body).** On Flutter web (Chrome, Safari on macOS;
Windows reported), Chinese IME composing gets interrupted whenever the
TextField's layout constraints change, making it impossible to compose.
Pressing spacebar doesn't commit; mouse double-click does.

**Why engine-level.** Layout-driven IME interruption is a web-engine
text-input integration issue — the DOM input overlay loses composing
state when Flutter re-lays out its TextField. Framework has no vantage.

---

### #120852 — [macOS] TextField left arrow key while composing deletes text inside composing range

- **URL:** https://github.com/flutter/flutter/issues/120852
- **Created:** 2023-02-16 (~3.2 y old) · **Updated:** 2024-06-13
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `engine`, `a: internationalization`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 3.7/3.8`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level** (MCIME-1 cluster member)

**Root cause (per summary).** macOS Japanese IME: after committing some
text, then typing to bring up the candidate list, pressing left arrow
deletes text inside the composing range. In 3.7.3 the regression
worsened — left arrow also deletes text preceding the composing range.
macOS-only. Also triggers a macOS system error sound on arrow key press.

**Why engine-level.** macOS composing-state handling in
`FlutterTextInputPlugin.mm` — arrow-key event routing during active
composing doesn't correctly decide between "move within composing" vs
"delete composing content". Same file family as MCIME-1 siblings.

**Cluster.** **MCIME-1** (macOS CJK IME composing state) — confirmed
member.

---

### #124966 — macOS: updateEditingValue is not called when typing Chinese/non-English

- **URL:** https://github.com/flutter/flutter/issues/124966
- **Created:** 2023-04-17 (~3.0 y old) · **Updated:** 2025-10-09
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `engine`, `platform-macos`, `a: internationalization`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 3.7/3.10`, `team-macos`, `triaged-macos`
- **Ownership:** `team-macos`
- **Decision:** **skip — engine-level** (MCIME-1 cluster member)

**Root cause (per summary).** macOS + Pinyin/Chinese IME:
`updateEditingValue` is never called during composition; English input
is fine. macOS console reports `_TIPropertyValueIsValid called with 5
on nil context!` and related errors. Triager linked related #107462.
Also causes unexpected UI refreshes / text-field content wipes.

**Why engine-level.** The macOS plugin's bridge from Cocoa text-input
events to `updateEditingValue` platform-channel calls is what's
failing. Framework has no vantage.

**Cluster.** **MCIME-1** — confirmed member.

---

### #125765 — [Web] iPhone Japanese input disappears after line break + delete

- **URL:** https://github.com/flutter/flutter/issues/125765
- **Created:** 2023-04-30 (~3.0 y old) · **Updated:** 2024-03-06
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `platform-web`, `has reproducible steps`, `P2`, `c: parity`, `browser: safari-ios`, `found in release: 3.7/3.10`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level** (Flutter web engine)

**Root cause (per summary).** Flutter web on iOS Safari / Chrome only:
typing Japanese → line break → immediate single-char delete → more
input + confirm → entered text disappears. Does not reproduce on
Android web.

**Why engine-level.** iOS-Safari-specific web IME composition sequencing;
fix lives in the Flutter web engine's text-input integration.

**Dedup scan.** Summary mentions relation to #120351 (Samsung Android
batch-edit) but confirms distinct bugs. Joins the growing web-IME
issue set; no tight duplicate.

---

### #126263 — [TextField] Odd behavior with Microsoft IME Japanese Text on Windows (regression)

- **URL:** https://github.com/flutter/flutter/issues/126263
- **Created:** 2023-05-08 (~3.0 y old) · **Updated:** 2024-06-13
- **Reactions:** 0
- **Labels:** `a: text input`, `c: regression`, `engine`, `a: internationalization`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 3.7/3.11`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **skip — engine-level** (forms new cluster **CSR-1**)

**Root cause (per summary).** Windows Microsoft Japanese IME: after the
system underlines a composing region, clicking to move the cursor to
a different position during active composition duplicates preceded
text on next input. Root cause: the candidate list is not dismissed
when the cursor moves during active composition. Windows-only
(confirmed regression; web works; macOS has a related-but-different
"append to end" symptom; Linux can't reproduce due to no candidate list).

**Why engine-level.** Composing-state lifecycle on cursor movement is
owned by the Windows embedder (and the macOS embedder for its
related-but-different symptom). Framework has no vantage.

**Cluster.** New tentative cluster **CSR-1** (Composing state not
reset on position / text change). Paired with #128315 (iOS
programmatic text replacement leaves Japanese suggestion active),
which #128315's summary explicitly cross-references with this issue.
Shared theme: active composing state doesn't get reset by disruptive
framework-side changes (cursor move, programmatic text replacement).

---

### #126329 — [Linux] Chinese Sogou/fcitx candidate list positioned wrong

- **URL:** https://github.com/flutter/flutter/issues/126329
- **Created:** 2023-05-09 (~3.0 y old) · **Updated:** 2024-06-07
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `engine`, `a: internationalization`, `platform-linux`, `a: desktop`, `P2`, `team-linux`, `triaged-linux`
- **Ownership:** `team-linux`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Linux + Sogou/fcitx: candidate list stays
in lower-left corner instead of following the cursor. iBus works on
Ubuntu but intermittently fails (~10%). UOS (uniontech) + fcitx also
reproduces. Summary identifies the positioning as "IME-side" (fcitx),
not a pure Flutter bug — but Flutter's interaction with fcitx doesn't
provide the positioning hints fcitx could use.

**Why engine-level.** Linux GTK embedder <-> fcitx IM module
integration. Sibling of DSK-IME-1 (desktop IME candidate-window
positioning) theme — same symptom family, different platform with
different root cause (fcitx-side vs `setComposingRect(offset=0)`).
Not merged into DSK-IME-1; both are desktop-IME-positioning siblings.

---

### #128565 — isComposingRangeValid is inconsistent between platforms

- **URL:** https://github.com/flutter/flutter/issues/128565
- **Created:** 2023-06-09 (~2.9 y old) · **Updated:** 2026-02-27
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `has reproducible steps`, `P2`, `found in release: 3.10/3.12`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** `TextEditingValue.isComposingRangeValid`
returns different things across platforms. iOS correct: true only
during CJK composition, false after candidate confirmation. Android
(Gboard) incorrect: returns true even for English typing, returns
false for selected suggestions. Regression in 3.10.1–3.10.5. PR
#130081 was filed but not merged. Workaround via
`addPostFrameCallback` reported as unreliable. Linked to #174159.

**Why engine-level.** Although `isComposingRangeValid` is a framework-
side getter, its value comes from whatever composing range the
platform plugin sends. Android embedder (Gboard variant) sends a
composing range for English too; fix must land in the Android plugin
to not report composing range for non-composing-IME typing. Framework
getter is just reading the wrong input.

**Dedup scan.** Related thematically to AIR-1 (Android IME restart on
composing-region change) — both involve Android embedder emitting
inappropriate composing-region state. Different symptom (restart vs
inconsistent-validity flag), possibly shared plumbing. Not
classifying as a tight AIR-1 member without clearer shared
root-cause evidence.

---

### #130654 — [Web] canvaskit + StrutStyle + useMaterial3 breaks Japanese input

- **URL:** https://github.com/flutter/flutter/issues/130654
- **Created:** 2023-07-15 (~2.8 y old) · **Updated:** 2024-02-29
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: internationalization`, `platform-web`, `has reproducible steps`, `P2`, `found in release: 3.10`, `team-web`, `triaged-web`, `found in release: 3.13`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level** (Flutter web engine / canvaskit)

**Root cause (per summary).** Flutter web + canvaskit renderer +
StrutStyle + useMaterial3 + Japanese multi-keystroke input (e.g. 'ka'
= k+a as first char) → first character doubled (`ｋｋあ` for 'ka' input).
HTML renderer unaffected. Console reports HardwareKeyboard key-up/down
mismatches (flagged as separate issue).

**Why engine-level.** Very specific web-canvaskit + Material-3 theme
interaction with IME key event timing. Fix lives in the web engine's
canvaskit text-input path.

---

### #132272 — [macOS] Provide a way to close the accent panel programmatically

- **URL:** https://github.com/flutter/flutter/issues/132272
- **Created:** 2023-08-09 (~2.7 y old) · **Updated:** 2025-10-09
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `framework`, `platform-macos`, `d: api docs`, `c: proposal`, `a: desktop`, `P3`, `team-macos`, `triaged-macos`
- **Ownership:** `team-macos`
- **Decision:** **skip — feature/proposal**

**Scope.** Request: add a `TextInputConnection` method to
programmatically close macOS's accent panel, so super_editor (which
handles BACKSPACE via onKey) can dismiss the panel after consuming
the key event. Comments note `InputMethodKit`'s `hidePalettes` may
work as the underlying API.

**Why skip.** `c: new feature` / `c: proposal`. API-surface expansion.

---

### #134092 — [web] Typing compound characters generates unexpected deltas on Safari

- **URL:** https://github.com/flutter/flutter/issues/134092
- **Created:** 2023-09-06 (~2.6 y old) · **Updated:** 2024-05-09
- **Reactions:** 0
- **Labels:** `a: text input`, `engine`, `platform-web`, `has reproducible steps`, `browser: safari-macos`, `assigned for triage`, `P2`, `team-web`, `triaged-web`, `found in release: 3.13/3.14`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level** (Flutter web engine, Safari-specific)

**Root cause (per summary).** Safari/WebKit reports a
`TextEditingDeltaInsertion` for a dead-key (`~`, OPTION+U) with an
uncollapsed selection, then a separate `TextEditingDeltaNonTextUpdate`
to collapse it. Flutter's delta system calls `setEditingState` between
these two deltas because the editor's selection differs from the IME's,
which prevents the follow-up non-text delta from arriving and breaks
IME composition. Web/Safari only. Renzo-Olivares proposed batching the
two deltas; was unassigned due to inactivity.

**Why engine-level.** Fix requires the web engine's delta pipeline to
batch Safari's two-part dead-key + collapse sequence before calling
back to the framework. Framework has no web-engine delta-pipeline
vantage.

---

### #134268 — [Web] Unable to detect if a native IME panel is opened

- **URL:** https://github.com/flutter/flutter/issues/134268
- **Created:** 2023-09-08 (~2.6 y old) · **Updated:** 2023-11-09
- **Reactions:** 0
- **Labels:** `a: text input`, `has reproducible steps`, `P2`, `team-web`, `triaged-web`, `found in release: 3.13/3.14`
- **Ownership:** `team-web`
- **Decision:** **skip — feature/proposal**

**Scope.** super_editor handles arrow keys for selection navigation
which prevents arrow keys from reaching the native IME panel
(emoji picker, Japanese suggestion panel). Request: a framework-level
API to check whether an IME panel is currently displayed, so apps can
conditionally bubble arrow keys to the OS.

**Why skip.** Framework API request; no bug to regress. Workaround
exists (`composing.isValid`) but breaks at right-edge selection edge
case. The real fix is a new framework API surface — out of scope.

---

### #134398 — UndoHistoryController does not function properly with Japanese

- **URL:** https://github.com/flutter/flutter/issues/134398
- **Created:** 2023-09-11 (~2.6 y old) · **Updated:** 2025-09-25
- **Reactions:** 0
- **Labels:** `a: text input`, `f: material design`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 3.13/3.14`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Undo during CJK composition is broken in
two different ways across platforms: non-Android platforms prevent
coalescing during CJK composition to avoid interference, so undo has
no effect and the initial composing state isn't saved to history; on
Android, the embedder calls `restartInput` after undo, adding
unexpected history entries. Renzo-Olivares had a POC fix that caused
regressions.

**Why engine-level.** Android branch of the bug is embedder-scope
(`restartInput` after undo); the non-Android branch is a design
question about how undo should interact with composing state that
the framework has already decided not to do. No clean framework-only
fix; blocking layer for both branches is engine/embedder.

---

### #134926 — [Web] ATOK 2014 underline on text is misaligned on Japanese keyboard

- **URL:** https://github.com/flutter/flutter/issues/134926
- **Created:** 2023-09-18 (~2.6 y old) · **Updated:** 2023-09-28
- **Reactions:** 0
- **Labels:** `a: text input`, `a: internationalization`, `platform-web`, `P2`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level** (Flutter web engine)

**Root cause (per summary).** Flutter web + ATOK 2014 IME: after
converting `a` + space → `阿`, the composing underline renders at `a`
instead of `阿`. ATOK 2014-specific; system IME and other IMEs work
correctly. Windows desktop unaffected.

**Why engine-level.** Web-specific composing-underline rendering bug
triggered by ATOK 2014's particular composition sequence. Fix in web
engine.

---

### #137677 — macOS Pinyin-Simplified: navigation box positioned incorrectly with selection

- **URL:** https://github.com/flutter/flutter/issues/137677
- **Created:** 2023-11-01 (~2.5 y old) · **Updated:** 2024-06-07
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-macos`, `a: internationalization`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 3.13/3.16`, `team-macos`, `triaged-macos`
- **Ownership:** `team-macos`
- **Decision:** **skip — engine-level** (partial fix landed)

**Root cause (per summary).** macOS: paste long text → select lines →
type Pinyin → IME navigation box at wrong position. Fix landed in
#137863 (using selection.start instead of selection.baseOffset); only
addresses horizontal positioning. The remaining case — TextField
widget itself changing size/position as text is typed — persists.

**Why engine-level.** Remaining case needs macOS plugin to observe
widget reposition and update IME coordinates mid-composing. Partial
fix already landed; remaining is an edge case at lower priority.

**Dedup scan.** DSK-IME-1 family (desktop IME candidate positioning).
The #137863 fix and the remaining case don't overlap with #92050's
`editable_text.dart:5021` root cause — different mechanism. Stands
outside the tight DSK-IME-1 cluster.

---

### #139603 — [Windows][Web] Unexpected deltas when using Japanese keyboard

- **URL:** https://github.com/flutter/flutter/issues/139603
- **Created:** 2023-12-05 (~2.4 y old) · **Updated:** 2024-06-27
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `platform-web`, `has reproducible steps`, `P2`, `found in release: 3.16/3.18`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level** (Flutter web engine)

**Root cause (per summary).** Windows Chrome web + Japanese Hiragana
IME: first letter produces a duplicated output (`ｋ...ｋ`). Root cause:
`setEditingState` called to resync after IME update → second delta
insertion at wrong offset. Not reproducible on Windows desktop or
macOS Chrome.

**Why engine-level.** The `setEditingState` resync timing vs IME
updates is a web-engine delta-pipeline issue. Framework receives the
deltas after the issue has occurred.

---

### #140537 — when using 3-set Korean keyboard, TextField ignores space on Windows

- **URL:** https://github.com/flutter/flutter/issues/140537
- **Created:** 2023-12-22 (~2.3 y old) · **Updated:** 2025-03-18
- **Reactions:** 0
- **Labels:** `a: text input`, `a: internationalization`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 3.16/3.18`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **skip — engine-level** (WKI-1 cluster confirmed member)

**Root cause (per summary).** Windows 3-beolsik Korean IME: pressing
space produces no space character in TextField. Key event is detected
but not resolved. Not reproducible with 2-beolsik Korean IME. Windows-
specific.

**Why engine-level.** Windows embedder's handling of specific Korean
keyboard layout space-key events. Shares surface with other WKI-1
issues touching the Windows Korean IME code path.

**Cluster.** **WKI-1** — confirmed member.

---

### #142493 — [macOS] Japanese-kana with live conversion disabled produces weird characters

- **URL:** https://github.com/flutter/flutter/issues/142493
- **Created:** 2024-01-29 (~2.2 y old) · **Updated:** 2025-10-09
- **Reactions:** 0
- **Labels:** `a: text input`, `engine`, `platform-macos`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 3.16/3.19`, `team-macos`, `triaged-macos`
- **Ownership:** `team-macos`
- **Decision:** **skip — engine-level** (MCIME-1 cluster confirmed member)

**Root cause (per summary).** macOS + Japanese-Kana keyboard with
"Live Conversion" disabled: picking a suggestion produces invalid
characters (e.g., `^_`) before the correct text. Also reproduces on
web (CanvasKit). Summary flags #149379 as a possible duplicate.

**Why engine-level.** The delta stream from macOS plugin includes an
invalid-character replacement before the correct text, indicating the
plugin's composing commit sequence is wrong for the "live conversion
disabled" path.

**Cluster.** **MCIME-1** — confirmed member. This is the #142493 that
MCIME-1 was watching for as a "possibly related" member; confirmed on
processing.

---

### #145887 — Korean input on Android adding spaces between characters (controller misuse pattern)

- **URL:** https://github.com/flutter/flutter/issues/145887
- **Created:** 2024-03-28 (~2.1 y old) · **Updated:** 2024-04-04
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-android`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **likely-stale (signal-based)**

**Root cause (per summary).** Setting `_textController.text = v` inside
the onChange callback (reassigning rather than updating) disrupted
composing state on Android with Korean input. After a Gboard update,
the original reproducer no longer reproduces; the issue only
manifests with this misuse pattern.

**Why likely-stale.** Summary explicitly states: "After the Gboard
update this is not reproducible via the original code; the issue only
manifests with the misuse pattern." This is a strong stale signal —
the user-visible bug is resolved by the upstream (Gboard) change, and
the remaining "issue" is an anti-pattern in user code that Flutter
shouldn't necessarily prevent. **Recommendation:** close with a note
pointing at the misuse pattern and the Gboard resolution.

**Verification.** No code change in Flutter closed this; it stopped
reproducing because Gboard changed. A quick real-device test on
current Gboard should confirm before closing.

**Dedup scan.** Thematic cousin of AIR-1 (Android IME restart on
composing-region change) — the controller-reassignment pattern is
exactly the kind of framework disruption that triggers AIR-1-style
restarts. Related pattern, different specific trigger.

---

### #152729 — [Windows] Suggestion window offset wrong for the first character

- **URL:** https://github.com/flutter/flutter/issues/152729
- **Created:** 2024-08-02 (~1.7 y old) · **Updated:** 2024-08-08
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `platform-windows`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.22/3.24`
- **Ownership:** `team-text-input`
- **Decision:** **likely-duplicate of #92050** (DSK-IME-1 cluster member)

**Root cause (per summary + DSK-IME-1 context).** Windows 11 Microsoft
Pinyin: candidate window jumps to correct position only after the
**second** character; first character is wrong. Web renders correctly
from first char. Similar observed on macOS.

**Why duplicate.** Textbook manifestation of the DSK-IME-1 bug:
when composing starts fresh (first character, empty
TextEditingValue.composing), `composingRange.isValid` is false, so
`setComposingRect` sends rect-at-offset-0 — then the second character
establishes a valid composing range and the rect correction happens.
Same fix (use `selection.baseOffset` when composingRange invalid)
eliminates the first-character miss.

**Cluster.** **DSK-IME-1** — confirmed member (previously tentative
"first character wrong" candidate).

---

### #153895 — [macOS] Dismissing the IME accent panel produces invalid character

- **URL:** https://github.com/flutter/flutter/issues/153895
- **Created:** 2024-08-21 (~1.7 y old) · **Updated:** 2024-11-06
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-macos`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.24/3.25`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** macOS press-hold letter → accent panel
→ arrow keys + ESC → left arrow → invalid character. Reproduces with
regular TextField, not just custom DeltaTextInputClient. Two distinct
sequences with different expected outcomes documented.

**Why engine-level.** macOS plugin's handling of accent-panel dismiss
+ arrow-key sequence. Framework has no vantage; the accent panel is
managed by macOS and the plugin bridges its state.

**Dedup scan.** Thematic cousin of #132272 (macOS accent panel close
API request) but distinct: #132272 asks for an API to dismiss the
panel; #153895 is a bug in how panel dismiss currently flows. Also
cousin of #104950 (macOS backspace on composing character from opt+u)
— same macOS-dead-key composing-state territory. Holding as cousins,
not tight duplicates.

---

### #154055 — Keyboard events: dead key, should not generate character

- **URL:** https://github.com/flutter/flutter/issues/154055
- **Created:** 2024-08-24 (~1.7 y old) · **Updated:** 2025-10-09
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `has reproducible steps`, `P2`, `team-framework`, `triaged-framework`, `found in release: 3.24/3.25`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level** (forms new cluster **DKD-1**)

**Root cause (per summary).** French input method: pressing `[` (dead
key for `^`) generates `^` as a character on first keystroke, and the
second keystroke `e` generates `ê` only on Windows. Linux and macOS
show a related but distinct problem where the second keystroke
produces `e` instead of the composed `ê`. Confirmed framework-level
by team; framework-labeled ownership.

**Why engine-level.** Although labeled framework, the relevant
key-event state machine (dead-key detection + deferred character
emission) is shared between the Linux/macOS embedders and the
framework-side key-event translation. `LogicalKeyEvent.character`
computation for composed-character cases needs platform-plugin
cooperation. Test harness would need per-platform embedder behavior.

**Cluster.** New tentative cluster **DKD-1** (Desktop dead-key
composition). Sibling of DK-1 (mobile), but desktop-specific fix
path — framework/embedder dead-key state machine rather than
mobile `CharacterCombiner`-style handler.

---

### #154069 — Windows: AltGr generates Control Left + Alt Right instead of altGraph

- **URL:** https://github.com/flutter/flutter/issues/154069
- **Created:** 2024-08-25 (~1.7 y old) · **Updated:** 2025-10-09
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `platform-windows`, `has reproducible steps`, `P2`, `team-windows`, `triaged-windows`, `found in release: 3.24/3.25`
- **Ownership:** `team-windows`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Windows reports AltGr as Ctrl+Alt at the
OS level; Flutter doesn't collapse this into a single
`LogicalKeyboardKey.altGraph` event. Ambiguity: apps can't distinguish
"user pressed AltGr on fr-FR" from "user pressed Ctrl Left + Alt Right
on en-US." Doesn't reproduce on macOS or web.

**Why engine-level.** Windows embedder should recognize the
synthetic Ctrl+Alt as AltGr and emit a single altGraph event.
Framework-side collapse is possible in principle but fragile; the
authoritative fix is at the Windows embedder's key-event translation
layer.

---

### #154160 — Linux/macOS: dead keys produce wrong character on second keystroke

- **URL:** https://github.com/flutter/flutter/issues/154160
- **Created:** 2024-08-27 (~1.7 y old) · **Updated:** 2025-10-09
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `platform-macos`, `a: internationalization`, `platform-linux`, `has reproducible steps`, `P2`, `team-framework`, `triaged-framework`, `found in release: 3.24/3.25`
- **Ownership:** `team-framework`
- **Decision:** **likely-duplicate of #154055** (DKD-1 cluster member)

**Root cause (per summary).** On Linux and macOS with French layout:
pressing dead key `[` then `e` should produce `ê`, but the resulting
`KeyDownEvent` carries `character: "e"` instead. Does not reproduce
on Windows (which has #154055 instead as its variant).

**Why duplicate.** Same root-cause family as #154055: desktop
dead-key composition produces wrong `KeyEvent.character`. The two
issues were filed explicitly cross-referencing each other (this one
was filed from #154055's comment #2309898881). Same DKD-1 cluster.

**Cluster.** **DKD-1** — confirmed member.

---

### #154692 — Text duplication with Microsoft Translate (SwiftKey AI) keyboard on Android

- **URL:** https://github.com/flutter/flutter/issues/154692
- **Created:** 2024-09-05 (~1.6 y old) · **Updated:** 2024-09-26
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-android`, `a: internationalization`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.24/3.25`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Microsoft SwiftKey AI Keyboard on
Android: English-to-Japanese translation with a trailing space after
the source word duplicates the text in the TextField. Reproduced on
Pixel 7 Android 14 stable 3.24.2 and master.

**Why engine-level.** SwiftKey's non-standard InputConnection
sequencing around translated-text commits; the Android embedder
forwards its output as-is. Same "Android embedder forwards
non-standard IME behavior" pattern as AIR-1's members and
#98720/#184744 phantom-shift; different specific trigger (translate +
trailing space).

---

### #156183 — [iOS] iPad Portuguese keyboard: `´`+a deletes character (iOS 17.5 simulator)

- **URL:** https://github.com/flutter/flutter/issues/156183
- **Created:** 2024-10-03 (~1.6 y old) · **Updated:** 2024-10-18
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-ios`, `a: tablet`, `a: internationalization`, `e: OS-version specific`, `has reproducible steps`, `P3`, `team-text-input`, `triaged-text-input`, `found in release: 3.24/3.26`
- **Ownership:** `team-text-input`
- **Decision:** **likely-stale (signal-based)**

**Root cause (per summary).** iPad Air 13" iOS 17.5 simulator +
Portuguese (Portugal) keyboard: pressing `´` then `a` produces `A`
(deletes the character unexpectedly) instead of `Á`. Does not
reproduce on iOS 18.0. **Testing on native iOS 17.5 (Reminders app)
shows the same bug** — this is an iOS 17.5 simulator bug, not
Flutter-specific.

**Why likely-stale.** Two independent signals: (a) iOS 18 fixes it
in Apple's own implementation, (b) the bug reproduces in native iOS
17.5 apps (Reminders), confirming it's external to Flutter.
**Recommendation:** close with a note that this is an Apple-side
iOS 17.5 simulator bug fixed in iOS 18, and not within Flutter's scope.

---

### #156184 — [iOS] iPad Portuguese compound character creates extra character

- **URL:** https://github.com/flutter/flutter/issues/156184
- **Created:** 2024-10-03 (~1.6 y old) · **Updated:** 2024-10-17
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-ios`, `framework`, `a: tablet`, `a: internationalization`, `has reproducible steps`, `P3`, `team-text-input`, `triaged-text-input`, `found in release: 3.24/3.26`
- **Ownership:** `team-text-input`
- **Decision:** **likely-duplicate of #59541** (DK-1 cluster)

**Root cause (per summary).** iPad iOS 17.5 + Portuguese (Portugal)
keyboard: `´` + `a` produces `´á` instead of `Á`. Still reproduces
on iOS 18 (unlike sibling #156183). Filed at the same time as
#156183 but with a different symptom (extra-char, not character-
deletion).

**Why duplicate.** Classic DK-1 symptom: dead-key + letter →
composed char *plus* leftover dead-key glyph (`´á` instead of `Á`).
Matches #146486 (iOS umlauts), #87257 (iPad French/Spanish soft
keyboard), #59541 (iOS external keyboard Spanish accented chars).
The Portuguese variant extends DK-1's reach further into the
dead-key-bearing European layouts on iPad.

**Cluster.** **DK-1** — confirmed member (fifth).

---

### #157771 — PhysicalKeyboardKey wrong with Backspace/Enter when using CJK IME on Android emulator

- **URL:** https://github.com/flutter/flutter/issues/157771
- **Created:** 2024-10-29 (~1.5 y old) · **Updated:** 2025-09-20
- **Reactions:** 0
- **Labels:** `a: text input`, `e: device-specific`, `platform-android`, `a: internationalization`, `has reproducible steps`, `P2`, `team-android`, `triaged-android`, `found in release: 3.24/3.27`
- **Ownership:** `team-android`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Android emulator (Pixel 4 API 34) +
Samsung Galaxy S10 tablet: switching between English and ko/zh/ja
IMEs produces incorrect `PhysicalKeyboardKey` USB HID usage on
Enter/Backspace. Does not reproduce on Pixel 7 or Pixel Tablet
physical devices. Backspace/Enter still functionally work — only the
key metadata is wrong.

**Why engine-level.** Emulator-specific (and one tablet) key-event
translation in the Android embedder. Fix is Android-embedder-side
USB HID usage mapping when CJK IME is active. Logging-only impact
— doesn't break functionality.

---

### #159634 — [Android] CJK IME candidate window position wrong with external keyboard

- **URL:** https://github.com/flutter/flutter/issues/159634
- **Created:** 2024-11-30 (~1.4 y old) · **Updated:** 2025-07-17
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-android`, `a: internationalization`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Android + physical keyboard + CJK IME:
candidate window always appears at lower-left origin. Root cause
pinpointed by community: `InputConnectionAdaptor.getCursorAnchorInfo()`
at `shell/platform/android/io/flutter/plugins/editing/InputConnectionAdaptor.java`
never calls `setInsertionMarkerLocation`. A community patch using
`mLayout.getPrimaryHorizontal` corrected horizontal placement but
left vertical at origin. No official PR.

**Why engine-level.** Explicit Android engine file named;
`InputConnectionAdaptor.java` is the fix target. Framework has no
vantage for Android IME candidate positioning.

**Dedup scan.** Sibling of DSK-IME-1 (desktop IME candidate-window
positioning) but Android-specific with a distinct embedder pinpoint.
Same theme family — "IME candidate window positioning requires
embedder to send coordinates correctly" — but different platform
surfaces.

---

### #163946 — Web Chinese candidate box doesn't follow cursor

- **URL:** https://github.com/flutter/flutter/issues/163946
- **Created:** 2025-02-23 (~1.2 y old) · **Updated:** 2025-03-12
- **Reactions:** 0
- **Labels:** `a: text input`, `a: internationalization`, `platform-web`, `has reproducible steps`, `P2`, `team-web`, `triaged-web`, `found in release: 3.29/3.30`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level** (Flutter web engine)

**Root cause (per summary).** Flutter web + multiline TextField +
Chinese IME: candidate box stays at bottom initially, then at left
with offset after maxLines reached. Not reproducible on macOS /
Windows desktop. Web-only. A commenter linked to #149979 as possible
shared root cause.

**Why engine-level.** Web-engine IME candidate coordinate handling.
Fix likely lives in web engine's text-input overlay positioning.

**Dedup scan.** Another entry in the growing Web-IME candidate
position issue set (#149979, #101222, #163946). All web-only IME
positioning issues with different sub-symptoms but shared "Flutter
web doesn't correctly report caret position to the browser IME"
theme. Not formally clustering here since root causes diverge —
revisit if more gather.

---

### #165734 — [Android] IME connection closure not reported on swipe-back

- **URL:** https://github.com/flutter/flutter/issues/165734
- **Created:** 2025-03-22 (~1.1 y old) · **Updated:** 2025-03-27
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-android`, `framework`, `f: focus`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.29/3.31`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Swipe from right edge on Android
(back gesture) closes the keyboard but Flutter's TextInput connection
is not notified of IME closure. TextField retains focus and selection;
Flutter still thinks the keyboard is open. Confirmed on stable 3.29.2
and master 3.31.0.

**Why engine-level.** Android system-gesture detection is an embedder
concern; the embedder needs to detect the back-swipe and propagate
the IME-closure signal to the framework. Framework has no direct
vantage on system gestures.

**Dedup scan.** Thematic cousin of #117771 (proposal for
`TextInputConnection` closure listener) — both about connection-state
notification gaps — but #117771 is about framework API surface;
this one is the underlying notification not firing at all on a
specific trigger. Different layers; not a cluster.

---

### #168588 — [Firefox] macOS emoji picker doesn't input emoji (focus removes input element)

- **URL:** https://github.com/flutter/flutter/issues/168588
- **Created:** 2025-05-09 (~1.0 y old) · **Updated:** 2025-05-21
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-macos`, `platform-web`, `has reproducible steps`, `browser: firefox`, `P2`, `team-web`, `triaged-web`, `found in release: 3.29/3.32`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level** (Flutter web engine)

**Root cause (per summary).** Firefox + macOS web: TextField loses
focus when the emoji picker opens, and Flutter removes the underlying
`<input>` DOM element. When the user picks an emoji, there's no
element to receive it.

**Why engine-level.** Web engine's lifecycle management of the
`<input>` overlay on focus change. Fix is to keep the element alive
across brief focus-loss transitions.

---

### #171068 — [iOS] Chinese Pinyin leaves invisible U+2006 characters on focus change

- **URL:** https://github.com/flutter/flutter/issues/171068
- **Created:** 2025-06-24 (~0.8 y old) · **Updated:** 2025-07-24
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-ios`, `a: internationalization`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.32/3.33`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level** (CSR-1 cluster add)

**Root cause (per summary).** iOS Pinyin composing state: tapping a
second TextField without confirming the composition leaves
`U+2006` six-per-em space separator characters embedded in the first
field's text. Native iOS UITextField cleans these up on focus loss;
Flutter doesn't. Comment notes the fix will be easier once
`EditableTextState` handles `resignFirstResponder` synchronously.

**Why engine-level.** Cleanup requires coordinating the iOS text
input plugin's response to `resignFirstResponder` with the framework's
`EditableTextState` focus lifecycle — the hand-off is asynchronous
today, leaving composing state to flush onto the field.

**Cluster.** **CSR-1** (Composing state not reset on disruptive
change) — confirmed member. This is the focus-change variant; joins
programmatic-replacement (#128315) and cursor-move (#126263) cases.

---

### #171319 — [Windows] Suggestion window stuck at same position with external keyboard

- **URL:** https://github.com/flutter/flutter/issues/171319
- **Created:** 2025-06-28 (~0.8 y old) · **Updated:** 2025-07-25
- **Reactions:** 0
- **Labels:** `a: text input`, `e: device-specific`, `a: internationalization`, `platform-windows`, `a: desktop`, `P3`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **likely-duplicate of #92050** (DSK-IME-1 cluster)

**Root cause (per body + DSK-IME-1 context).** Windows + Chinese IME +
external keyboard on notebook computers: IME auxiliary input box
stays in the upper-left corner. macOS unaffected.

**Why duplicate.** Textbook DSK-IME-1 manifestation: stuck-at-origin
candidate window is the signature of the `setComposingRect(offset=0)`
bug. This issue is the "stays at 0,0 throughout" variant (rather than
per-keystroke flicker like #128323 or per-first-character like #152729).

**Cluster.** **DSK-IME-1** — confirmed member (previously tentative
"candidate window stuck" candidate).

---

### #174159 — TextEditingController.value.composing gives wrong results on Web & iOS

- **URL:** https://github.com/flutter/flutter/issues/174159
- **Created:** 2025-08-20 (~0.7 y old) · **Updated:** 2026-04-03
- **Reactions:** 0
- **Labels:** `a: text input`, `platform-ios`, `framework`, `engine`, `f: material design`, `platform-web`, `has reproducible steps`, `P2`, `c: parity`, `team-text-input`, `triaged-text-input`, `found in release: 3.35/3.36`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level** (CSR-1 cluster add)

**Root cause (per summary).** After a Pinyin IME commit, the
composing range should reset to `(-1, -1)`. On macOS and Android it
does; on Web and iOS it stays at the pre-commit range (e.g. `(0, 2)`).
Likely regression from #161593. Rooted in a behavioral difference
between Chinese and Japanese IMEs. Resolution: update `TextField.onChanged`
documentation to clarify IME composing limitations and recommend
`addListener` as the workaround.

**Why engine-level.** Although the observation surface is a framework
getter (`TextEditingController.value.composing`), the underlying
value comes from the iOS plugin / web engine. Fix lives in those
plugins' post-commit state reset. Team resolution leaned toward
docs, but the behavior inconsistency remains.

**Cluster.** **CSR-1** — confirmed member (post-commit variant of
composing-state-not-reset).

---

### #177360 — [Android] [Chromecast with Google TV] Software keyboard arrow navigation broken

- **URL:** https://github.com/flutter/flutter/issues/177360
- **Created:** 2025-10-22 (~0.5 y old) · **Updated:** 2026-01-07
- **Reactions:** 0
- **Labels:** `a: text input`, `e: device-specific`, `platform-android`, `P2`, `team-text-input`, `triaged-text-input`, `a: tv`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Android TV (Chromecast with Google TV,
plus some Phillips and Samsung TVs): arrow-key D-pad navigation on
the software keyboard doesn't move between letters, making text input
impossible. Hot restart temporarily fixes it. Google has rejected
Flutter TV app submissions because of this. A community contributor's
`InputConnectionAdaptor.java` patch attempt was unsuccessful.

**Why engine-level.** Android TV embedder's InputConnectionAdaptor
interaction with D-pad events on software keyboards. Deep Android
embedder work.

**Status note.** Highest-impact Android TV bug in IME/CJK — blocks
Flutter apps from shipping on Google TV. Worth surfacing to the
Android team roadmap outside this cleanup.

---

### #181487 — [Windows] TextField cannot completely disable system IME

- **URL:** https://github.com/flutter/flutter/issues/181487
- **Created:** 2026-01-26 (~0.2 y old) · **Updated:** 2026-03-15
- **Reactions:** 0
- **Labels:** `a: text input`, `c: new feature`, `framework`, `engine`, `a: internationalization`, `platform-windows`, `c: proposal`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Scope.** Request for a TextField property / API to completely
disable the Windows system IME for scenarios like OTP/PIN entry and
terminal-style inputs. Existing properties (`keyboardType`,
`textInputAction`, `inputFormatters`) don't suppress IME composition
state. Third-party plugin `force_english_ime` exists as workaround.

**Why skip.** `c: proposal` / `c: new feature`. Thematically adjacent
to #134330 (password field IME restriction, processed batch 6) —
both asking for IME suppression on desktop but from different
angles: #134330 is the existing-API-should-already-do-this framing,
#181487 is the new-API-request framing.

---

### #183078 — [Web] Korean IME composing range assertion after window blur (Cmd+Tab)

- **URL:** https://github.com/flutter/flutter/issues/183078
- **Created:** 2026-03-01 (~0.1 y old) · **Updated:** 2026-03-17
- **Reactions:** 0
- **Labels:** `a: text input`, `framework`, `platform-web`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level** (CSR-1 cluster add)

**Root cause (per summary).** Flutter web + Chrome macOS + Korean
2-Set IME: while composing, pressing Cmd+Tab to switch apps fires a
`compositionend` event in the DOM which removes the composing text,
but Flutter's internal composing range isn't updated. Backspace then
fires a `TextEditingValue` assertion (`composingExtent > text.length`
— e.g., `composingExtent: 2, text.length: 1`). After the assertion,
all key inputs stop working.

**Why engine-level.** The root cause is in the web engine's
composition event handling on window blur: `compositionend` isn't
translated into a composing-range reset for the framework side. A
community contributor has expressed interest in fixing.

**Cluster.** **CSR-1** — confirmed member (window-blur variant of
composing-state-not-reset).

---

## Duplicate clusters

### Cluster WKI-1: Windows Korean IME family (tentative, shared-root-cause)

Not tight duplicates — distinct symptoms — but all touch the Windows
embedder's Korean IME handling. A single fix pass in that code path could
plausibly address multiple. Worth coordinating.

- **#140739** (10 reactions, P2) — composing caret drawn one position ahead · **processed**
- **#121376** (6 reactions) — Korean input buffer issue after clear · **processed**
- **#130559** (5 reactions) — backspace + maxLength with Korean IME · **processed**
- **#166400** (1 reaction, P3) — Windows 10: Korean-to-Hanja conversion · **processed**
- **#140537** (0 reactions, P2) — space bar ignored with 3-beolsik Korean keyboard · **processed**

Canonical for coordination: **#140739** (most reactions, P2, with the
tightest pinpoint — composing caret drawn one position ahead tied to
Windows Korean in-place composition handling) recommended as cluster
home. All five members touch the Windows embedder's Korean IME handling
code and can plausibly be addressed by one coordinated fix pass.

### Cluster DSK-IME-1: Desktop IME candidate-window positioning (tentative)

Same root cause — Flutter's `setComposingRect` path (see
`editable_text.dart:5021`) sends rect-at-offset-0 when `composingRange` is
invalid, so OS-level IME candidate windows end up mispositioned.

- **#92050** (7 reactions, P2) — Sogou dropdown mispositioned after commit; pinpointed fix path · **processed**
- **#79933** (6 reactions, P2) — Sogou candidate window doesn't track caret (more general framing); older filing · **processed**
- **#128323** (1 reaction, P2) — Windows 10 Chinese candidate flickers at 0,0 between keystrokes · **processed**
- **#152729** (0 reactions, P2) — Windows 11 Microsoft Pinyin: candidate wrong for first char, correct from second · **processed**
- **#171319** (0 reactions, P3) — Windows Chinese IME + external keyboard: suggestion window stuck at upper-left · **processed**

Canonical (fix-coordination): recommend **#79933** as cluster home given
its broader scope and older filing date; carry #92050's fix-path notes
(`editable_text.dart:5021`, use `selection.baseOffset` when composingRange
invalid) into #79933. The #128323 flicker is the same bug observed in a
per-frame racing form.

**Candidate additional members** (desktop IME candidate-window positioning,
different IMEs / triggers — to verify when processed): #113944 Japanese
prompt window Windows, #152729 suggestion window offset first-character
Windows, #171319 suggestion window stuck external-keyboard Windows.

### Cluster CWB-1: CJK word breaks (tight-duplicate, shared root cause)

Missing CJK word-segmentation dictionary in the engine's ICU data. Every
consumer of `TextPainter.getWordBoundary` on CJK text — long-press word
selection, double-tap word selection, modifier+arrow word cursor nav —
returns single-character ranges. One fix (ship CJK dictionary / delegate
to platform tokenizers) closes multiple bug reports.

- **#19584** (11 reactions, P3) — long-press / double-tap CJK word selection · **processed, regression test authored (failing)** · **canonical**
- **#123065** (2 reactions, P2) — ctrl/option+arrow word nav on desktop · **processed, likely-duplicate**

The #19584 regression test covers the shared API — a pass there will
signal both are fixed.

### Cluster MCIME-1: macOS CJK IME composing state (tentative, shared-root-cause) — formerly MJIME-1

Shared surface `FlutterTextInputPlugin.mm` — macOS engine text-input
plugin's handling of CJK IME composing/commit state. Renamed from
MJIME-1 (Japanese-only) to cover Chinese as well. Distinct symptoms,
shared embedder code path.

- **#149379** (2 reactions, P2) — Japanese: text duplicated on Enter to confirm; possible-stale per later comment · **processed**
- **#153065** (2 reactions, P2) — Japanese: delta state inconsistency on suggestion-panel navigation · **processed**
- **#91861** (1 reaction, P2) — Chinese Pinyin: IME backspace fails to ignore decorational spaces · **processed**
- **#120852** (0 reactions, P2) — Japanese: left arrow during composing deletes text; regression worsened in 3.7.3 · **processed**
- **#124966** (0 reactions, P2) — Chinese: `updateEditingValue` never called; `_TIPropertyValueIsValid` errors · **processed**
- **#142493** (0 reactions, P2) — Japanese-Kana live-conversion-off: invalid char delta on suggestion pick · **processed**

Canonical for coordination: **#149379** (highest reactions, most
complete write-up, cross-referenced as possible-stale candidate).
All six members touch `FlutterTextInputPlugin.mm` and relate to CJK
composing-state handling. A single plugin refactor pass could close
several simultaneously.

### Cluster CRC-1: Composing-region cursor clamping (tentative, shared root cause)

Flutter does not clamp the caret to the active composing region the way
native iOS and Android do. On iOS the plugin (UITextInput bridge) keeps
treating the cursor as end-of-composing after a user moves it inside;
on Android/Gboard the cursor renders in the wrong visual position
during composing. Symptoms differ per platform, but they trace to the
same "composing-region is not authoritative over cursor position"
design gap in the text-input plugins.

- **#122490** (1 reaction, P3) — general statement: cursor should stay in composing region (iOS + Android) · **processed** · **canonical**
- **#108016** (2 reactions, P2) — iOS: floating-cursor in composing region treated as end · **processed**
- **#86471**  (2 reactions, P2) — iOS: insert/delete mid-pinyin doesn't land at caret · **processed**

Shared follow-up: iOS text-input plugin needs composing-region-aware
cursor logic (possibly requiring a secret UITextInput method per the
#108016 radar). Android side needs separate investigation.

### Cluster CSR-1: Composing state not reset on disruptive event (tentative, shared theme)

Active composing state leaks across disruptive events that should
reset it — programmatic text replacement, cursor move during composing,
focus change, IME commit (!), window blur. Distinct triggers and
platforms, all traceable to the same "platform plugin doesn't emit a
composing-range reset signal when it should" gap.

- **#128315** (1 reaction, P2) — iOS: programmatic `.text` + `.selection` replacement during composing → Japanese suggestion auto-fills · **processed**
- **#126263** (0 reactions, P2, regression) — Windows: cursor move during Microsoft Japanese IME composing → next input duplicates preceded text · **processed**
- **#171068** (0 reactions, P2) — iOS: focus change during Pinyin composing leaves U+2006 invisible chars in first field · **processed**
- **#174159** (0 reactions, P2) — Web/iOS: composing range stays set at (0,2) after Pinyin commit (should reset to -1,-1) · **processed**
- **#183078** (0 reactions, P2) — Web Korean: window blur during composing → assertion failure on subsequent backspace · **processed**

All five share: disruptive event (replace/move/focus/commit/blur) →
plugin should send a composing-range reset → doesn't. Different
plugins (iOS, Windows, Web) need coordinated fixes; conceptual
contract is shared: "the platform text-input plugin must emit a
composing-range reset when the compose session is interrupted."

### Cluster AIR-1: Android IME restart on composing-region change (tentative, shared-root-cause)

Android text input plugin calls `InputMethodManager.restartInput`
whenever the framework mutates the composing region. Framework-side
`InputFormatter`s (single-line newline stripping,
`FilteringTextInputFormatter`) mutate the composing region; each
mutation triggers an IME restart, which breaks long-press-delete,
breaks certain non-English IMEs, and changes IME lifecycle
(`onStartInput` called on every space). Native Android editors don't
apply such formatters so don't exhibit the pattern. Fix: suppress
restart when composing change originated from the framework, not from
the IME.

- **#97775** (1 reaction, P2) — IME deltas trigger restarts during held-backspace delete · **processed** · **canonical**
- **#95410** (0 reactions, P2) — `onStartInput` called on every space (single-line formatter trigger) · **processed**
- **#96092** (0 reactions, P2) — Fujitsu Super-ATOK fails; removing `FilteringTextInputFormatter` fixes it · **processed**
- **Possibly related** (not yet processed): #139143 — non-English keyboard + `enableSuggestions: false`

### Cluster IHK-1: iOS hardware-keyboard IME candidate navigation (tentative, tight duplicates)

Hardware-keyboard arrow/tab keys are consumed by Flutter's key handling
and don't reach the iOS IME candidate window's selection logic. Users
can't navigate Chinese IME candidates with the keyboard on iOS/iPadOS
with external keyboards. Fix is in the iOS text input plugin.

- **#110647** (2 reactions, P2) — iPadOS/iOS, Chinese IME, external keyboard arrow keys don't control candidate list · **processed** · **canonical**
- **#135406** (1 reaction, P2) — iOS hardware keyboard (Magic Keyboard / Bluetooth), Chinese IME, arrow & tab keys ignored · **processed**
- **#115903** (0 reactions, P2) — iPadOS physical keyboard, Japanese IME, Tab key moves focus instead of cycling candidates · **processed**

### Cluster DKD-1: Desktop dead-key composition (tentative, shared-root-cause)

Desktop dead-key handling is broken in two complementary ways across
Windows / Linux / macOS with French (and similar) layouts: on Windows
the dead key produces a character on first keystroke when it
shouldn't; on Linux/macOS the second keystroke produces the wrong
character (`e` instead of composed `ê`). Fix lives in desktop
embedders' key-event state machines + framework-side character
derivation. Sibling of DK-1 (mobile) but different fix path
(embedder key-state, not `CharacterCombiner`).

- **#154055** (0 reactions, P2) — Windows: dead key `[` generates `^` on first keystroke (shouldn't); also summarizes the Linux/macOS variant · **processed** · **canonical**
- **#154160** (0 reactions, P2) — Linux/macOS: dead-key sequence `[` + `e` → KeyDownEvent.character is `e` instead of `ê` · **processed**

### Cluster DK-1: Dead-key composition on mobile with external/physical keyboards (tentative, shared-root-cause)

Likely same root cause: embedder does not combine dead-key + letter events
into one composed character on iOS/Android. Windows has this fix.

- **Canonical:** #59541 (oldest, 15 reactions, most detailed history) · **processed**
- **Confirmed member:** #146486 (iOS umlauts, physical keyboard) · **processed** — pinpointed to `[FlutterTextInputView insertText:]` not replacing composing range from `setMarkedText:selectedRange:`
- **Confirmed member:** #87257 (iPad Pro 12.9" soft keyboard, French/Spanish dead keys) · **processed** — same symptom on iPad soft keyboards with dedicated dead-key glyph buttons
- **Confirmed member:** #156184 (iPad iOS 17.5+18 Portuguese, `´`+a → `´á`) · **processed** — same DK-1 symptom (dead-key + letter → composed char plus leftover glyph) with Portuguese layout
- **Not members (processed):** #103136 (Samsung accents with visiblePassword — different mechanism: no input at all rather than 2 chars), #154055/#154160 (desktop dead-key handling — moved to DKD-1), #156183 (iPad iOS 17.5 simulator bug, native Reminders reproduces → Apple-side, not Flutter)

To confirm the cluster, each candidate should be read in full before any
merge action on GitHub.



_None identified yet._

## Likely-stale candidates for closure review

Issues where we suspect the bug is no longer valid. Each entry notes the
basis (test-based vs signal-based) and whether real-device verification is
recommended before action on GitHub.

- **#145887** — Korean input on Android adding spaces between characters.
  **Basis:** signal-based — summary explicitly states "After the Gboard
  update this is not reproducible via the original code; the issue only
  manifests with the misuse pattern." The fix was upstream (Gboard), not
  Flutter. **Verification:** recommended on current Gboard with the
  original reproducer before closing; if confirmed non-reproducing, close
  with a note pointing at the misuse pattern.
- **#156183** — iPad Portuguese keyboard `´`+a deletes char (iOS 17.5
  simulator). **Basis:** signal-based, two independent signals — (a)
  iOS 18 fixes it, (b) bug reproduces in native iOS 17.5 Reminders app
  (not Flutter-specific). **Verification:** none needed within Flutter;
  this is an Apple-side iOS 17.5 simulator bug. Close with a note
  pointing at the iOS-18 resolution.

## Cross-category sibling / split-issue links

Issues whose root cause is also represented in another taxonomy category —
important because per-category dedup scans miss these.

- **#98720 (IME/CJK)** ↔ **#184744 (Hardware keyboard, key events, and
  shortcuts)** — same embedder-level root cause in
  `KeyEmbedderResponder.java` (synthesized ShiftRight down without matching
  up). #184744 was filed by @gnprice as an explicit split for the Gboard
  variant; #98720 keeps the Samsung Keyboard history. Any fix lands in one
  place and should cover both.

## Skipped — engine-level

_None identified yet._
