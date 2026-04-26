# Hardware Keyboard Cleanup Report

Iterative cleanup audit for the **Hardware keyboard, key events, and
shortcuts** category (99 open issues as of the `text_input_issues.json`
snapshot).

Format and workflow specified in
[`../CLEANUP_REPORT_FORMAT.md`](../CLEANUP_REPORT_FORMAT.md). Processed
**one issue at a time** in batches of 10; order is reactions-descending
within the category. Per-issue entries record decision, reasoning, dedup
scan, and (when applicable) the authored regression test and its outcome.

**Priors from IME/CJK (relevant to this category):**
- **#184744** (this category) is the cross-category sibling of #98720
  (IME/CJK) — same embedder-level root cause in `KeyEmbedderResponder.java`
  (synthesized ShiftRight down without matching up). Already logged in
  IME/CJK's cross-category links section; revisit when reached here.
- Potential shared-surface clusters with IME/CJK: **DK-1** (mobile
  dead-key composition) and **DKD-1** (desktop dead-key composition)
  involve key-event state-machine issues that may also manifest here;
  watch for overlap.

## Running summary — **CATEGORY COMPLETE**

- **Processed: 99 / 99** ✅
- Tests written: 2 (retained as framework-level gates)
  - Failed as expected (confirms issue is real): 2
    - #163475 MenuAnchor arrow-key consumption (`_RawMenuAnchorState` Shortcuts widget)
    - #150338 readOnly TextFormField onFieldSubmitted on desktop (`_shouldCreateInputConnection`)
