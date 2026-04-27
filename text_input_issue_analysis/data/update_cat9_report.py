import re

file_path = 'flutter-agent-skills/text_input_issue_analysis/cleanup_reports/internationalization_bidi_and_text_layout.md'
with open(file_path, 'r') as f:
    content = f.read()

content = content.replace('- Processed: 4 / 44', '- Processed: 5 / 44')
content = content.replace('- Skip — engine-level: 2', '- Skip — engine-level: 3')

entry = """### #40648 — Trailing space doesn't work with TextField with TextAlign.right 

- **URL:** https://github.com/flutter/flutter/issues/40648
- **Created:** 2019-09-17 (~6.5 y old) · **Updated:** 2025-01-29
- **Reactions:** 16
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.5`, `found in release: 2.6`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — engine-level**

**Root cause.** Trailing spaces are visually trimmed or fail to render the cursor advancement when a `TextField` is set to `TextAlign.right`. This happens because `SkParagraph` drops or mishandles trailing whitespace width in right-aligned contexts.

**Why skip-engine / Test approach.** A corresponding Skia bug (issue 11933) confirms the root cause lives in `SkParagraph` layout algorithms. The framework merely passes `TextAlign.right` to the engine, which incorrectly computes the cursor or line width. This cannot be fixed or isolated with a framework test.

**Dedup scan.** Scanned for "TextAlign.right", "trailing space", "whitespace". Found #90058 ("TextFormField with textAlign: TextAlign.right whitespace doesn't show unless text is entered"), which is a clear duplicate. 

"""

content = content.replace('## Processed issues\n', '## Processed issues\n\n' + entry)
content = content.replace('## Skipped — engine-level\n', '## Skipped — engine-level\n- #40648 (Trailing space does not work with TextAlign.right)\n')

with open(file_path, 'w') as f:
    f.write(content)

print('Updated report for #40648.')
