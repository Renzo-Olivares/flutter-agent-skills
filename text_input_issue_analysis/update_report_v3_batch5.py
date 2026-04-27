import re

report_path = 'cleanup_reports/internationalization_bidi_and_text_layout_v3.md'
with open(report_path, 'r') as f:
    content = f.read()

entries = """
### #165204 — Unicode characters not being rendered correctly in goldens test

- **URL:** https://github.com/flutter/flutter/issues/165204
- **Created:** 2025-03-14 (~0.1 y old) · **Updated:** 2025-03-27
- **Reactions:** 0 ()
- **Labels:** `a: tests`, `a: text input`, `framework`, `has reproducible steps`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** The `Ahem` font used by default in `matchesGoldenFile` does not include the `U+25CF` bullet character, rendering it as a tofu box.

**Why skip-proposal.** This is the expected behavior of the `Ahem` test font. Developers must explicitly load a font that supports the character if they want to render it in golden tests.

**Dedup scan.**
  - **Terms / scope:** "goldens test", "Unicode characters", "Ahem"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #167466 — Ellipsis not working properly when a text overflows via constrained height instead of max lines

- **URL:** https://github.com/flutter/flutter/issues/167466
- **Created:** 2025-04-21 (~0.0 y old) · **Updated:** 2025-12-21
- **Reactions:** 0 ()
- **Labels:** `framework`, `a: typography`, `c: rendering`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Ellipsis is triggered by `maxLines` or maximum width constraints within `TextPainter`. If the text overflows because the parent `Container`'s height is constrained, `TextPainter` does not know to insert an ellipsis because the layout algorithm processes line-by-line width, not aggregate height bounds.

**Why skip-engine.** Modifying `TextPainter` or the underlying `SkParagraph` layout algorithm to support truncation by block height is an engine-level feature request / text-layout architectural change.

**Dedup scan.**
  - **Terms / scope:** "Ellipsis", "constrained height", "overflows"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #177408 — The framework should provide a mechanism to change the paragraph spacing of text

- **URL:** https://github.com/flutter/flutter/issues/177408
- **Created:** 2025-10-22 (~0.5 y old) · **Updated:** 2026-01-06
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `c: new feature`, `a: accessibility`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Request to add `paragraphSpacing` to `TextStyle` to control the space between paragraphs separated by `\\n`.

**Why skip-proposal.** Feature proposal for text styling.

**Dedup scan.**
  - **Terms / scope:** "paragraph spacing", "paragraphSpacing"
  - **Hits, classified:** 
    - **adjacent-different:** #36854 (Setting paragraph distance in Text and TextField). Very similar proposal, but distinct issues tracking the same request.
  - **Cluster decision:** none

### #177953 — The framework should apply `paragraphSpacingOverride` to its text

- **URL:** https://github.com/flutter/flutter/issues/177953
- **Created:** 2025-11-03 (~0.4 y old) · **Updated:** 2026-01-02
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `c: new feature`, `a: accessibility`, `platform-web`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Request to apply the existing `MediaQueryData.paragraphSpacingOverride` to the framework's internal text components to meet WCAG standards out of the box.

**Why skip-proposal.** Feature parity / accessibility integration request.

**Dedup scan.**
  - **Terms / scope:** "paragraphSpacingOverride", "WCAG"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #183571 — iOS: NSJSONSerialization crash when deleting SMP characters

- **URL:** https://github.com/flutter/flutter/issues/183571
- **Created:** 2026-03-12 (~0.1 y old) · **Updated:** 2026-03-19
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `platform-ios`, `P1`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Deleting Supplementary Multilingual Plane (SMP) characters on iOS leaves orphaned UTF-16 surrogates, causing `NSJSONSerialization` to crash the app via `FlutterCodecs.mm`.

**Why skip-engine.** This is an embedder/engine crash in the iOS `FlutterCodecs.mm` layer when communicating with the framework.

**Dedup scan.**
  - **Terms / scope:** "NSJSONSerialization crash", "SMP characters", "UTF-16 surrogates"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

"""

# update counters
content = re.sub(r'Processed: 39 \/ 44', 'Processed: 44 / 44', content)

# update process issues
content = content.replace('## Duplicate clusters\n', entries + '\n## Duplicate clusters\n')

# add to skip engine
skip_engine = """- #167466 — TextPainter layout ellipsis by height constraint limits
- #183571 — iOS embedder NSJSONSerialization surrogate pair crash
"""
content = content.replace('## Skipped — engine-level\n', '## Skipped — engine-level\n' + skip_engine)

with open(report_path, 'w') as f:
    f.write(content)