- Skipped — feature/proposal: 14
- Skipped — engine-level: 69
- Skipped — needs native-platform verification: 0
- Likely-duplicate: 2 (#106475 → #107972 [WKR-1/PKC-1]; #100042 → #96660 [iOS hold-key repeat])
- Likely-stale candidates (no test, signal-based): 4 (#90207 webview hybrid-composition default; #72816 emulator-only; #155081 unmaintained GLFW embedder; #155089 upstream Chromium/macOS browser bug)
- Duplicate clusters (tentative): **3** — PKC-1, NKI-1, WKR-1 (sub-cluster inside PKC-1)
- Cross-category sibling/split-issue links: 1 (#184744 ↔ #98720)

### Coverage summary
- 3 tentative clusters cover **12 of 99 issues** (~12%). Lower cluster density than IME/CJK (37%) — Hardware keyboard has more one-off platform-specific bugs rather than broad shared-root-cause families.
- 2 regression tests authored; both fail as expected on framework-diagnosed bugs with clear fix paths:
  - `_RawMenuAnchorState` should only register arrow shortcuts when menu is open
  - `_shouldCreateInputConnection` should not gate `onFieldSubmitted` on `readOnly` for desktop
- 14 skip-proposal — much higher proposal rate than IME/CJK (~9%). Hardware keyboard is a feature-request-heavy category (layout-agnostic shortcuts, stateful activators, native-parity default shortcuts, test simulator completeness, Insert/overtype mode, gamepad, CommandOrControl activator, IME toolbar shortcuts).
- 4 likely-stale candidates — two upstream-ecosystem resolutions (webview_flutter default, Chromium bug), one unmaintained platform (GLFW embedder), one emulator-only behavior. Real-device verification is the shared follow-up.
- 69 skip-engine — the category is deeply embedder-specific. Recurring themes: PKC-1 (pressed-keys state corruption from synthesis bugs), NKI-1 (non-keyboard input device mis-mapping), layout-mapping gaps (non-US / Dvorak / Neo2 / AltGr variants), iOS-hardware-key-repeat missing, media-key forwarding.

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

### #9383 — Support keyboard events in flutter_driver

- **URL:** https://github.com/flutter/flutter/issues/9383
- **Created:** 2017-04-13 (~9.0 y old) · **Updated:** 2025-06-30
- **Reactions:** 53 (👍 38, ❤️ 15)
- **Labels:** `a: tests`, `a: text input`, `tool`, `t: flutter driver`, `customer: crowd`, `c: proposal`, `P3`, `team-tool`, `triaged-tool`, `tool-still-valid`
- **Ownership:** `team-tool`
- **Decision:** **skip — feature/proposal**

**Scope.** Request for a Flutter Driver API to send keyboard events to
devices in integration tests. Useful for comprehensive text-input /
physical-keyboard / IME-compose testing. Original flutter_driver API
was never implemented; comments suggest using `integration_test` +
`tester.testTextInput.receiveAction` as a partial replacement. A
commenter notes `tester.sendKeyEvent` in integration tests also doesn't
reliably inject text on device.

**Why skip.** `c: proposal`, test-infrastructure. Thematic relative of
#102101 "Add integration tests for IME input" and #24955 "Ability to
Integration Test Marked Text" in IME/CJK — test-infrastructure gaps
that would make cross-category attackability much better if closed.

---

### #107972 — A KeyRepeatEvent is dispatched, but the state shows the physical key is not pressed

- **URL:** https://github.com/flutter/flutter/issues/107972
- **Created:** 2022-07-19 (~3.8 y old) · **Updated:** 2024-10-14
- **Reactions:** 32 (👍 32)
- **Labels:** `a: text input`, `framework`, `platform-windows`, `customer: crowd`, `a: desktop`, `a: error message`, `P2`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **skip — engine-level** (forms new cluster **WKR-1**)

**Root cause (per summary).** On Windows, holding a modifier key (Ctrl,
Shift, Alt, Caps Lock) and then moving the mouse or clicking causes
the engine to send a synthesized `KeyUpEvent` followed by a
`KeyRepeatEvent` — but the framework's `_pressedKeys` map no longer
contains the key, triggering the `_assertEventIsRegular` assertion in
`hardware_keyboard.dart:535`. Fixed in engine PR #36129 (Flutter
3.4.0-34.1.pre / 3.5.0 master) but comments in 3.7.0 and 3.19.5/3.19.6
indicate regressions. Debug-only; release strips the assertion.

**Why engine-level.** Fix path is the Windows embedder's key-event
synthesis order — it should not emit a `KeyUpEvent` before a
`KeyRepeatEvent` for a held modifier. Framework-side tolerance of the
wrong sequence would be a workaround, not a fix. Test harness note:
`tester.sendKey*Event` calls go through the framework's
`HardwareKeyboard`; a test reproducing the synthesized-up-then-repeat
sequence would fire the same assertion, so the behavior is
framework-observable even though the fix is embedder-side.

**Cluster.** New tentative cluster **WKR-1** (Windows synthesized
key-event ordering) with #106475 as confirmed member (below).

---

### #67915 — KeyboardListener buggy after focusing a TextField (Chromebook)

- **URL:** https://github.com/flutter/flutter/issues/67915
- **Created:** 2020-10-12 (~5.5 y old) · **Updated:** 2025-03-10
- **Reactions:** 25 (👍 25)
- **Labels:** `a: text input`, `framework`, `engine`, `f: material design`, `platform-chromebook`, `has reproducible steps`, `P2`, `team-framework`, `triaged-framework`, `found in release: 3.19/3.20`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Chromebook / Android + physical keyboard
+ focused TextField: hardware key events don't reach `KeyboardListener`;
the soft keyboard also pops up on every hardware keypress. Engine PR
#22340 partially restored `RawKeyEvent` delivery; soft-keyboard-pop
persists. Switching away from Gboard eliminates the soft-keyboard
pop-up, implicating Gboard's handling of hardware keypresses.

**Why engine-level.** Android embedder's handling of hardware key
events vs. soft-keyboard visibility is where the soft-keyboard-pop
behavior lives. Framework's `KeyboardListener` only receives what the
embedder forwards.

**Dedup scan.** Related to AIR-1 (Android IME restart on composing-
region change, from IME/CJK) — both involve Gboard + Android embedder
doing the wrong thing on keyboard events. Different symptom (soft-
keyboard-pop vs IME restart), same "Android embedder forwards
Gboard-specific behavior" family. Not a tight duplicate; loose cousin.

---

### #30725 — Add desktop shell support for text navigation key combinations

- **URL:** https://github.com/flutter/flutter/issues/30725
- **Created:** 2019-04-08 (~7.0 y old) · **Updated:** 2024-06-27
- **Reactions:** 12 (👍 12)
- **Labels:** `c: new feature`, `engine`, `platform-macos`, `platform-windows`, `platform-linux`, `c: proposal`, `a: desktop`, `e: glfw`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Scope.** On macOS, typing `cmd+right` should invoke
`moveToRightEndOfLine:` via `doCommandBySelector:`. Three architectural
approaches discussed: (1) let `NSKeybindingManager` map keys to intents
and send to framework, (2) track key sequences that trigger
`doCommandBySelector:`, (3) preprocess key events before
`NSTextInputContext`. Approach 1 favored. Blocks IME accent-menu
support (#78061) and iPad physical keyboard. Framework-side shortcuts
via `Shortcuts` work for common combos but don't respect user-
customized macOS key bindings.

**Why skip.** `c: new feature` / `c: proposal`. Architectural design
discussion with no PR. API-surface design outside cleanup scope.

---

### #106475 — [Windows] Keyboard shortcuts stop working after modifier key repeat

- **URL:** https://github.com/flutter/flutter/issues/106475
- **Created:** 2022-06-23 (~3.8 y old) · **Updated:** 2023-07-08
- **Reactions:** 12 (👍 11, 👀 1)
- **Labels:** `a: text input`, `framework`, `platform-windows`, `P2`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **likely-duplicate of #107972** (WKR-1 cluster)

**Root cause (per summary).** Windows: holding a modifier long enough
to generate repeat events. Engine sends synthesized key-up before
key-repeat (Windows IME interaction); framework receives key-repeat
for a key it believes not pressed; hits the `_pressedKeys.containsKey`
assertion in `HardwareKeyboard._assertEventIsRegular`. After the
assertion fires in debug mode, `_keyEventsSinceLastMessage` is not
cleared, permanently breaking subsequent shortcut handling until app
restart. Debug-only.

**Why duplicate.** Exact same root cause as #107972 — engine's
synthesized-up-before-repeat ordering, same `_assertEventIsRegular`
assertion, same `hardware_keyboard.dart` line. #107972 is the more
general framing (more reactions, files the assertion text directly
as the title); #106475 is the user-visible consequence (shortcuts
stop working after the assertion leaves state broken).

**Cluster.** **WKR-1** — confirmed member.

---

### #93915 — [Proposal] Add option to enable/disable the TextInputAction

- **URL:** https://github.com/flutter/flutter/issues/93915
- **Created:** 2021-11-19 (~4.4 y old) · **Updated:** 2024-03-06
- **Reactions:** 10 (👍 10)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `c: proposal`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal**

**Scope.** Request for iOS-style `enablesReturnKeyAutomatically`
behavior — the return key auto-enables when the field is non-empty.

**Why skip.** `c: proposal` / `c: new feature`. API-surface
addition.

---

### #90207 — [Android 12][Keyboard] Display ID mismatch with webview

- **URL:** https://github.com/flutter/flutter/issues/90207
- **Created:** 2021-09-16 (~4.6 y old) · **Updated:** 2024-03-06
- **Reactions:** 9 (👍 9)
- **Labels:** `a: text input`, `platform-android`, `engine`, `a: platform-views`, `e: OS-version specific`, `has reproducible steps`, `P2`, `platform-views: vd`, `found in release: 2.2/2.6`, `team-android`, `triaged-android`
- **Ownership:** `team-android`
- **Decision:** **likely-stale (signal-based)**

**Root cause (per summary).** Android 12+ Virtual Display-based
platform views use a `DisplayId` that doesn't match
`InputMethodManager`'s display, causing keyboard failures. Switching
to Hybrid Composition (`useHybridComposition: true` or
`SurfaceAndroidWebView`) resolves it. **For `webview_flutter >=
3.0.0`, hybrid composition is the default.**

**Why likely-stale.** The ecosystem upstream change (webview_flutter
defaulting to hybrid composition from 3.0.0, now at 4.x+) effectively
resolves the user-facing pain. The core engine VD-DisplayId issue
still exists but users rarely encounter it outside explicit legacy
VD usage. **Recommendation:** close with a pointer to hybrid
composition as the default resolution and note the VD-DisplayId gap
remains as a low-priority engine concern if anyone revives VD for
specific cases. Real-device verification on current webview_flutter
+ Android 12+ would confirm before closing.

---

### #100456 — [Keyboard] Analyze keyboard layout and enforce mandatory logical keys

- **URL:** https://github.com/flutter/flutter/issues/100456
- **Created:** 2022-03-21 (~4.1 y old) · **Updated:** 2024-08-21
- **Reactions:** 9 (👍 9)
- **Labels:** `a: text input`, `platform-macos`, `platform-web`, `platform-linux`, `a: desktop`, `P2`, `team-text-input`, `fyi-windows`, `fyi-linux`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause (per body + summary).** Algorithm for deriving logical
keys on Web/macOS/Linux produces non-intuitive results on non-US
layouts: Shift-Digit keys broken (Shift+Digit1 → exclamation on US),
French layout Digit1 → ampersand, Russian layout keyA → ф. Body
describes the fix as "completed on macOS, GTK, Web, Android"; iOS
remaining. No comments beyond a bot label.

**Why engine-level.** Fix is in each platform's key-event translation
layer (iOS text input plugin remaining). The completed work landed
engine-side across macOS/GTK/Web/Android. The iOS-remaining work is
the same engine-side pattern.

**Partial-fix note.** Status is "mostly done" — iOS plugin is the
only remaining gap. Worth verifying that macOS/Web/Linux are indeed
at the "new logical keys" behavior (from the body's target table).

---

### #166683 — iOS Full Keyboard Access breaks external keyboard navigation

- **URL:** https://github.com/flutter/flutter/issues/166683
- **Created:** 2025-04-07 (~1.1 y old) · **Updated:** 2026-04-16
- **Reactions:** 9 (👍 9)
- **Labels:** `a: text input`, `e: device-specific`, `platform-ios`, `framework`, `a: accessibility`, `P2`, `team-ios`, `triaged-ios`, `fyi-text-input`
- **Ownership:** `team-ios`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** iOS Full Keyboard Access (FKA)
accessibility setting + external keyboard: Flutter apps become
unresponsive to keyboard input. Device-specific — reproduces on
iPhone 12 Pro Max iOS 18.4 and iOS 17 simulator, not on iOS 18
simulators or some physical devices (>=90% of fleet per a commenter).
Additional sub-issues: `onFocusChange` and
`Semantics.onDidGainAccessibilityFocus` never called when tabbing
with FKA (only on Space-key press); sliders not focusable via FKA.

**Why engine-level.** FKA integration lives in the iOS text input /
semantics plugin. Framework's `Semantics` and focus system only see
what the plugin signals.

**Dedup scan.** Thematic cousin of #110647 / #135406 / #115903 (IHK-1:
iOS hardware-keyboard IME candidate navigation) — shared theme "iOS
hardware keyboard accessibility/navigation falls through Flutter's
key-event system." Different trigger (FKA accessibility setting) and
different mechanism (semantics events); not IHK-1 member.

---

### #96660 — [iOS] Holding Backspace on hardware keyboard doesn't keep deleting

- **URL:** https://github.com/flutter/flutter/issues/96660
- **Created:** 2022-01-14 (~4.3 y old) · **Updated:** 2024-03-06
- **Reactions:** 8 (👍 5, 👀 3)
- **Labels:** `a: text input`, `platform-ios`, `framework`, `has reproducible steps`, `P2`, `found in release: 2.8/2.9/2.10`, `team-ios`, `triaged-ios`
- **Ownership:** `team-ios`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** iOS simulator + hardware keyboard:
holding Backspace only deletes one character; applies to Backspace,
Delete, and arrow keys — any hardware keyboard key doesn't repeat.
Regression from Flutter 2.0.1 working to 2.8.1 broken. Also
reproduces on physical iPad/iPhone with external keyboard.

**Why engine-level.** Key-repeat dispatching from the iOS plugin
to the framework broke somewhere between 2.0.1 and 2.8.1. The iOS
plugin needs to forward key-repeat events the same way other
platforms do. Framework-side `HardwareKeyboard` handles repeat
events if received; the iOS plugin isn't sending them for held keys.

**Status note.** Regression without a clear mitigation — 4 years
stalled. High-impact UX issue (can't bulk-delete with held
Backspace on iOS). Worth flagging to the iOS roadmap.

---

### #97506 — Option to drag cursor handle continuously (Samsung native default)

- **URL:** https://github.com/flutter/flutter/issues/97506
- **Created:** 2022-01-30 (~4.2 y old) · **Updated:** 2025-01-20
- **Reactions:** 7 (👍 7)
- **Labels:** `a: text input`, `c: new feature`, `platform-android`, `platform-ios`, `framework`, `f: material design`, `a: fidelity`, `c: proposal`, `P3`, `e: samsung`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Scope.** Proposal for `cursorBehavior` API (e.g.,
`JumpingCursorBehavior`, `GoThroughCursorBehavior`,
`CupertinoCursorBehavior`) to match Samsung's continuous cursor-drag
behavior. Samsung-device-specific (A32, M22 on One UI 3.1).

**Why skip.** `c: proposal` / `c: new feature`.

---

### #35347 — [Web] RawKeyboardListener does not return correct data

- **URL:** https://github.com/flutter/flutter/issues/35347
- **Created:** 2019-06-29 (~6.8 y old) · **Updated:** 2024-03-06
- **Reactions:** 5 (👍 5)
- **Labels:** `a: text input`, `c: contributor-productivity`, `framework`, `platform-web`, `P2`, `c: tech-debt`, `team: skip-test`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level** (web engine)

**Root cause (per summary).** Web: `RawKeyboardListener.onKey`
receives `logicalKey` values that don't match the pressed key
(e.g., 'A' produces "Digit 9" or "Launch Mail"). Fails in release
web builds. Skipped tests in `raw_keyboard_test.dart` and
`focus_traversal_test.dart` track this.

**Why engine-level.** Web engine's DOM keyboard-event translation
to Flutter logical keys. Framework `RawKeyboardListener` receives
whatever the engine mapped. Companion to #100456 (analyze keyboard
layout / enforce mandatory logical keys), though that issue addresses
non-US layouts while this one fails even on default US.

---

### #90368 — [web] Option key shortcuts broken on macOS

- **URL:** https://github.com/flutter/flutter/issues/90368
- **Created:** 2021-09-20 (~4.6 y old) · **Updated:** 2024-03-06
- **Reactions:** 4 (👍 4)
- **Labels:** `a: text input`, `framework`, `platform-web`, `has reproducible steps`, `browser: safari-macos`, `P2`, `found in release: 2.5/2.6`, `browser: chrome-desktop`, `customer: troy`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level** (web engine on macOS)

**Root cause (per summary).** Flutter web on macOS (Chrome + Safari):
Option/Alt-based `ShortcutActivator` / `SingleActivator` doesn't
trigger. Windows web and macOS desktop work correctly. Workaround:
`CharacterActivator('å', alt: true)` — works if the layout produces
a modified character for the key.

**Why engine-level.** Web engine's macOS-specific Option-key event
translation drops the alt modifier flag for shortcut matching.
Framework activators consume what the engine forwards.

---

### #99848 — [Desktop] Multimedia key events not reported to HardwareKeyboard

- **URL:** https://github.com/flutter/flutter/issues/99848
- **Created:** 2022-03-09 (~4.1 y old) · **Updated:** 2024-08-05
- **Reactions:** 4 (👍 4)
- **Labels:** `a: text input`, `platform-macos`, `a: desktop`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause (per body + summary).** macOS + web: pressing
multimedia keys (Play/Pause, Forward, Backward) — same physical
keys as F-keys under FN-toggle — produces no events in
`HardwareKeyboard`. F-keys and regular keys work. Spotify and other
media-player apps receive these events; Flutter currently can't.

**Why engine-level.** macOS and web platform embedders don't
register for system-level media-key events. The fix is registering
for those events in each embedder and forwarding them via the
usual HardwareKeyboard path.

---

### #105914 — Support gamepad on Web

- **URL:** https://github.com/flutter/flutter/issues/105914
- **Created:** 2022-06-13 (~3.9 y old) · **Updated:** 2025-02-10
- **Reactions:** 4 (👍 4)
- **Labels:** `a: text input`, `platform-web`, `P2`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — feature/proposal**

**Scope.** Body: "Gamepad on Web uses the special gamepad API. We
should support it. Also, Web supports multiple gamepads. Is keyboard
the best way to support them?" New-capability proposal; no
specific bug behavior.

**Why skip.** New feature request even without explicit `c: new
feature` label. Out of cleanup scope.

---

### #163475 — TextField surrounded by MenuAnchor does not respond to arrow keys

- **URL:** https://github.com/flutter/flutter/issues/163475
- **Created:** 2025-02-17 (~1.2 y old) · **Updated:** 2025-02-27
- **Reactions:** 4 (👍 4)
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.29/3.30`
- **Ownership:** `team-text-input`
- **Decision:** **write-test** → **fail-as-expected** (confirms bug is real and framework-observable)

**Root cause (per summary).** `_RawMenuAnchorState`'s internal
`Shortcuts` widget unconditionally registers arrow-key shortcuts
that consume events before the wrapped TextField can process them.
Proposed fix: only register those shortcuts when the menu is
actually open.

**Test approach.** `testWidgets` places a TextField inside a
`MenuAnchor` with empty `menuChildren` (menu closed by default),
focuses the field, puts the caret at the end of 'abcdef' (offset
6), and sends `LogicalKeyboardKey.arrowLeft`. Asserts the caret
moves to offset 5.

**Test:** [`issue_163475_textfield_in_menuanchor_ignores_arrow_keys_test.dart`](../regression_tests/hardware_keyboard/issue_163475_textfield_in_menuanchor_ignores_arrow_keys_test.dart)

**Test outcome.** Fails as expected: `Actual: <6>` vs `Expected:
<5>`. The caret stays at end-of-text — the left-arrow event is
consumed by MenuAnchor's unconditional arrow Shortcuts, never
reaching the TextField. Confirms the bug is real, framework-level,
and testable without real-device IME behavior.

**Dedup scan.** Similar in shape to other "framework-widget consumes
keys that should reach TextField" cases but specifically scoped to
MenuAnchor. No tight duplicates in Hardware keyboard.

---

### #78220 — [chromeOS] TextField backspace doesn't work + Japanese select

- **URL:** https://github.com/flutter/flutter/issues/78220
- **Created:** 2021-03-15 (~5.1 y old) · **Updated:** 2024-06-27
- **Reactions:** 3 (👍 3)
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `platform-chromebook`, `a: typography`, `a: desktop`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Chromebook + Japanese input: Backspace doesn't work
after confirming text; text selection also broken with Japanese
input. Triager lacks the device; no diagnostic progress beyond
linking to #78221. Stalled.

**Why engine-level.** Chromebook is Android-on-ChromeOS; fix path is
the Android embedder's handling of Japanese IME + Backspace key
events on the Chromebook variant. Thematic cousin of #67915
(Chromebook + KeyboardListener) processed in batch 1.

---

### #94965 — [Proposal][Desktop] Let ESC key de-select currently selected item

- **URL:** https://github.com/flutter/flutter/issues/94965
- **Created:** 2021-12-09 (~4.4 y old) · **Updated:** 2024-06-27
- **Reactions:** 3 (👍 3)
- **Labels:** `a: text input`, `c: new feature`, `f: material design`, `c: proposal`, `a: desktop`, `a: error message`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Scope.** Desktop parity request: ESC should deselect selected
text/widgets/tab-focused items, matching other desktop programs.
Related: #98163, #84416. WCAG 2.1 accessibility raised.

**Why skip.** `c: proposal` / `c: new feature`.

---

### #152391 — PDA keyboard Shift key fires `_assertEventIsRegular` assertion

- **URL:** https://github.com/flutter/flutter/issues/152391
- **Created:** 2024-07-26 (~1.7 y old) · **Updated:** 2025-09-02
- **Reactions:** 3 (👍 3)
- **Labels:** `a: text input`, `e: device-specific`, `platform-android`, `engine`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** HT730 PDA keyboard on Android maps
Shift Right's physical key to the Shift Left logical key. When the
subsequent `KeyUpEvent` arrives with the correct Shift Right logical
key, `HardwareKeyboard._assertEventIsRegular` at line 505 fails
(`!_pressedKeys.containsKey(event.physicalKey)`) because the
physical↔logical pairing doesn't match what was recorded on key-down.

**Why engine-level.** Device-specific key remapping at the Android
embedder level. The PDA's InputConnection is non-standard; Flutter's
assertion was correct that the event stream is inconsistent.

**Dedup scan.** Thematic relative of WKR-1 (Windows synthesized
key-event ordering) — both are `_assertEventIsRegular` assertion
failures caused by embedder-forwarded non-standard key-event
sequences. Different platforms (Android PDA vs Windows modifiers)
and different specific causes (physical-to-logical remap vs
synthesized-up-before-repeat); shared "non-standard key-event
stream breaks framework assertion" pattern. Not a tight cluster
member.

---

### #182775 — [BUG][WEB] KeyUpEvent synthesized too eagerly with Meta + multiple non-modifier keys

- **URL:** https://github.com/flutter/flutter/issues/182775
- **Created:** 2026-02-23 (~0.2 y old) · **Updated:** 2026-02-24
- **Reactions:** 3 (👍 3)
- **Labels:** `a: text input`, `engine`, `P2`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level** (Flutter web engine)

**Root cause (per body).** Web embedder's key-guard mechanism
(required when Meta/Cmd is held) misbehaves when multiple
non-modifier keys are pressed alongside Meta. Only the last pressed
non-modifier sends repeat events; after ~1.5s (the
`_kKeydownCancelDurationMac` threshold), the framework incorrectly
synthesizes KeyUp events for the other physically-held non-modifier
keys. Engine PR #180692 fixed the normal-typing / game-control
case (#162305) but left this Meta+multi-key variant unresolved.

**Why engine-level.** Web engine's key-guard synthesis logic is the
fix target. Framework receives the incorrectly-synthesized KeyUp
events as-is.

**Dedup scan.** Thematic cousin of WKR-1 (Windows synthesized
key-event ordering). Same pattern ("engine synthesizes key events
that shouldn't exist") on a different platform (web vs Windows).
Not a tight cluster; different specific trigger and fix location.

---

### #48296 — Inconsistent behavior of RawKeyboardListener on different Android devices

- **URL:** https://github.com/flutter/flutter/issues/48296
- **Created:** 2020-01-07 (~6.3 y old) · **Updated:** 2024-03-06
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `platform-android`, `framework`, `engine`, `P2`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Samsung Android devices (S9, Android 9)
don't produce media-key events from a Bluetooth keyboard until an
`InputConnection` is opened (triggered by TextField focus). Pixel
devices always produce the events. Suggested to switch from deprecated
`RawKeyboardListener` to `KeyboardListener`; unlikely to fix the
underlying issue.

**Why engine-level.** Android embedder / Samsung-device-specific
behavior around when media keys are forwarded. Sibling of #99848
(desktop multimedia keys) but on mobile. Stalled without a Samsung
device for debugging.

---

### #72816 — RawKeyboard listener holding key on Android emulator (emulator behavior)

- **URL:** https://github.com/flutter/flutter/issues/72816
- **Created:** 2020-12-22 (~5.3 y old) · **Updated:** 2026-03-07
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `platform-android`, `engine`, `d: api docs`, `has reproducible steps`, `P2`, `found in release: 3.3/3.7`, `team-android`, `triaged-android`
- **Ownership:** `team-android`
- **Decision:** **likely-stale (signal-based)**

**Root cause (per summary).** Android emulator's `dispatchKeyEvent`
in `FlutterView` emits paired down/up events on held keys. **This
is Android emulator behavior — on real devices with a physical
Bluetooth keyboard, key-repeat down events fire correctly and up
fires only on release. The issue is emulator-specific, not a
Flutter bug.** A separate web-specific variant was filed at #182775
(processed batch 2).

**Why likely-stale.** Explicit statement that this is emulator
behavior, not a Flutter bug. **Recommendation:** close as
working-as-expected on real devices; the emulator-specific
divergence is upstream Android emulator behavior and out of
Flutter's scope.

---

### #73544 — TextField not working after backspace when using Frozen Keyboard

- **URL:** https://github.com/flutter/flutter/issues/73544
- **Created:** 2021-01-08 (~5.3 y old) · **Updated:** 2024-03-06
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `platform-android`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 3.3/3.7`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Frozen Keyboard (Android) fails to call
`endBatchEdit()` after dispatching a backspace keydown inside a batch
edit, leaving `InputConnectionAdaptor` in a broken state. Traced by
@justinmc. Engine PR #24500 linked as potential fix. Specific to
Frozen Keyboard's non-standard IME behavior. Workaround: disable the
Unicode switch in Frozen Keyboard settings.

**Why engine-level.** Fix is either in Android InputConnectionAdaptor
(detect and recover from unclosed batch edits) or upstream in Frozen
Keyboard. Framework gets the broken state forwarded through the
InputConnection path.

**Dedup scan.** Family pattern "Android embedder forwards non-standard
IME behavior": AIR-1 cluster (Android IME restart on composing-region
change), #98720/#184744 (Samsung/Gboard shift-stuck), #120351 (Samsung
batch-edit ordering), #81314 (Gboard off-by-one), etc. Frozen Keyboard
variant is yet another member of this "Android embedder should defend
against non-standard IME sequencing" family. Not a tight cluster.

