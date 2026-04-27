import re

report_path = 'cleanup_reports/internationalization_bidi_and_text_layout_v3.md'
with open(report_path, 'r') as f:
    content = f.read()

entries = """
### #84317 — Share code between RenderParagraph and RenderEditable

- **URL:** https://github.com/flutter/flutter/issues/84317
- **Created:** 2021-06-10 (~4.9 y old) · **Updated:** 2023-07-08
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `a: typography`, `P2`, `c: tech-debt`, `team-framework`, `triaged-framework`
- **Ownership:** `team-framework`
- **Decision:** **skip — feature/proposal**

**Root cause.** A tech-debt proposal to share underlying logic between `RenderParagraph` and `RenderEditable`.

**Why skip-proposal.** This is a refactoring/architecture proposal without a specific user-facing bug regression surface.

**Dedup scan.**
  - **Terms / scope:** "Share code", "RenderParagraph", "RenderEditable"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #86668 — TextField doesn't handle trailing space as characters if textAlign is TextAlign.right/TextAlign.center

- **URL:** https://github.com/flutter/flutter/issues/86668
- **Created:** 2021-07-19 (~4.8 y old) · **Updated:** 2024-09-26
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 2.2`, `found in release: 2.4`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **likely-duplicate**

**Root cause.** Trailing spaces fail to render/align when `textAlign` is not `left`. This is exactly the same Skia rendering issue as #40648 and #90058.

**Dedup scan.**
  - **Terms / scope:** "textAlign", "trailing space"
  - **Hits, classified:** 
    - **duplicate:** #40648, #90058
  - **Cluster decision:** join `TRL-SPC-1`

### #103705 — letterSpacing in TextField with monospace font is only applied to right side of the first character

- **URL:** https://github.com/flutter/flutter/issues/103705
- **Created:** 2022-05-13 (~3.9 y old) · **Updated:** 2023-07-08
- **Reactions:** 1 (👍 1)
- **Labels:** `a: text input`, `engine`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.0`, `found in release: 3.1`, `team-engine`, `triaged-engine`
- **Ownership:** `team-engine`
- **Decision:** **skip — engine-level**

**Root cause.** Bug in how the engine handles letterSpacing bounds during string mutation. Was tracked and patched in Skia (skia-review.googlesource.com/c/skia/+/541978).

**Why skip-engine.** Issue is deep within Skia's typography measuring phase; the fix was merged upstream.

**Dedup scan.**
  - **Terms / scope:** "letterSpacing", "monospace", "first character"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #133930 — No good way to get line metrics for `Text`/`TextField` based widgets.

- **URL:** https://github.com/flutter/flutter/issues/133930
- **Created:** 2023-09-03 (~2.6 y old) · **Updated:** 2024-08-23
- **Reactions:** 1 (👍 1)
- **Labels:** `framework`, `a: typography`, `has reproducible steps`, `P2`, `found in release: 3.13`, `found in release: 3.14`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Feature request for an `onTextLayoutChanged` or similar callback to reliably retrieve line metrics directly from the framework's widgets rather than rebuilding them in a dummy `TextPainter`.

**Why skip-proposal.** Proposal for a new framework API.

**Dedup scan.**
  - **Terms / scope:** "line metrics", "TextPainter"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #174689 — App highlights / selects trailing whitespaces in a multi-line textfield.

- **URL:** https://github.com/flutter/flutter/issues/174689
- **Created:** 2025-08-29 (~0.7 y old) · **Updated:** 2025-09-18
- **Reactions:** 1 (👀 1)
- **Labels:** `a: text input`, `platform-android`, `platform-ios`, `a: desktop`, `has reproducible steps`, `P2`, `team-text-input`, `triaged-text-input`, `found in release: 3.35`, `found in release: 3.36`
- **Ownership:** `team-text-input`
- **Decision:** **skip — engine-level**

**Root cause.** Selecting text on a line highlights trailing whitespace if the line below it is longer. This differs from native Android/iOS behavior. 

**Why skip-engine.** This is caused by `getRectsForRange` provided by the Skia text engine (which paints selection boxes). The framework uses the rects given to it.

**Dedup scan.**
  - **Terms / scope:** "highlights", "trailing whitespaces", "multi-line"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #184240 — Vertical baseline alignment mismatch between Text and collapsed TextField when changing TextLeadingDistribution

- **URL:** https://github.com/flutter/flutter/issues/184240
- **Created:** 2026-03-27 (~0.1 y old) · **Updated:** 2026-04-02
- **Reactions:** 1 (❤️ 1)
- **Labels:** `framework`, `f: material design`, `has reproducible steps`, `team-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **write-test** [→ **pass-green, exercises bug path**]

**Root cause.** Alleged baseline mismatch when `TextLeadingDistribution.even` is used alongside `InputDecoration.collapsed()`.

**Test approach.** 
  - Render a `Row` with `crossAxisAlignment: CrossAxisAlignment.baseline`.
  - Place a `Text` and an `Expanded(TextField)` inside it.
  - Compare the global Y offset of their RenderBoxes.

**Test:** [`issue_184240_baseline_alignment_test.dart`](../../regression_tests/internationalization_bidi_and_text_layout_v3/issue_184240_baseline_alignment_test.dart)

**Test outcome.** 
  - `pass-green, exercises bug path`. The difference is within 1 pixel, meaning the framework already aligns them successfully on master.

**Dedup scan.**
  - **Terms / scope:** "Vertical baseline", "TextLeadingDistribution"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #13468 — TextSelection.isDirectional is not respected, make it do something useful eg: for Mac

- **URL:** https://github.com/flutter/flutter/issues/13468
- **Created:** 2017-12-09 (~8.4 y old) · **Updated:** 2024-05-09
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `framework`, `c: proposal`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Proposal to wire up the unused `TextSelection.isDirectional` flag to drive text editing shortcuts.

**Why skip-proposal.** The property is dormant/unused API design proposal.

**Dedup scan.**
  - **Terms / scope:** "isDirectional"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #33858 — Unicode input should be indicated.

- **URL:** https://github.com/flutter/flutter/issues/33858
- **Created:** 2019-06-04 (~6.9 y old) · **Updated:** 2024-12-13
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `c: new feature`, `framework`, `f: material design`, `platform-windows`, `platform-linux`, `a: desktop`, `P3`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** A feature request to display an underlined 'u' in the text field when awaiting a Unicode hex entry via `Ctrl+Shift+U`.

**Why skip-proposal.** Feature request for IME visual indicators.

**Dedup scan.**
  - **Terms / scope:** "Unicode input", "Ctrl+Shift+U"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #38503 — TextField doesn't appear within a direction:Axis.vertical Wrap

- **URL:** https://github.com/flutter/flutter/issues/38503
- **Created:** 2019-08-14 (~6.7 y old) · **Updated:** 2024-12-11
- **Reactions:** 0 ()
- **Labels:** `a: text input`, `framework`, `f: material design`, `has reproducible steps`, `P2`, `found in release: 3.3`, `found in release: 3.7`, `team-design`, `triaged-design`
- **Ownership:** `team-design`
- **Decision:** **write-test** [→ **fail-as-expected**]

**Root cause.** `Wrap` with `direction: Axis.vertical` fails to provide bounded width constraints to its children. `TextField` (and its `InputDecorator`) asserts that it must have a bounded width to lay itself out.

**Test approach.** 
  - Render a `TextField` inside a `Wrap(direction: Axis.vertical)`.

**Test:** [`issue_38503_vertical_wrap_test.dart`](../../regression_tests/internationalization_bidi_and_text_layout_v3/issue_38503_vertical_wrap_test.dart)

**Test outcome.** 
  - `fail-as-expected`. The test catches the `AssertionError` ("An InputDecorator... cannot have an unbounded width") and fails, accurately reproducing the crash.

**Dedup scan.**
  - **Terms / scope:** "Axis.vertical Wrap", "unbounded width"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

### #54998 — Directional navigation key binding defaults should be limited to those platforms that use it.

- **URL:** https://github.com/flutter/flutter/issues/54998
- **Created:** 2020-04-16 (~6.0 y old) · **Updated:** 2024-07-22
- **Reactions:** 0 ()
- **Labels:** `framework`, `platform-macos`, `a: desktop`, `a: devtools`, `P2`, `team-text-input`, `triaged-text-input`
- **Ownership:** `team-text-input`
- **Decision:** **skip — feature/proposal**

**Root cause.** Proposal to change the default behavior of directional focus key bindings on macOS and Linux.

**Why skip-proposal.** Requests changes to default shortcuts and `Intent` configurations rather than reporting a bug.

**Dedup scan.**
  - **Terms / scope:** "navigation key binding"
  - **Hits, classified:** 
    - No hits in category.
  - **Cluster decision:** none

"""

