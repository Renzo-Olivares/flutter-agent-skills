import re

file_path = 'flutter-agent-skills/text_input_issue_analysis/cleanup_reports/internationalization_bidi_and_text_layout.md'
with open(file_path, 'r') as f:
    content = f.read()

# Update counters
content = content.replace('- Processed: 35 / 44', '- Processed: 44 / 44')
content = content.replace('- Tests written: 5', '- Tests written: 6')
content = content.replace('  - Pass-green, does not exercise bug path: 0', '  - Pass-green, does not exercise bug path: 1')
content = content.replace('- Skip — feature/proposal: 14', '- Skip — feature/proposal: 17')
content = content.replace('- Skip — engine-level: 11', '- Skip — engine-level: 15')
content = content.replace('- Skip — needs native-platform verification: 0', '- Skip — needs native-platform verification: 1')

entries = """### #119684 — Extending to paragraph/or word boundary on MacOS should default to the `downstream` position when at a word wrap

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

**Root cause.** Certain Unicode characters (like `\\u25CF`) render as tofu boxes in golden tests because the default test font (`Ahem`) does not include those glyphs.

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

"""

content = content.replace('## Processed issues\n', '## Processed issues\n\n' + entries)

# Add skip engine items
engine_items = """- #139443 ([Windows] Incorrect character deletion in right-to-left texts)
- #144759 (Arrow key navigation gets stuck at the end of RTL text using Samsung Keyboard)
- #167466 (Ellipsis not working properly when a text overflows via constrained height instead of max lines)
- #183571 (iOS: NSJSONSerialization crash when deleting SMP characters)
"""
content = content.replace('## Skipped — engine-level\n', '## Skipped — engine-level\n' + engine_items)

with open(file_path, 'w') as f:
    f.write(content)

print('Updated report for final 9 issues (35 to 43).')