---

### #116658 — Make shortcuts portable across different keyboard layouts

- **URL:** https://github.com/flutter/flutter/issues/116658
- **Created:** 2022-12-07 (~3.4 y old) · **Updated:** 2023-07-08
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `c: new feature`, `engine`, `c: proposal`, `P3`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — feature/proposal**

**Scope.** `SingleActivator` is not keyboard-layout-agnostic (Ctrl+`+`
works on Finnish but needs Ctrl+Shift+`+` on US English). Existing
`CharacterActivator` covers the layout-agnostic case per
@gspencergoog. Issue labeled as proposal; no framework change planned.

**Why skip.** `c: proposal` / `c: new feature`.

---

### #119088 — SingleActivator doesn't recognize shortcuts with some alt+key combinations

- **URL:** https://github.com/flutter/flutter/issues/119088
- **Created:** 2023-01-24 (~3.3 y old) · **Updated:** 2024-03-06
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `engine`, `c: proposal`, `P3`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — feature/proposal**

**Scope.** `SingleActivator(LogicalKeyboardKey.keyG, meta: true,
alt: true)` fails because `alt+G` produces `©` and `SingleActivator`
uses `RawKeyEvent`. `CharacterActivator('©', meta: true, alt: true)`
works as a workaround but loses the "actual G key" intent. Proposal:
a new activator using `KeyEvent` (layout-agnostic).

**Why skip.** `c: proposal`. Thematic sibling of #116658 (layout-
portable shortcuts); both about the same `SingleActivator` /
`CharacterActivator` limitations under modifiers that transform the
character.

---

### #142820 — Hardware keyboard handlers invoked when TextField keyboardType is number/phone

- **URL:** https://github.com/flutter/flutter/issues/142820
- **Created:** 2024-02-02 (~2.2 y old) · **Updated:** 2025-06-27
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `framework`, `engine`, `has reproducible steps`, `P3`, `team-design`, `triaged-design`, `found in release: 3.16/3.20`
- **Ownership:** `team-design`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Android software keyboards for numeric /
phone / other number-forward `TextInputType`s send simulated hardware
key events (unlike text-forward types). This causes `HardwareKeyboard`
listeners to fire on digit presses — and, if they return `true`, the
input never reaches the TextField. Reproduced with Gboard and AOSP on
Android 9–13. **Team resolution: document the inconsistency; no
framework fix planned.**

**Why engine-level.** Keyboard-app-dependent behavior outside Flutter's
direct control; the Android embedder faithfully forwards what each
IME emits. Framework could theoretically compensate but the team chose
documentation as the appropriate response.

---

### #184744 — [Android] Tapping Shift gets stuck into change-selection state

- **URL:** https://github.com/flutter/flutter/issues/184744
- **Created:** 2026-04-08 (~0.0 y old) · **Updated:** 2026-04-14
- **Reactions:** 2 (👍 2)
- **Labels:** `a: text input`, `c: regression`, `platform-android`, `has reproducible steps`, `P1`, `f: selection`, `team-android`, `triaged-android`
- **Ownership:** `team-android`
- **Decision:** **skip — engine-level** (cross-category sibling of #98720, pre-logged)

**Root cause (per summary).** Filed as an explicit split by @gnprice
from #98720 (IME/CJK cleanup). Same root cause:
`KeyEmbedderResponder.java` synthesizes a ShiftRight key-down in
response to Gboard's shift-tap on-screen key but doesn't synthesize
the matching key-up. Framework then treats subsequent taps as shift-
extend-selection. `P1 c: regression` — highest-severity tag in this
whole audit.

**Why engine-level.** Pinpointed to `KeyEmbedderResponder.java` on
the Android embedder. Identical to #98720 which we cluster-noted in
IME/CJK. Any fix in `KeyEmbedderResponder.java` closes both issues.

**Cross-category link.** Already logged in this report's
"Cross-category sibling / split-issue links" section (top of file).
Within HW keyboard alone it's a standalone skip-engine; the actual
merge action is with #98720 across the IME/CJK ↔ HW keyboard
boundary.

---

### #65233 — OK/Select on IR Remotes causes `_assertEventIsRegular` exception

- **URL:** https://github.com/flutter/flutter/issues/65233
- **Created:** 2020-09-04 (~5.6 y old) · **Updated:** 2026-01-07
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `c: crash`, `platform-android`, `framework`, `P2`, `team-android`, `triaged-android`, `a: tv`
- **Ownership:** `team-android`
- **Decision:** **skip — engine-level**

**Root cause (per @gspencergoog in summary).** Android TV IR remote
scan codes are translated through the keyboard physical-key mapping,
so scan code 97 (IR OK button) maps to "Control Right". The
assertion in `raw_keyboard.dart:601` fires because the metaState
modifier bit for that "modifier" key isn't set on the event — IR
remote isn't a modifier-capable source.

**Proposed fix (per commenter).** Skip modifier-key synchronization
when the input source is not a keyboard (platform-detectable).
Community patch bypasses modifier sync in `hardware_keyboard.dart`;
another workaround re-dispatches IR OK as `KEYCODE_ENTER` in
`MainActivity.dispatchKeyEvent`.

**Why engine-level.** Fix requires detecting "input source is not
keyboard" — that signal lives in the Android `InputDevice` API and
needs to flow through the embedder to the framework. Framework-only
compensation (always skip modifier sync when metaState=0) would be
fragile. Sibling of WKR-1 / #152391 / #182775 in the "framework
assertion fires because embedder forwards non-keyboard-looking
events" pattern.

**Dedup scan.** Thematic family with #177360 (Android TV software
keyboard arrow navigation broken, from IME/CJK cleanup). Both are
Android TV / Chromecast / TV-remote-category bugs that block Flutter
apps on TV platforms. Different mechanisms but shared platform
strategic concern.

