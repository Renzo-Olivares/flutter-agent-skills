import re

report_path = 'cleanup_reports/internationalization_bidi_and_text_layout_v3.md'
with open(report_path, 'r') as f:
    content = f.read()

entries = """
### #75572 — Let RenderEditable use LineMetrics instead of assuming every line has the same height

- **URL:** https://github.com/flutter/flutter/issues/75572
- **Created:** 2021-02-07 (~5.2 y old) · **Updated:** 2026-03-05
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `framework`, `f: material design`, `P2`, `c: tech-debt`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal**

**Root cause.** Tech-debt ticket to remove hardcoded line height assumptions in RenderEditable and instead query LineMetrics.

**Why skip-proposal.** This is an architectural tech-debt tracker.

**Dedup scan.**
  - **Terms / scope:** "RenderEditable", "LineMetrics", "same height"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #87536 — BIDI text painting skipped tests.

- **URL:** https://github.com/flutter/flutter/issues/87536
- **Created:** 2021-08-03 (~4.7 y old) · **Updated:** 2023-07-08
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `c: contributor-productivity`, `framework`, `a: internationalization`, `P2`, `c: tech-debt`, `team: skip-test`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** A tracker to review and un-skip tests in `text_painter_rtl_test.dart`.

**Why skip-proposal.** Tracking issue for skipped tests.

**Dedup scan.**
  - **Terms / scope:** "skipped tests", "BIDI text painting"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #92507 — Document "ghost run" and its interaction with `Paragraph.getBoxesForRange`

- **URL:** https://github.com/flutter/flutter/issues/92507
- **Created:** 2021-10-26 (~4.5 y old) · **Updated:** 2023-08-04
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `engine`, `d: api docs`, `a: typography`, `P2`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — feature/proposal**

**Root cause.** Missing API documentation for Skia's concept of a "ghost run" in text layout metrics.

**Why skip-proposal.** Documentation request for engine behavior.

**Dedup scan.**
  - **Terms / scope:** "ghost run", "getBoxesForRange"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #99139 — [MacOS] Trailing whitespace in multiline TextField overflows and doesn't go to newline.

- **URL:** https://github.com/flutter/flutter/issues/99139
- **Created:** 2022-02-25 (~4.2 y old) · **Updated:** 2024-06-20
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `framework`, `f: material design`, `a: desktop`, `has reproducible steps`, `P2`, `found in release: 2.10`, `found in release: 2.11`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** On Desktop platforms, Skia text layout does not automatically wrap trailing whitespaces in multiline fields to a new line, matching some native desktop behavior but frustrating code-editor developers.

**Why skip-engine.** This text wrapping and boundary behavior is controlled by the engine's text layout implementation. 

**Dedup scan.**
  - **Terms / scope:** "Trailing whitespace", "multiline TextField", "MacOS"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #110470 — canvas.drawLine() does not paint correctly on Samsung Galaxy Note 20 Ultra

- **URL:** https://github.com/flutter/flutter/issues/110470
- **Created:** 2022-08-29 (~3.6 y old) · **Updated:** 2024-09-26
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `e: device-specific`, `platform-android`, `framework`, `engine`, `f: material design`, `dependency: skia`, `c: rendering`, `P2`, `e: samsung`, `team-android`, `triaged-android`
- **Ownership:** `team-android`
- **Decision:** **skip — engine-level**

**Root cause.** Device-specific Skia rendering defect for `drawLine` on older Samsung hardware.

**Why skip-engine.** Engine/Skia GPU rendering issue.

**Dedup scan.**
  - **Terms / scope:** "drawLine()", "Samsung"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #113228 — Provide an API to detect if a TextPosition is located at a soft word wrap

- **URL:** https://github.com/flutter/flutter/issues/113228
- **Created:** 2022-10-10 (~3.5 y old) · **Updated:** 2024-03-06
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `c: new feature`, `platform-ios`, `framework`, `c: proposal`, `P3`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **skip — feature/proposal**

**Root cause.** Request for a new `RenderEditable` API to detect if a text position is at a soft wrap boundary, to control iOS toolbar toggling.

**Why skip-proposal.** Feature/API request.

**Dedup scan.**
  - **Terms / scope:** "soft word wrap", "TextPosition"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #119684 — Extending to paragraph/or word boundary on MacOS should default to the `downstream` position when at a word wrap

- **URL:** https://github.com/flutter/flutter/issues/119684
- **Created:** 2023-02-01 (~3.2 y old) · **Updated:** 2024-06-06
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `framework`, `platform-macos`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** macOS text selection shortcuts (shift+option+up/down) need to default to a downstream affinity when crossing a soft word wrap boundary.

**Why skip-proposal.** This relates to default text selection intent logic for macOS shortcuts, closer to a feature request / behavioral tweak than a testable regression without engine layout metrics.

**Dedup scan.**
  - **Terms / scope:** "downstream", "word wrap", "extend selection"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #139443 — [Windows] Incorrect character deletion in right-to-left texts

- **URL:** https://github.com/flutter/flutter/issues/139443
- **Created:** 2023-12-03 (~2.4 y old) · **Updated:** 2025-08-21
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `platform-windows`, `has reproducible steps`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **write-test** [→ **fail-as-expected**]

**Root cause.** On Windows, manual typing generates CRLF line endings instead of LF. The framework's text selection endpoints return the incorrect visual offset for RTL text containing CRLF boundaries, causing backspace to delete the wrong visual character.

**Test approach.** 
  - Extract the visual X-offset of a collapsed text selection just after a CRLF (`\\r\\n`) in an RTL string.
  - Compare it to the visual X-offset of the same string using just LF (`\\n`).
  - Assert they are equal.

**Test:** [`issue_139443_crlf_rtl_test.dart`](../../regression_tests/internationalization_bidi_and_text_layout_v3/issue_139443_crlf_rtl_test.dart)

**Test outcome.** 
  - `fail-as-expected`. Expected `<747.0>`, actual `<795.0>`. The visual carets diverge because the framework misinterprets the `\\r` length during layout in an RTL context.

**Dedup scan.**
  - **Terms / scope:** "deletion in right-to-left", "CRLF", "Windows RTL backspace"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #144759 — Arrow key navigation gets stuck at the end of RTL text using Samsung Keyboard

- **URL:** https://github.com/flutter/flutter/issues/144759
- **Created:** 2024-03-07 (~2.1 y old) · **Updated:** 2024-03-07
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `framework`, `a: internationalization`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — needs native-platform verification**

**Root cause.** Samsung Keyboard IME on Android ignores the left-arrow key if the cursor is at the visual left edge of the text field. However, Flutter traverses RTL text logically (where the logical start is at the visual right), meaning the framework waits for a key event it never receives.

**Why skip-native.** The core problem relies on the native IME (Samsung Keyboard specifically) consuming/ignoring arrow key inputs before they hit the Flutter engine. Simulating this requires an Android integration test with that specific OEM keyboard.

**Dedup scan.**
  - **Terms / scope:** "Arrow key navigation", "Samsung Keyboard", "stuck at the end"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #155919 — Error where possible null is being asserted in rendering paragraph

- **URL:** https://github.com/flutter/flutter/issues/155919
- **Created:** 2024-09-30 (~1.6 y old) · **Updated:** 2024-10-23
- **Reactions:** 0 ()
- **Labels:** `framework`, `a: error message`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **write-test** [→ **pass-green, exercises bug path**]

**Root cause.** Pumping a `Text` widget inside an un-expanded `Row` child that is forcibly squished to zero width (`BoxConstraints` 0) previously caused a null assertion in `RenderParagraph`.

**Test approach.** 
  - Render a `SizedBox(width: 0)` containing a `Row` with one `Expanded(child: Text())` and one unexpanded `Text()`.
  - Assert that no framework exceptions are thrown.

**Test:** [`issue_155919_squished_text_test.dart`](../../regression_tests/internationalization_bidi_and_text_layout_v3/issue_155919_squished_text_test.dart)

**Test outcome.** 
  - `pass-green, exercises bug path`. The test completes successfully without throwing an assertion. Likely fixed in an intervening layout patch.

**Dedup scan.**
  - **Terms / scope:** "null is being asserted", "rendering paragraph", "width 0"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

"""

# update counters
content = re.sub(r'Processed: 29 \/ 44', 'Processed: 39 / 44', content)
content = re.sub(r'Tests written: 5', 'Tests written: 7', content)
content = re.sub(r'Failed as expected: 3', 'Failed as expected: 4', content)
content = re.sub(r'Pass-green, exercises bug path: 2', 'Pass-green, exercises bug path: 3', content)

# update process issues
content = content.replace('## Duplicate clusters\n', entries + '\n## Duplicate clusters\n')

# add to likely stale
stale = """- #155919 — Squished `Text` widget null assertion passes without error on master.
"""
content = content.replace('## Likely-stale candidates for closure review\n', '## Likely-stale candidates for closure review\n' + stale)

# add to skip engine
skip_engine = """- #99139 — Skia macOS text layout trailing whitespace line break differences
- #110470 — Device-specific Skia drawLine defect on Samsung
"""
content = content.replace('## Skipped — engine-level\n', '## Skipped — engine-level\n' + skip_engine)

with open(report_path, 'w') as f:
    f.write(content)