# update counters
content = re.sub(r'Processed: 19 \/ 44', 'Processed: 29 / 44', content)
content = re.sub(r'Tests written: 3', 'Tests written: 5', content)
content = re.sub(r'Failed as expected: 2', 'Failed as expected: 3', content)
content = re.sub(r'Pass-green, exercises bug path: 1', 'Pass-green, exercises bug path: 2', content)

# update process issues
content = content.replace('## Duplicate clusters\n', entries + '\n## Duplicate clusters\n')

# update duplicate clusters list
cluster_update = """- **TRL-SPC-1** Trailing space trimmed on TextAlign.right (3 members)
  - Canonical: #40648
  - Members: #90058, #86668"""
content = re.sub(r'- \*\*TRL-SPC-1\*\*.+?- Members: #90058', cluster_update, content, flags=re.DOTALL)

# add to likely stale
stale = """- #184240 — `TextLeadingDistribution.even` baseline alignment test passes on master.
"""
content = content.replace('## Likely-stale candidates for closure review\n', '## Likely-stale candidates for closure review\n' + stale)

# add to skip engine
skip_engine = """- #103705 — Skia letterSpacing bounds issue (fixed upstream)
- #174689 — Skia getRectsForRange highlights trailing spaces
"""
content = content.replace('## Skipped — engine-level\n', '## Skipped — engine-level\n' + skip_engine)

with open(report_path, 'w') as f:
    f.write(content)