---

### #78421 — [Linux] Keyboard stops working after using some backspacing

- **URL:** https://github.com/flutter/flutter/issues/78421
- **Created:** 2021-03-17 (~5.1 y old) · **Updated:** 2024-06-07
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `e: device-specific`, `engine`, `platform-linux`, `a: desktop`, `P2`, `team-linux`, `triaged-linux`
- **Ownership:** `team-linux`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Linux engine emits a warning
"Event response for event id ... received, but pending event was
not found" whenever keyboard input stops working. Correlated with
slower processors (1.2–1.3 GHz). Intermittent; harder to reproduce
on VMs. A separate commenter reports space key triggering inkwell
effects instead of inserting text.

**Why engine-level.** Linux (GTK) engine's key-event pending-queue
handling races on slower hardware. Framework receives no events.
Fix is Linux embedder race-condition work.

---

### #80108 — LogicalKeyboardKey doesn't always match PhysicalKeyboardKey on Windows

- **URL:** https://github.com/flutter/flutter/issues/80108
- **Created:** 2021-04-09 (~5.0 y old) · **Updated:** 2024-06-07
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `engine`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.0/2.1`, `team-windows`, `triaged-windows`
- **Ownership:** `team-windows`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Barcode scanner on Windows sends
shift+digit sequences; Flutter maps to shifted logical keys (e.g. `!`
for digit 1) on first event, then emits a second event with
"Unknown Windows key code 49" for the same physical key. Results in
mismatched logical/physical keys.

**Why engine-level.** Windows embedder's scan-code handling for
non-keyboard input devices (barcode scanners) — same pattern as
#65233 (IR remote) and #152391 (PDA keyboard): embedder treats
non-keyboard sources as keyboards and derives logical keys from an
inapplicable layout table.

**Dedup scan.** Recurring pattern across #65233 (IR remote, Android),
#152391 (PDA keyboard, Android), #80108 (barcode scanner, Windows):
**non-keyboard input devices emit raw events that Flutter mis-maps to
keyboard logical keys**. Could form a cluster "NKI-1 non-keyboard
input device mis-mapping" — but fix targets differ per platform
(detect non-keyboard source in each embedder). Holding tentative;
revisit if more appear.

---

### #87064 — Default text section shortcuts missing on some platforms

- **URL:** https://github.com/flutter/flutter/issues/87064
- **Created:** 2021-07-26 (~4.7 y old) · **Updated:** 2026-04-12
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `a: quality`, `a: desktop`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Scope.** Checklist of macOS/Windows/Linux default text-navigation
shortcuts not yet implemented in Flutter (macOS Ctrl-L, Ctrl-Backspace,
Windows/Linux Ctrl+T, shift+ctrl+A/E for extend-selection-to-line
boundary, etc.). Per-platform native-parity gaps.

**Why skip.** No `c:` label, but the body is a feature-completeness
roadmap ("we don't currently implement these"). Not a regression;
no single reproducible bug. Each item would be an individual
implementation task.

---

### #93373 — Newline in TextFormField doesn't work on desktop (streetAddress keyboardType)

- **URL:** https://github.com/flutter/flutter/issues/93373
- **Created:** 2021-11-10 (~4.5 y old) · **Updated:** 2025-10-09
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `f: material design`, `platform-macos`, `platform-linux`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.5/2.6`, `team-macos`, `triaged-macos`
- **Ownership:** `team-macos`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** `TextInputType.streetAddress` falls back
to `TextInputType.text` on web/Linux/macOS, which doesn't allow
newlines (only `TextInputType.multiline` does). Confirmed on macOS
desktop, Linux, and web. Related PR #90211 merged but didn't fix.

**Why engine-level.** The keyboardType fallback logic lives in the
platform embedders. Framework passes the requested type through;
the embedders decide how to map unsupported types to supported ones.
Fix would be embedder-side: `streetAddress` with multiple lines
should map to `multiline`, not `text`.

---

### #95630 — hardware_keyboard.dart throws Null check operator used on a null value

- **URL:** https://github.com/flutter/flutter/issues/95630
- **Created:** 2021-12-21 (~4.3 y old) · **Updated:** 2024-03-06
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `c: crash`, `platform-android`, `framework`, `a: error message`, `a: production`, `P2`, `team-android`, `triaged-android`
- **Ownership:** `team-android`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** Production crash from
`KeyEventManager._convertRawEventAndStore` (`hardware_keyboard.dart:902`):
null check operator on null. Reported via Crashlytics from
older Android devices (API 25, 28). No reproducible steps; no specific
device pattern beyond "older Android".

**Why engine-level.** The null value comes from event data that the
Android embedder passes up to the framework. Framework-side defensive
nullability check would stop the crash but wouldn't fix what's
actually wrong with the event. Engine should not be sending null
fields for required data.

**Dedup scan.** Sibling of the WKR-1 / PDA-keyboard / IR-remote
"embedder forwards malformed event data" pattern. Not a tight cluster
member because this is a different failure mode (null field vs
inconsistent sequence).

---

### #95634 — HardwareKeyboard.logicalKeysPressed returns previously pressed keys

- **URL:** https://github.com/flutter/flutter/issues/95634
- **Created:** 2021-12-21 (~4.3 y old) · **Updated:** 2025-03-18
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.8/2.9`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause (per body + summary).** After pressing and releasing
`cmd+k`, then pressing `arrow left`, Flutter's
`HardwareKeyboard.instance.logicalKeysPressed` reports `Arrow Left +
Key K` — the K key leaked into the next event's pressed-keys set.
Reproduces on web Chrome and Windows desktop (with Alt instead of
Meta); not on macOS desktop. Framework-level key-state corruption
stemming from engine-side event ordering under modifier+key
sequences.

**Why engine-level.** The web/Windows embedders don't emit a key-up
for the non-modifier key when it's released while the modifier is
still held — so the framework's `_pressedKeys` keeps recording it.
Fix needs embedder-side key-up emission. A related web issue (#162977)
was linked about triggers not being released on focus loss.

**Dedup scan.** Close to WKR-1 thematic family (Windows synthesized
key-event ordering) and #100455 (next entry, web+macOS Cmd+digit
→ Option+digit assertion). All three are `_pressedKeys` state
corruption from engine-side sequencing bugs. Different triggers,
shared underlying invariant. Holding tentative; could form a
"pressed-keys-state-corruption" cluster if a 4th+ case appears.

---

### #96021 — Test key simulator doesn't work with uppercase characters

- **URL:** https://github.com/flutter/flutter/issues/96021
- **Created:** 2022-01-01 (~4.3 y old) · **Updated:** 2024-06-27
- **Reactions:** 1 (👍 1)
- **Labels:** `a: tests`, `a: text input`, `c: new feature`, `framework`, `a: desktop`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Scope.** `WidgetTester.sendKeyDownEvent` / `sendKeyEvent`
converts all characters to lowercase per a TODO in
`event_simulation.dart`. Request: honor shift state and support
uppercase/shifted characters. Intention was to deprecate old
simulation code once the new KeyEvent-based system was ready.

**Why skip.** `c: new feature`, test-infrastructure completeness.

---

### #96022 — WidgetTester macOS shift+key logical keys throws

- **URL:** https://github.com/flutter/flutter/issues/96022
- **Created:** 2022-01-01 (~4.3 y old) · **Updated:** 2024-06-27
- **Reactions:** 1 (👍 1)
- **Labels:** `a: tests`, `a: text input`, `framework`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.8/2.9`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level** (test infra internal map)

**Root cause (per summary).** `KeyEventSimulator` has no macOS
physical-key mapping for shifted logical keys like `!`, `*`, `(`. The
assertion fires at `event_simulation.dart:243`. Workaround: specify
`physicalKey` explicitly (e.g., `PhysicalKeyboardKey.digit1`) or
simulate Shift+key separately. Broader fix tracked in #100456
(keyboard layout / logical keys analysis).

**Why engine-level.** Fix is in the `flutter_test`
`event_simulation.dart` mapping table — test infrastructure gap
rather than product bug. Not write-test territory; the bug *is* in
the test harness.

---

### #100455 — [web on macOS] KeyUpEvent assertion after Cmd+digit → Option+digit

- **URL:** https://github.com/flutter/flutter/issues/100455
- **Created:** 2022-03-20 (~4.1 y old) · **Updated:** 2024-03-06
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `engine`, `platform-macos`, `platform-web`, `has reproducible steps`, `P2`, `found in release: 2.10/2.13`, `team-web`, `triaged-web`
- **Ownership:** `team-web`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** On web + macOS: `cmd+1` released, then
`option+1` pressed → assertion `_pressedKeys[event.physicalKey] ==
event.logicalKey` fires. Root cause: macOS remaps the logical key
for modifier+digit (cmd+1 produces `¡` for option+1 release); Flutter
records the wrong logical key on key-down and the key-up assertion
fails. Also reported with Korean IME, Windows Emoji picker, and
Apple Magic Keyboard with no special combo. Keyboard gets stuck
after the assertion fires.

**Why engine-level.** Web + macOS key-event translation preserves
macOS's layout-dependent logical-key-under-modifier behavior, which
conflicts with Flutter's `_pressedKeys` invariant. Fix requires the
web engine to either (a) normalize the logical key across modifier
transitions, or (b) weaken the framework invariant.

**Dedup scan.** Sibling of WKR-1 and #95634 — all three are
`_pressedKeys`-state-corruption-from-engine-side-sequencing bugs.
Could form "PKC-1 pressed-keys state corruption" cluster if more
appear.

---

### #105514 — isKeyPressed behaves differently for Korean on RawKeyboardListener

- **URL:** https://github.com/flutter/flutter/issues/105514
- **Created:** 2022-06-07 (~3.9 y old) · **Updated:** 2023-07-08
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `has reproducible steps`, `P2`, `found in release: 3.0/3.1`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause (per summary).** `RawKeyboard` (legacy) maps Korean `ㄷ`
(physical Key E on QWERTY) to a different logical key than `keyE`,
so `isKeyPressed(LogicalKeyboardKey.keyE)` returns `false` for the
Korean input. Maintainer directed users to `HardwareKeyboard` /
`KeyboardListener` + `Shortcuts` / `SingleActivator`. Follow-up test:
even `Shortcuts` + `SingleActivator` don't trigger for the Korean
key — acknowledged as a separate problem to investigate.

**Why engine-level.** Non-US layout logical-key mapping lives in
each platform's engine-side key translation (companion to #100456
and #35347). Sibling of "keyboard layout logical keys don't match
physical keys" family.

---

### #106853 — Support stateful shortcut activators

- **URL:** https://github.com/flutter/flutter/issues/106853
- **Created:** 2022-06-30 (~3.8 y old) · **Updated:** 2023-07-08
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `c: new feature`, `framework`, `c: proposal`, `P3`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Scope.** Proposal for stateful shortcut activators to cover:
long-press a key, tap-shift-with-no-intervening-events, chord
sequences like Ctrl-A Ctrl-D.

**Why skip.** `c: new feature` / `c: proposal`.

---

### #122673 — Insert key doesn't switch overtype/insert modes in TextField

- **URL:** https://github.com/flutter/flutter/issues/122673
- **Created:** 2023-03-15 (~3.1 y old) · **Updated:** 2024-08-28
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `engine`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 3.7/3.9`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Scope.** Insert key (overtype vs insert modes) not currently
implemented on web/Linux/Windows; macOS lacks the key entirely.
Team noted "not currently implemented"; workaround is `Shortcuts`
with `LogicalKeyboardKey.insert`. Hex-editor use case offered.

**Why skip.** Feature-request-shaped bug. No `c:` label but the team
explicitly says this is unimplemented functionality, not a
regression. Adding overtype mode to TextField is a behavior addition
with design implications.

---

### #144936 — Desktop TextFormField ignores HOME/END/numpad arrows

- **URL:** https://github.com/flutter/flutter/issues/144936
- **Reactions:** 1 · **Labels:** `a: desktop`, `has reproducible steps`, `P2`, `team-text-input`
- **Decision:** **skip — engine-level** (partially fixed)

Flutter didn't define shortcuts for numpad navigation keys on desktop.
PRs #145146 and #145464 landed NumLock-aware numpad navigation on
Linux. Windows fix blocked by #98377 (Windows NumLock state reporting
bug). Linux-fixed, Windows-still-broken. Remaining Windows path is
engine-side (NumLock state reporting).

---

### #147138 — Android TextFormField numpad Enter doesn't fire onFieldSubmitted

- **URL:** https://github.com/flutter/flutter/issues/147138
- **Reactions:** 1 · **Labels:** `platform-android`, `framework`, `has reproducible steps`, `P3`, `team-text-input`
- **Decision:** **skip — engine-level**

Android-specific; gesture-navigation-bar-mode dependent. When a small
arrow indicator is tapped first, numpad Enter fires. Workaround uses
deprecated `RawKeyboardListener`; `KeyboardListener` doesn't receive
the event. Android embedder's gesture-nav mode interaction with
external keyboard numpad Enter routing is the fix path.

---

### #148936 — macOS right Control key not recognized by HardwareKeyboard

- **URL:** https://github.com/flutter/flutter/issues/148936
- **Reactions:** 1 · **Labels:** `platform-macos`, `a: desktop`, `has reproducible steps`, `P2`, `team-macos`
- **Decision:** **skip — engine-level**

External keyboard on macOS with both left+right Control keys:
`HardwareKeyboard.instance.isControlPressed` and `onKeyEvent` only
recognize left Control; right Control is ignored. Old
`RawKeyboard.onKey` recognizes both correctly. macOS plugin's
right-modifier-key forwarding in the new KeyEvent path is the fix.

---

### #149480 — Control modifier doesn't work in CharacterActivator

- **URL:** https://github.com/flutter/flutter/issues/149480
- **Reactions:** 1 · **Labels:** `framework`, `has reproducible steps`, `P2`, `team-text-input`
- **Decision:** **skip — engine-level**

Windows/macOS/Android/iOS: `CharacterActivator('g', control: true)`
doesn't fire on Ctrl+g; Linux works. `SingleActivator` with same
combo works on all platforms. Team's "Ctrl+G produces Bell ASCII"
hypothesis was refuted (fails on all alphabet keys). Root cause in
engine/framework CharacterActivator vs KeyEvent translation on
non-Linux platforms; could in principle be framework-testable but
requires platform-specific investigation that hasn't been done.

**Dedup scan.** Thematic cousin of #116658 / #119088 (layout-agnostic
shortcut requests) but different mechanism — those are about
activator-vs-character selection; this is about a specific modifier
being dropped.

---

### #150326 — Linux Wayland: pressing_records assertion failure

- **URL:** https://github.com/flutter/flutter/issues/150326
- **Reactions:** 1 · **Labels:** `engine`, `platform-linux`, `a: desktop`, `P2`, `team-text-input`
- **Decision:** **skip — engine-level**

Linux Wayland (Arch+KDE6 Wayland, Ubuntu 23.10 Wayland): paste + delete
sequence triggers `FlKeyEmbedderResponder`'s `lookup_hash_table
(pressing_records, physical_key) != 0` assertion. XWayland
unaffected. Engine emits key events with physical/logical key 0.
Still open in 3.29.2; workaround is XWayland. Sibling of the
PKC-1 watchlist (pressed-keys state corruption from engine-side
sequencing).

---

### #154563 — Android physical keyboard Backspace first-press (TextInputType.none)

- **URL:** https://github.com/flutter/flutter/issues/154563
- **Reactions:** 1 · **Labels:** `platform-android`, `P2`, `team-text-input`
- **Decision:** **skip — engine-level**

Intermittent Android issue: `TextFormField` with
`keyboardType: TextInputType.none` + physical keyboard — first
Backspace press doesn't register. Subsequent Backspace works.
`TextField` workaround exists. Android IME service state
interaction with `TextInputType.none`; fix path is Android embedder
or framework `TextFormField` behavior under that input type.

---

### #178609 — macOS KeyEvent doesn't expose NSEvent modifier flags

- **URL:** https://github.com/flutter/flutter/issues/178609
- **Reactions:** 1 · **Labels:** `platform-macos`, `P2`, `team-macos`
- **Decision:** **skip — engine-level**

External apps (Raycast, Alfred, Wispr Flow, Spokenly) send synthetic
keyboard events with modifier flags via NSEvent. macOS plugin doesn't
surface those modifier flags to Dart's `KeyEvent` because no
physical modifier key was pressed; `HardwareKeyboard.isMetaPressed`
returns false. macOS plugin needs to forward NSEvent modifier flags
independently of physical key state. Related: #153907.

---

### #181907 — [Windows] Shift key randomly gets stuck in pressed state

- **URL:** https://github.com/flutter/flutter/issues/181907
- **Reactions:** 1 · **Labels:** `platform-windows`, `P2`, `team-windows`
- **Decision:** **skip — engine-level** (PKC-1 watchlist)

Windows: intermittent Shift-key stuck state during TextField editing
(Shift+arrows, Shift+click, or unfocus+refocus). Single triage
acknowledgment comment; no root cause. Fourth data point for the
PKC-1 (pressed-keys-state-corruption) watchlist — promoting that
watchlist to tentative cluster status.

---

### #27880 — TextFormField doesn't support input shortcuts (IME toolbar)

- **URL:** https://github.com/flutter/flutter/issues/27880
- **Reactions:** 0 · **Labels:** `c: new feature`, `framework`, `P2`, `team-framework`
- **Decision:** **skip — feature/proposal**

Request for third-party IME toolbar shortcuts (copy/paste/select
buttons rendered by the IME) to interact with Flutter TextFormField.
Linked to #14047. 7-year-old feature gap.

---

### #59444 — [Flutter Web] FocusNode with RawKeyBoardListener

- **URL:** https://github.com/flutter/flutter/issues/59444
- **Reactions:** 0 · **Labels:** `framework`, `engine`, `platform-web`, `f: focus`, `P2`, `team-web`
- **Decision:** **skip — engine-level**

Thin issue: "Is there a way to use FocusNode with RawKeyBoardListener
on Flutter Web?" filed from a Tizen context. No summary, no
reproducible behavior identified. `RawKeyboard` is now the legacy API;
users are directed to `HardwareKeyboard` + `KeyboardListener`.

---

### #61039 — [Web] RawKeyEvent valid assertion broken in tests

- **URL:** https://github.com/flutter/flutter/issues/61039
- **Reactions:** 0 · **Labels:** `a: tests`, `c: contributor-productivity`, `framework`, `platform-web`, `P3`, `c: tech-debt`, `team: skip-test`, `team-web`
- **Decision:** **skip — feature/proposal** (test-infrastructure tech-debt)

Two tests in `raw_keyboard_test.dart` are skipped for web because they
expect assertions on invalid `unicodeScalarValues` that don't fire in
the web runtime. Tech-debt cleanup, not a product bug.

---

### #74233 — TextField adds newline on Enter without Shift on macOS

- **URL:** https://github.com/flutter/flutter/issues/74233
- **Reactions:** 0 · **Labels:** `framework`, `platform-macos`, `a: desktop`, `has reproducible steps`, `P2`, `team-macos`
- **Decision:** **skip — engine-level**

macOS TextField ignores Shift-modifier for Enter: `TextInputAction.done`
or `TextInputAction.newline` both produce newlines regardless of
whether Shift is held. Workaround uses `RawKeyboardListener` with
`TextInputAction.unspecified`. Fix path is the macOS plugin's
Enter-key translation to `TextInputAction` semantics.

---

### #76632 — Access to Shift-toggle keys via LogicalKeyboardKey

- **URL:** https://github.com/flutter/flutter/issues/76632
- **Reactions:** 0 · **Labels:** `c: new feature`, `engine`, `c: proposal`, `P3`, `team-engine`
- **Decision:** **skip — feature/proposal**

Request for convenience statics like `LogicalKeyboardKey.ampersand`
(currently reachable only via `LogicalKeyboardKey(0x26)`). Related
layout-dependent key mapping tracked in #77048.

---

### #78054 — iOS HID input not processed on iOS 13+ (Flutter 2.0+ regression)

- **URL:** https://github.com/flutter/flutter/issues/78054
- **Reactions:** 0 · **Labels:** `platform-ios`, `has reproducible steps`, `P2`, `team-ios`
- **Decision:** **skip — engine-level**

iOS HID input (Bluetooth keyboard, HID barcode scanners) via
`AppDelegate.keyCommands` only fires when a TextField is focused on
iOS 13+. Pre-Flutter-2.0 it fired regardless. Flutter 2.0 engine
change in UIKeyCommands handling is the regression source. Related
pattern with #80108 (Windows barcode scanner) in the NKI-1
watchlist, but different platform/fix target.

---

### #78572 — Windows word-modifier inconsistencies

- **URL:** https://github.com/flutter/flutter/issues/78572
- **Reactions:** 0 · **Labels:** `framework`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `team-windows`
- **Decision:** **skip — engine-level**

Windows Ctrl+Arrow word navigation: Windows native jumps to start of
next word in both directions, while macOS jumps to end-of-next-word
(right arrow) or start-of-previous-word (left). Flutter matches the
macOS convention on Windows. Framework-level shortcut map per
platform would be the fix shape; engine-labeled because the
per-platform shortcut tables are managed engine-adjacent.

---

### #79040 — Tab+Shift order dependency (shortcut system)

- **URL:** https://github.com/flutter/flutter/issues/79040
- **Reactions:** 0 · **Labels:** `framework`, `f: material design`, `a: desktop`, `has reproducible steps`, `P2`, `team-framework`
- **Decision:** **skip — engine-level**

Pressing Tab first then Shift (Tab+Shift order) moves focus forward
and then back; Shift+Tab (Shift first) works correctly. Flutter's
shortcut system doesn't account for key-press order when evaluating
modifier combinations. Team noted known gap with changes being
considered; no PR. Fix is in the framework's shortcut evaluation
logic but currently deferred.

---

### #79497 — ExpansionTile + TextField backspace behavior

- **URL:** https://github.com/flutter/flutter/issues/79497
- **Reactions:** 0 · **Labels:** `framework`, `f: focus`, `has reproducible steps`, `P3`, `team-text-input`
- **Decision:** **skip — engine-level**

Combining TextField with ExpansionTile produces undesirable backspace
behavior. Only a triage comment confirming reproduction; no root
cause identified. Likely focus/shortcut intercept pattern similar
to #163475 MenuAnchor case (batch 2), but without diagnostic work.

---

### #81172 — Uppercase and case-insensitive LogicalKeyboardKey statics

- **URL:** https://github.com/flutter/flutter/issues/81172
- **Reactions:** 0 · **Labels:** `c: new feature`, `framework`, `c: proposal`, `P3`, `team-framework`
- **Decision:** **skip — feature/proposal**

Request for uppercase `LogicalKeyboardKey` statics. Team decided to
add uppercase convenience statics.

---

### #83611 — [Flutter Web] EditableText doesn't receive keyboard events after clicking an HtmlElementView

- **URL:** https://github.com/flutter/flutter/issues/83611
- **Reactions:** 0 · **Labels:** `engine`, `a: platform-views`, `platform-web`, `has reproducible steps`, `P2`, `team-web`
- **Decision:** **skip — engine-level**

Clicking a platform view (HtmlElementView) blurs the browser-side
focus from Flutter's TextField but the framework still considers the
field focused. Root cause: Flutter lacks a concept of "blur a text
field without focusing something else." Escalated to P1 note;
broader platform-view focus design issue.

---

### #83733 — Create CommandOrControl activator (cross-platform Ctrl/Cmd)

- **URL:** https://github.com/flutter/flutter/issues/83733
- **Reactions:** 0 · **Labels:** `engine`, `c: proposal`, `P3`, `team-engine`
- **Decision:** **skip — feature/proposal**

Proposal for `OsSingleActivator` / `AdaptiveSingleActivator` with
`osControl`/`osMeta` fields so Ctrl+C means Cmd+C on macOS. Electron's
`CommandOrControl` cited. Flutter's built-in default editing
shortcuts already handle this via separate platform maps, but no
public-API activator exists for user shortcuts.

---

### #91603 — [Web][Windows] RawKeyboard listener intercepted by Chrome for Ctrl+D

- **URL:** https://github.com/flutter/flutter/issues/91603
- **Reactions:** 0 · **Labels:** `c: new feature`, `framework`, `engine`, `platform-windows`, `platform-web`, `has reproducible steps`, `P3`, `team-web`
- **Decision:** **skip — feature/proposal**

Flutter web on Windows: Ctrl+D triggers Chrome's bookmark dialog
before the app can handle it. Same issue for macOS with Cmd+D.
Browser-level intercept; no framework fix possible. `c: new feature`-
labeled as "provide a way to prevent the browser from stealing."

---

### #93450 — Device-specific keyboard events on Fuchsia

- **URL:** https://github.com/flutter/flutter/issues/93450
- **Reactions:** 0 · **Labels:** `framework`, `engine`, `platform-fuchsia`, `P2`, `team-text-input`
- **Decision:** **skip — engine-level**

Fuchsia backspace not normalized — reported as
`LogicalKeyboardKey(42 | LogicalKeyboardKey.fuchsiaPlane)` instead of
`LogicalKeyboardKey.backspace`. Dependency on upstream Fuchsia
changes. Fuchsia-specific; low-priority platform.

---

### #93778 — [Web] RawKeyUpEvent not triggered on Ctrl+mouse-click (macOS Chrome context menu)

- **URL:** https://github.com/flutter/flutter/issues/93778
- **Reactions:** 0 · **Labels:** `framework`, `platform-web`, `has reproducible steps`, `P2`, `team-web`
- **Decision:** **skip — engine-level**

Ctrl+click on macOS Chrome opens the browser context menu, which
swallows the Ctrl key-up event — Flutter never receives it,
leaving framework state with Ctrl still held. Browser-level
swallowing; no in-Flutter fix without cooperation from the browser.
Another PKC-1-adjacent case (Ctrl stuck in pressed state after
browser intercept), but the trigger is browser UI rather than
engine synthesis.

---

### #93873 — KeyEventResult.skipRemainingHandlers differs across platforms (by design)

- **URL:** https://github.com/flutter/flutter/issues/93873
- **Reactions:** 0 · **Labels:** `engine`, `a: desktop`, `f: focus`, `has reproducible steps`, `P3`, `team-text-input`
- **Decision:** **skip — feature/proposal**

TextField's FocusNode returns `skipRemainingHandlers`, stopping key
events from reaching top-level Shortcuts. Desktop behavior is
considered correct by design; web diverges. Team concluded platforms
intentionally differ; no fix planned. Effectively a "won't fix"
design-discussion close.

---

### #94441 — [Android] Alt+Tab with Bluetooth keyboard → assertion, keyboard unusable

- **URL:** https://github.com/flutter/flutter/issues/94441
- **Reactions:** 0 · **Labels:** `platform-android`, `framework`, `has reproducible steps`, `P2`, `team-android`
- **Decision:** **skip — engine-level** (PKC-1 cluster)

After alt+tab switches away and back, engine synthesizes key-up for
Alt; next key-repeat event fires `_pressedKeys.containsKey`
assertion because the key was never recorded as re-pressed. Keyboard
becomes unusable. Classic PKC-1 pattern (pressed-keys state
corruption from engine-side sequencing) on Android via Bluetooth
keyboard.

**Cluster.** **PKC-1** — confirmed member.

---

### #96572 — [Desktop] Holding down a key does not repeat keystrokes

- **URL:** https://github.com/flutter/flutter/issues/96572
- **Reactions:** 0 · **Labels:** `framework`, `engine`, `a: desktop`, `has reproducible steps`, `P2`, `team-text-input`
- **Decision:** **skip — engine-level**

macOS + Linux: holding a key doesn't produce repeat keystrokes
(native macOS shows accent menu instead). Native Linux and Windows
behavior not determined in thread. Engine-side key-repeat dispatch
at the embedder level. Sibling of #96660 (iOS hold-Backspace
doesn't repeat, batch 1) — both are "hold-key-no-repeat"
regressions/gaps on different platforms.

---

### #98377 — [Windows][HardwareKeyboard] Incorrect Caps Lock state on startup

- **URL:** https://github.com/flutter/flutter/issues/98377
- **Reactions:** 0 · **Labels:** `framework`, `engine`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `team-windows`
- **Decision:** **skip — engine-level**

Starting Flutter app on Windows with Caps Lock already enabled:
`HardwareKeyboard.instance.lockModesEnabled` reports inverted state.
Engine doesn't query initial lock state from OS on startup. Also
affects Linux; macOS has a variant where lockModesEnabled doesn't
update until a key event fires. Also: lockModesEnabled fails to
update when Caps Lock toggles while app unfocused. Persists through
3.19. Related #98533.

---

### #98533 — [Win32] Fix synthesization of toggle keys from phase 0 to 3

- **URL:** https://github.com/flutter/flutter/issues/98533
- **Reactions:** 0 · **Labels:** `platform-windows`, `a: desktop`, `P2`, `team-windows`
- **Decision:** **skip — engine-level**

Win32 synthesization: last observed phase 0 (pressed 0 toggled 0)
and current phase 3 (pressed 1 toggled 0) should emit 3 events
(down, up, down) but only 1 event (down) is emitted. TODO for a
unit test `SynthesizeModifiers`. Windows embedder key-event
synthesis. Sibling of #98377 (Caps Lock state) and WKR-1 pattern.

---

### #99198 — Distinguish keys with same scancodes but different logical keys

- **URL:** https://github.com/flutter/flutter/issues/99198
- **Reactions:** 0 · **Labels:** `c: new feature`, `framework`, `platform-windows`, `c: proposal`, `P3`, `team-framework`
- **Decision:** **skip — feature/proposal**

Win+V paste and web context-menu emoji insert produce emulated
Ctrl+V / Win+period with scancode 0 on Windows and empty/Unidentified
code on Chromium web. Proposal to distinguish these from
user-typed keys. Extracted from #97582 and #88646. Chromium bug
filed.

---

### #99255 — CharacterActivator not working with hardware keyboard on iOS

- **URL:** https://github.com/flutter/flutter/issues/99255
- **Reactions:** 0 · **Labels:** `platform-ios`, `P2`, `team-ios`
- **Decision:** **skip — engine-level**

iOS-specific `CharacterActivator` silent with hardware keyboard
(Android works). No substantive thread activity beyond a bot comment.
Thematic sibling of #149480 (Control modifier in CharacterActivator
broken on Win/macOS/Android/iOS) — both are CharacterActivator
failures on specific platforms. Same general "CharacterActivator
doesn't see what SingleActivator sees" family.

---

### #99653 — [Windows] Microsoft IME triggers KeyUpEvent assertion

- **URL:** https://github.com/flutter/flutter/issues/99653
- **Reactions:** 0 · **Labels:** `framework`, `platform-windows`, `a: desktop`, `a: error message`, `P2`, `team-windows`
- **Decision:** **skip — engine-level** (PKC-1 cluster)

Windows Microsoft Pinyin/Japanese IME absorbs Shift key-down, emits
only key-up → `_pressedKeys` has no record of the physical key →
assertion. Appeared in Flutter 3.3 (not 3.0.5); 3.4 beta may have
fixed it; status unclear. Textbook PKC-1 pattern.

**Cluster.** **PKC-1** — confirmed member.

---

### #100041 — [iOS] FlutterViewController initWithEngine breaks keyboardManager

- **URL:** https://github.com/flutter/flutter/issues/100041
- **Reactions:** 0 · **Labels:** `platform-ios`, `engine`, `P2`, `team-ios`
- **Decision:** **skip — engine-level**

Creating `FlutterViewController` via `initWithEngine` leaves
`_engineNeedsLaunch = NO`, so `addInternalPlugins` is skipped and
`keyboardManager` stays nil. External/physical keyboard input is
dropped; soft keyboard works. iOS plugin initialization-order bug.

---

### #100042 — [iOS] Long-press delete on physical keyboard doesn't delete continuously

- **URL:** https://github.com/flutter/flutter/issues/100042
- **Reactions:** 0 · **Labels:** `platform-ios`, `framework`, `a: fidelity`, `has reproducible steps`, `P2`, `found in release: 2.10/2.13`, `team-text-input`
- **Decision:** **likely-duplicate of #96660**

Same symptom and root cause as #96660 (processed batch 1): iOS
physical keyboard key-repeat not forwarded to framework. #96660 is
the more-reacted filing (8 reactions vs 0) with the wider scope
("any hardware key, not just Backspace"); this one is the delete-
specific narrative. One fix closes both.

---

### #101275 — Android TV Select key `keysPressed is empty` assertion

- **URL:** https://github.com/flutter/flutter/issues/101275
- **Reactions:** 0 · **Labels:** `platform-android`, `framework`, `a: error message`, `P2`, `team-design`, `a: tv`
- **Decision:** **skip — engine-level** (NKI-1 cluster)

Android TV and IR remotes send Select mapped to `Control Right`
physical key without modifier flags; framework's
`keysPressed is non-empty` assertion fires on the first KeyDown.
Also reported with Windows USB barcode scanners on Shift Left.
Same NKI-1 pattern as #65233 (IR remote), #152391 (PDA keyboard),
#80108 (Windows barcode scanner). Workaround via #65233's FocusNode
onKey trick.

**Cluster.** **NKI-1** — confirmed member.

---

### #101285 — [Windows][Surface] Shift + trackpad → stuck keys

- **URL:** https://github.com/flutter/flutter/issues/101285
- **Reactions:** 0 · **Labels:** `framework`, `platform-windows`, `a: desktop`, `a: error message`, `P2`, `team-windows`
- **Decision:** **skip — engine-level** (PKC-1 cluster)

Microsoft Surface: pressing right-Shift + touching trackpad leaves
Caps/Ctrl stuck. Triager couldn't reproduce on non-Surface Windows.
Linked as similar to #99653. Surface-specific variant of the PKC-1
pattern.

**Cluster.** **PKC-1** — confirmed member (Surface-specific).

---

### #116456 — macOS "Dvorak - QWERTY ⌘" layout mapping

- **URL:** https://github.com/flutter/flutter/issues/116456
- **Reactions:** 0 · **Labels:** `platform-macos`, `a: desktop`, `P2`, `team-macos`
- **Decision:** **skip — engine-level**

macOS "Dvorak - QWERTY ⌘" layout has a second layer remapping keys
to QWERTY when Cmd is held. Flutter's mapping algorithm doesn't
handle two-layer behavior; Cmd+V on Dvorak fires as Cmd+J.

**Dedup scan.** Sibling of #100456 (analyze keyboard layout) and
#35347 (web RawKeyboardListener wrong) — all "Flutter's logical-key
derivation doesn't match native for non-US/alt layouts" family.

---

### #123565 — [Android] Chromebook numpad Control generates Num Lock

- **URL:** https://github.com/flutter/flutter/issues/123565
- **Reactions:** 0 · **Labels:** `engine`, `platform-chromebook`, `P2`, `team-engine`
- **Decision:** **skip — engine-level**

Lenovo Duet Chromebook (and Chromecast keyboard): pressing Control
generates Num Lock key event alongside. Chromebook-specific, no
device access for team.

---

### #130676 — [macOS] Keyboard exception on app start while Caps Lock is on

- **URL:** https://github.com/flutter/flutter/issues/130676
- **Reactions:** 0 · **Labels:** `framework`, `engine`, `platform-macos`, `a: error message`, `has reproducible steps`, `P3`, `found in release: 3.10/3.13`, `team-macos`
- **Decision:** **skip — engine-level** (PKC-1 cluster)

macOS app start with Caps Lock on → exception. Caps Lock generates
synthesized KeyUpEvent without corresponding KeyDown being tracked.
Engine-labeled. Sibling of #98377 Windows Caps Lock startup state.

**Cluster.** **PKC-1** — confirmed member (macOS Caps Lock startup).

---

### #132879 — [Shortcuts] Support shortcut sequences (chords)

- **URL:** https://github.com/flutter/flutter/issues/132879
- **Reactions:** 0 · **Labels:** `c: proposal`, `P2`, `team-text-input`
- **Decision:** **skip — feature/proposal**

Proposal for multi-keypress shortcut sequences (VS Code `Ctrl+K
Ctrl+O`, Gmail `g i`). Discussion notes configurable chord timeout
is needed (Gmail has one, vim doesn't).

---

### #133954 — KeyEventSimulator missing numpadEnter in Windows keyCode map

- **URL:** https://github.com/flutter/flutter/issues/133954
- **Reactions:** 0 · **Labels:** `a: tests`, `framework`, `platform-windows`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 3.13/3.14`, `team-windows`
- **Decision:** **skip — engine-level** (framework test infra gap)

`KeyEventSimulator` missing `numpadEnter` in its Windows keyCode
map, so `tester.sendKeyEvent(LogicalKeyboardKey.numpadEnter)` fails
under `defaultTargetPlatform = windows`. Companion to #96022 (macOS
shift+key missing) and #96021 (uppercase unsupported) — framework
test-harness completeness gaps.

---

### #134174 — Japanese characters left-arrow navigation with physical keyboard

- **URL:** https://github.com/flutter/flutter/issues/134174
- **Reactions:** 0 · **Labels:** `a: internationalization`, `P2`, `team-framework`, `from: manual-qa`
- **Decision:** **skip — engine-level**

iOS/Android with physical Magic keyboard: typing Japanese RTL
characters, can't navigate through them with left arrow. No summary,
no diagnostic progress.

---

### #140764 — macOS "Rewind" and "Fast Forward" key events not received

- **URL:** https://github.com/flutter/flutter/issues/140764
- **Reactions:** 0 · **Labels:** `P2`, `team-macos`
- **Decision:** **skip — engine-level**

macOS media keys (rewind, fast forward, alongside #99848's play/pause
family) not forwarded to HardwareKeyboard. Same media-key family as
#99848; thematic sibling.

---

### #140790 — [Linux] Neo2 keyboard layout layer-4 keys not recognized

- **URL:** https://github.com/flutter/flutter/issues/140790
- **Reactions:** 0 · **Labels:** `platform-linux`, `a: desktop`, `P2`, `team-linux`
- **Decision:** **skip — engine-level**

Linux desktop + Neo2 keyboard layout (M4/Mod4 layer): WASD/ESDF
combos should produce arrow/control events, but don't on Flutter
Linux desktop (web works). Requires physical ISO keyboard with
AltGr. Layout-mapping family like #100456, #35347, #116456.

---

### #143155 — Windows barcode scanner Shift Left with no modifiers → assertion

- **URL:** https://github.com/flutter/flutter/issues/143155
- **Reactions:** 0 · **Labels:** `platform-windows`, `a: desktop`, `a: error message`, `P3`, `team-design`
- **Decision:** **skip — engine-level** (NKI-1 cluster)

Windows barcode scanner emits Shift Left key-down with modifiers=0.
Fires `keysPressed` assertion. Exact NKI-1 pattern alongside #65233,
#152391, #80108, #101275.

**Cluster.** **NKI-1** — confirmed member.

---

### #147162 — Raw web keyCode can't be extracted from KeyEvent (WebOS magic remote)

- **URL:** https://github.com/flutter/flutter/issues/147162
- **Reactions:** 0 · **Labels:** `e: device-specific`, `platform-web`, `P2`, `team-web`
- **Decision:** **skip — engine-level**

Post-3.19 `KeyEvent` migration doesn't expose platform-specific
`keyCode` (intentional, per @gspencergoog). WebOS magic remote
special keys only provide `keyCode` with empty `code`; no mapping.
Fix: add mappings in keycode generator database. Also affects
Android TV / Fire TV users who need raw keycodes.

---

### #148375 — Android KeyboardListener catches software keyboard input

- **URL:** https://github.com/flutter/flutter/issues/148375
- **Reactions:** 0 · **Labels:** `platform-android`, `framework`, `P3`, `team-text-input`
- **Decision:** **skip — engine-level**

Android `InputConnection.sendKeyEvent()` allows software keyboards
to send backspace/enter as hardware `KeyEvent`s; Flutter doesn't
distinguish from physical key events. `InputConnectionAdaptor.java`
conflates the two paths. PR-invited in comments.

---

### #150338 — onFieldSubmitted doesn't fire on desktop when readOnly: true

- **URL:** https://github.com/flutter/flutter/issues/150338
- **Reactions:** 0 · **Labels:** `platform-macos`, `platform-windows`, `platform-linux`, `a: desktop`, `has reproducible steps`, `P2`, `team-text-input`, `found in release: 3.22/3.23`
- **Decision:** **write-test** → **fail-as-expected** (confirms bug is real and framework-observable)

**Root cause (per commenter).** `_shouldCreateInputConnection`
returns `false` for `readOnly: true` on non-web desktop, so
`TextInputConnection` isn't created — `onFieldSubmitted` never fires,
and Edit-menu Copy/Select-All also breaks on macOS. Web works
because `kIsWeb` short-circuits to `true`.

**Test approach.** `testWidgets` with `debugDefaultTargetPlatformOverride
= windows`, pumps a `TextFormField(readOnly: true, onFieldSubmitted:
...)`, focuses via `FocusNode.requestFocus`, sends
`LogicalKeyboardKey.enter`, asserts the `onFieldSubmitted` callback
fires with the initial value.

**Test:** [`issue_150338_onsubmitted_readonly_desktop_test.dart`](../regression_tests/hardware_keyboard/issue_150338_onsubmitted_readonly_desktop_test.dart)

**Test outcome.** Fails as expected: `Actual: <null>` vs
`Expected: 'hello'`. Callback never fires. Confirms the bug is real,
framework-observable, and framework-fixable.

---

### #153811 — KeyEvent USB-HID code wrong; AltGr emitted as Alt Right (macOS German)

- **URL:** https://github.com/flutter/flutter/issues/153811
- **Reactions:** 0 · **Labels:** `framework`, `a: internationalization`, `has reproducible steps`, `P2`, `team-framework`, `found in release: 3.24/3.25`
- **Decision:** **skip — engine-level**

macOS + German input: Alt/Option Right equivalent to AltGr but
Flutter reports `Alt Right` instead of `altGraph`; USB HID code is
`0x68` instead of correct `0x46`. Same theme as #154069 (Windows
AltGr Ctrl+Alt), different platform/mechanism.

---

### #155073 — [Web][Edge][Production] Spacebar sometimes doesn't work

- **URL:** https://github.com/flutter/flutter/issues/155073
- **Reactions:** 0 · **Labels:** `c: regression`, `platform-web`, `e: web_canvaskit`, `a: production`, `browser: edge`, `P2`, `team-text-input`
- **Decision:** **skip — engine-level**

Web + Edge release build: spacebar / Enter intermittently fail in
TextFields inside `SingleChildScrollView`. F5 soft-reload fixes
temporarily. Linked to #59439 focus regression. Workarounds:
remove `SingleActivator(space)` from `_defaultWebShortcuts` or
regenerate `index.html` via `flutter create . --platforms web`
(stale bootstrapping script is implicated).

---

### #155081 — FlutterEngineSendKeyEvent doesn't work in custom GLFW embedder

- **URL:** https://github.com/flutter/flutter/issues/155081
- **Reactions:** 0 · **Labels:** `engine`, `e: embedder`, `a: desktop`, `P3`, `team-engine`
- **Decision:** **likely-stale (signal-based)** — unmaintained platform

GLFW embedder example is unmaintained per team note; no fix planned.
Custom embedder path, not a Flutter-shipped platform.
**Recommendation:** close as "out of scope, unmaintained example."

---

### #155089 — Cmd+Enter on Chrome (macOS): Enter considered held down (upstream browser)

- **URL:** https://github.com/flutter/flutter/issues/155089
- **Reactions:** 0 · **Labels:** `platform-web`, `has reproducible steps`, `P2`, `team-text-input`, `found in release: 3.24/3.26`
- **Decision:** **likely-stale (signal-based)** — upstream browser/OS bug

macOS/Safari doesn't send `keyup` for Enter when Meta held. Chromium
bug filed at https://issues.chromium.org/issues/366284864. Framework
workaround: simulate KeyUpEvent after 100ms. Recommend close as
upstream browser issue with pointer to Chromium tracker.

---

### #157279 — [Android] IntlBackslash not recognized on ISO 102/105 keyboard

- **URL:** https://github.com/flutter/flutter/issues/157279
- **Reactions:** 0 · **Labels:** `platform-android`, `platform-linux`, `P2`, `team-text-input`
- **Decision:** **skip — engine-level**

Android + ISO 102/105 keyboard: IntlBackslash key (between left
Shift and letter) not recognized. Needs ISO keyboard to verify;
triager lacks device. Layout-mapping family (#100456, #35347,
#116456, #140790).

---

### #159384 — [Android] SwiftKey produces wrong PhysicalKeyboardKey usbHidUsage

- **URL:** https://github.com/flutter/flutter/issues/159384
- **Reactions:** 0 · **Labels:** `platform-android`, `has reproducible steps`, `P2`, `team-text-input`, `found in release: 3.24/3.27`
- **Decision:** **skip — engine-level**

Android + Microsoft SwiftKey as default IME: physical keyboard
usbHidUsage codes are wrong. Default Android IME produces correct
codes. Android-embedder + SwiftKey variant of the "Android embedder
forwards non-standard IME behavior" family (cf. AIR-1 and the
running SwiftKey pattern #102142, #154692).

---

### #161217 — [file_selector] KeyUpEvent missing after getSaveLocation dialog

- **URL:** https://github.com/flutter/flutter/issues/161217
- **Reactions:** 0 · **Labels:** `framework`, `package`, `has reproducible steps`, `P2`, `p: file_selector`, `team-text-input`, `found in release: 3.27/3.28`
- **Decision:** **skip — engine-level**

Ctrl+S triggers `getSaveLocation()` dialog, returns; KeyUpEvent for
Key S never fires (only Control Left's up fires). Macros/Windows
confirmed. Dialog-focus-transition swallows the up event — similar
in spirit to #93778 (Ctrl+click context menu swallows Ctrl up) but
with a Flutter dialog rather than a browser-native one.

---

### #168886 — Android KeyEvent.deviceType always returns Keyboard (bitmask vs equality bug)

- **URL:** https://github.com/flutter/flutter/issues/168886
- **Reactions:** 0 · **Labels:** `platform-android`, `engine`, `has reproducible steps`, `P2`, `team-text-input`, `found in release: 3.29/3.33`, `a: tv`
- **Decision:** **skip — engine-level**

Android `KeyEvent.getSource()` returns combined bitmask (e.g.,
`0x301 = SOURCE_KEYBOARD | SOURCE_DPAD`); `_convertDeviceType` in
`hardware_keyboard.dart` does exact equality, falls through to
`keyboard` default. Fix: bitwise AND. Framework file named but
the fix is tracked with the "Android input source bitmask"
embedder/framework boundary. Strong PR candidate; no PR yet.

---

### #172635 — Tab inserts space on iOS-app-on-Apple-Silicon-macOS

- **URL:** https://github.com/flutter/flutter/issues/172635
- **Reactions:** 0 · **Labels:** `platform-macos`, `platform-target-arm`, `f: focus`, `has reproducible steps`, `P3`, `team-text-input`, `found in release: 3.32/3.33`
- **Decision:** **skip — engine-level**

Apple Silicon Mac running iOS app via "My Mac (Designed for iPad)":
Tab inserts space instead of changing focus. Confirmed on master.
iOS-on-macOS target is a specific embedding path; Tab-shortcut
routing differs there.

---

### #172741 — [iOS] Hold arrow key moves cursor one position then stops

- **URL:** https://github.com/flutter/flutter/issues/172741
- **Reactions:** 0 · **Labels:** `platform-ios`, `has reproducible steps`, `P2`, `team-text-input`, `found in release: 3.32/3.33`
- **Decision:** **skip — engine-level**

iPad physical keyboard: holding arrow moves cursor one position
then stops. Left-arrow also moves right (!). Contributor
investigating timer-based fix. Same iOS-hardware-key-repeat family
as #96660 and #100042.

---

### #180435 — Action.overridable cannot be overridden by DoNothingAction

- **URL:** https://github.com/flutter/flutter/issues/180435
- **Reactions:** 0 · **Labels:** `c: crash`, `framework`, `a: error message`, `has reproducible steps`, `P2`, `team-text-input`, `found in release: 3.38/3.40`
- **Decision:** **skip — engine-level**

Two bugs in one issue: (1) `DoNothingAction` fails the
`is Action<T>` check in `Actions._castAction` (invariant generics);
typed `MyDoNothingAction<T extends Intent>` is a workaround; (2)
`ExtendSelectionVerticallyToAdjacent*Intent` can't be individually
overridden because the underlying action is typed
`DirectionalCaretMovementIntent`. PR #180883 may have addressed the
second. Framework-observable; could be write-test if
`Actions._castAction` exposed for testing — skipping for velocity.

---

### #184571 — [macOS] CGEvent-injected Cmd+V loses Command modifier

- **URL:** https://github.com/flutter/flutter/issues/184571
- **Reactions:** 0 · **Labels:** `platform-macos`, `has reproducible steps`, `P2`, `workaround available`, `team-text-input`, `fyi-macos`
- **Decision:** **skip — engine-level**

macOS apps that inject keystrokes via CGEvent (Raycast, Wispr Flow,
SuperWhisper): Cmd+V paste works in native macOS TextField but
Flutter's internal keyboard processing loses the modifier flag for
synthetic events. NSEvent `performKeyEquivalent` has the flag; it's
lost before reaching Dart. Workaround via `performKeyEquivalent`
override in `MainFlutterWindow.swift`. Closely related to #178609
(macOS NSEvent modifier flags).

---

## Duplicate clusters

### Cluster PKC-1: Pressed-keys state corruption from engine-side sequencing (tentative, shared root cause)

Embedders emit key-event sequences that violate the framework's
`_pressedKeys` invariants, leaving stale or mismatched entries that
cause subsequent events to fire assertions or mis-dispatch as
modifier+key shortcuts when no modifier is actually held.

- **#107972** (32 reactions, P2, Windows) — KeyRepeatEvent without matching down; debug assertion `_assertEventIsRegular` · **processed** · (WKR-1 canonical)
- **#106475** (12 reactions, P2, Windows) — consequence of #107972 · **processed**
- **#95634** (1 reaction, P2, web+Windows) — `logicalKeysPressed` leaks previously-pressed key across Meta+K → Arrow-Left · **processed**
- **#100455** (1 reaction, P2, web+macOS) — Cmd+digit → Option+digit triggers `_pressedKeys[physical] == logical` assertion · **processed**
- **#181907** (1 reaction, P2, Windows) — Shift randomly stuck; thin triage, matches symptom family · **processed**
- **#94441** (0 reactions, P2, Android) — Alt+Tab Bluetooth keyboard triggers `_pressedKeys.containsKey` assertion · **processed**
- **#99653** (0 reactions, P2, Windows) — Microsoft IME absorbs Shift key-down, emits only key-up · **processed**
- **#101285** (0 reactions, P2, Windows Surface) — right-Shift + trackpad touch → Caps/Ctrl stuck · **processed**
- **#130676** (0 reactions, P3, macOS) — Caps Lock on app start fires exception (synthesized up without tracked down) · **processed**

Shared pattern: engine's key-event translation loses state integrity
under modifier+non-modifier sequences or focus transitions. Fix path
is per-embedder state cleanup but same conceptual contract
("embedder must emit key-up for non-modifier when released, even if
modifier still held; must not emit repeat without prior down; must
consistent-map logical keys across modifier transitions").

### Cluster NKI-1: Non-keyboard input device mis-mapping (tentative, shared symptom)

Non-keyboard input sources (IR remotes, PDA keyboards, barcode
scanners) emit raw events that Flutter's embedders mis-map through
keyboard physical/logical-key tables, triggering assertion
failures or producing incorrect logical keys. Fix path: each
embedder should detect non-keyboard sources (via platform
`InputDevice` APIs) and bypass keyboard-specific modifier
synchronization / logical-key derivation.

- **#65233** (1 reaction, P2, Android TV) — IR remote OK/Select scan-code 97 → "Control Right" logical key; `_assertEventIsRegular` fires · **processed**
- **#152391** (3 reactions, P2, Android) — PDA HT730 keyboard maps Shift Right physical → Shift Left logical · **processed**
- **#80108** (1 reaction, P2, Windows) — barcode scanner shift+digit produces mismatched logical/physical keys · **processed**
- **#101275** (0 reactions, P2, Android TV) — Select key mapped to Control Right fires `keysPressed is non-empty` assertion; same family · **processed**
- **#143155** (0 reactions, P3, Windows) — barcode scanner emits Shift Left with modifiers=0; same assertion · **processed**

### Cluster WKR-1: Windows synthesized key-event ordering (tentative, tight duplicates)

**Promoted into PKC-1 as sub-cluster.** Retained here for the tight
pair's direct fix lead (engine PR #36129 and its regression history).

Windows embedder synthesizes `KeyUpEvent` before `KeyRepeatEvent` for
held modifier keys, causing the framework's
`HardwareKeyboard._assertEventIsRegular` to fire (`_pressedKeys` no
longer contains the key). Debug-only; once assertion fires,
`_keyEventsSinceLastMessage` doesn't clear, permanently breaking
shortcut handling until app restart.

- **#107972** (32 reactions, P2) — direct framing of the assertion (`A KeyRepeatEvent is dispatched, but the state shows...`) · **processed** · **canonical**
- **#106475** (12 reactions, P2) — user-visible consequence ("keyboard shortcuts stop working after modifier key repeat") · **processed**

History: engine PR #36129 landed in 3.4/3.5 as fix; regressions
observed in 3.7.0 and 3.19.5/3.19.6 per #107972 comments. Likely
multiple recurring engine-side changes re-introduce the broken
synthesis ordering. Recommend the Windows embedder team add a
regression test at the embedder level that asserts "held modifier
doesn't emit KeyUpEvent before KeyRepeatEvent."

## Likely-stale candidates for closure review

- **#90207** — Android 12 webview keyboard Display ID mismatch.
  **Basis:** signal-based — `webview_flutter >= 3.0.0` defaults to
  hybrid composition (the workaround that sidesteps the
  VD-DisplayId mismatch). Most users are no longer hit by this.
  **Verification:** confirm on current webview_flutter with
  Android 12+ before closing; if confirmed non-reproducing for
  default configurations, close with a pointer to hybrid
  composition as the default mitigation and note the underlying
  engine VD-DisplayId gap remains (low priority unless VD revived).
- **#72816** — RawKeyboard listener on Android emulator.
  **Basis:** signal-based — summary explicitly states "emulator-
  specific, not a Flutter bug; real devices with Bluetooth keyboards
  work correctly." Upstream Android emulator behavior.
  **Verification:** none within Flutter's scope; close as working-
  as-expected on real devices with a pointer to the emulator
  behavior being upstream.
- **#155081** — FlutterEngineSendKeyEvent in GLFW embedder.
  **Basis:** signal-based — team-stated: GLFW embedder is unmaintained,
  no fix planned. Custom embedder path, not a Flutter-shipped
  platform. **Verification:** none; close as out-of-scope.
- **#155089** — Cmd+Enter on Chrome (macOS) treats Enter as held.
  **Basis:** signal-based — identified as upstream browser/OS bug
  (macOS/Safari doesn't send keyup for Enter when Meta held).
  Chromium tracker https://issues.chromium.org/issues/366284864
  filed. Flutter-side 100ms-timeout workaround exists.
  **Verification:** none within Flutter's scope; close as upstream
  issue.

## Cross-category sibling / split-issue links

- **#184744 (this category)** ↔ **#98720 (IME/CJK)** — same embedder-level
  root cause in `KeyEmbedderResponder.java`. #184744 was filed by
  @gnprice as an explicit split for the Gboard variant; #98720 keeps the
  Samsung Keyboard history. Any fix lands in one place and covers both.
  Revisit when #184744 is processed in this cleanup pass.

## Skipped — engine-level

_None identified yet._
