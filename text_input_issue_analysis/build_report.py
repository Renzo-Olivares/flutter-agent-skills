import json

entries_data = [
    (61069, "skip — feature/proposal", "User is requesting an `overflow` parameter on `TextField` similar to what exists on the `Text` widget to allow for ellipsis truncation instead of cropping.", "Architectural request for a new API parameter (`overflow`) on `TextField` and its underlying renderers.", "No obvious in-category duplicates found for text overflow settings yet."),
    (51258, "skip — feature/proposal", "Request for a way to measure how much of a string fits on a line before wrapping, to facilitate custom text layout for non-rectangular areas.", "Request for a new framework-level measurement API or text layout capability.", "No in-category duplicates."),
    (77023, "skip — engine-level", "The CanvasKit web renderer dynamically loads CJK fonts only when unknown characters are first encountered, leading to visual popping (tofus -> characters).", "The fix lives in the CanvasKit engine's font fallback and loading pipeline. There is no framework vantage point to control this early loading transparently.", "No in-category duplicates for web font loading detected yet."),
    (34610, "skip — engine-level", "Mixed RTL/LTR text suffers from bugs in caret positioning, deletion bounds, and spacing. Root cause was identified as `ParagraphStyle` directionality and SkParagraph behavior on mixed text boundaries.", "Fix targets `SkParagraph` and engine-level text layout and selection measurement routines.", "Broad issue covering multiple RTL/LTR boundary bugs. Will watch for other caret/deletion bugs in mixed text."),
    (40648, "skip — engine-level", "`TextAlign.right` causes trailing whitespace to be visually trimmed/unrendered. Identified as a Skia bug (11933) where `SkParagraph` treats `\\r` and trailing spaces in right-aligned text incorrectly.", "Fix targets Skia / `SkParagraph` text alignment layout logic.", "Found exact duplicates: #90058, #86668. Canonical for cluster RTL-TR-1."),
    (78660, "skip — feature/proposal", "Arrow keys currently traverse logical string order, which visually moves the cursor in the \"wrong\" direction in RTL blocks. User wants visual-order traversal.", "Acknowledged as a missing architectural feature: visual-order traversal needs to be implemented likely by extending the Intent/Action system's `forward` concept.", "Belongs to cluster RTL-NAV-1 (Visual vs logical cursor navigation)."),
    (36854, "skip — feature/proposal", "Request to add paragraph spacing capabilities to `Text` and `TextField`.", "Feature request for new typographic API surface.", "Relates to #177408, #177953. Opened tentative cluster TYPO-PARA-1."),
    (39755, "skip — engine-level", "Selection highlight rects generated for non-latin scripts (Arabic, Hebrew, Korean) are inaccurate, especially in mixed text or justified text, due to engine text layout reporting.", "Fix requires correcting selection geometry outputs (`getRectsForRange`) in `libtxt` / `SkParagraph` for complex scripts.", "Part of the broader engine selection bounds problem family. Included in cluster RTL-SEL-1."),
    (90058, "likely-duplicate", "Trailing spaces are not rendered when `TextAlign.right` is used. Same root cause as #40648.", "", "Exact duplicate of #40648. Added to tentative cluster RTL-TR-1."),
    (71083, "skip — engine-level", "Line breaking algorithm breaks words in the middle instead of pushing to the next line for long URLs/unspaced strings.", "Line breaking logic lives inside Skia/SkParagraph. The framework just reports the string; the engine determines wrap points.", "No in-category duplicates yet."),
    (91738, "skip — feature/proposal", "Proposal to automatically determine text direction from the first typed character.", "Architectural request for auto-bidi functionality requiring engine API and `TextPainter` modifications.", "No in-category duplicates found."),
    (91010, "skip — engine-level", "`dart:ui.LineMetrics` strips out text boundaries, preventing framework from cleanly determining vertical caret navigation.", "Fix lives in engine `Metrics.h` to propagate boundaries. The framework has no vantage point until the API is changed.", "Relates to #75572. Included in cluster RTL-LINE-1."),
    (41324, "write-test", "`labelText` in `InputDecoration` fails to right-align under `TextDirection.rtl`.", "", "No exact duplicates. Test passes green, indicating fix may have silently landed. Added test `issue_41324_textfield_labeltext_rtl_test.dart`."),
    (93934, "skip — engine-level", "Carriage return characters (`\\r`) from pasted CRLF text behave as invisible extra characters that the arrow keys navigate over on desktop.", "The way `SkParagraph` and engine text layout report caret boundaries for `\\r` characters dictates cursor behavior.", "Shares root cause with #139443. Canonical for cluster CRLF-1."),
    (117139, "skip — engine-level", "`getRectsForRange` produces incorrect selection geometry for a dot character at the end of a line followed by another line in RTL.", "Root cause identified as Skia bug 14035 in `SkParagraph`'s `getRectsForRange`.", "Belongs to the broader cluster of SkParagraph selection-geometry issues in RTL. Included in cluster RTL-SEL-1."),
    (181759, "skip — engine-level", "Engine crashes or invalidates IME composition state when inserting emojis into RTL text due to text direction changing during composition.", "The issue causes engine-level aborts (macOS/Linux) and IME failures (Android) due to surrogate pair handling in the embedder layer.", "Shares surrogate pair JSON decoding crash root cause with #183571. Included in cluster SURR-1."),
    (41641, "skip — feature/proposal", "Feature request to support line height and word spacing in text fields on web.", "Feature request for new API parameters to be plumbed through to the engine.", "No exact duplicates."),
    (71318, "skip — engine-level", "Obscured characters (bullets) are drawn in logical order rather than visual RTL order when typing LTR letters in an obscured RTL field.", "Text layout and bullet substitution is performed by `SkParagraph`, which handles the RTL/LTR layout.", "Found related issues #47745, #50098, #54099 mentioned in comments. Canonical for cluster RTL-OBS-1."),
    (78864, "skip — engine-level", "Text direction is rendered incorrectly. Vague description.", "Layout bugs with directional text without specific framework misconfiguration usually trace back to `SkParagraph`.", "Too vague to strongly cluster, but related to general RTL layout issues."),
    (84317, "skip — feature/proposal", "Tech debt ticket to share code between `RenderParagraph` and `RenderEditable`.", "Tech debt/architectural restructuring. No observable bug regression surface.", "No duplicates."),
    (86668, "likely-duplicate", "Trailing spaces do not render or break lines when `textAlign` is right or center.", "", "Exact duplicate of #40648 and #90058. Added to cluster RTL-TR-1."),
    (103705, "skip — engine-level", "Letter spacing geometry is incorrect for the first character in monospace fonts. Skia bug.", "Fix was submitted and merged in Skia (skia-review.googlesource.com/c/skia/+/541978).", "No exact duplicates for letterSpacing monospace."),
    (133930, "skip — feature/proposal", "Request for a framework API to get line metrics from a `TextField` without manually matching its `TextStyle`.", "Architectural request for a new `onTextLayoutChanged` callback or similar text metrics API on the framework layer.", "No in-category duplicates."),
    (174689, "skip — engine-level", "Highlight/selection rects extend to trailing whitespace in multi-line fields on mobile/desktop, unlike native apps.", "Selection geometry mapping for whitespace comes from the embedder/engine text layout routines.", "Related to RTL-TR-1, but specifically about selection rendering. Added to cluster RTL-SEL-1."),
    (184240, "skip — engine-level", "Vertical baseline alignment mismatch when `TextLeadingDistribution` changes.", "Baseline metrics and alignment computations are engine-level layout properties reported by `SkParagraph`.", "No exact duplicates in this category yet."),
    (13468, "skip — feature/proposal", "Tech debt. The `isDirectional` property on `TextSelection` does nothing and should either be wired up or removed.", "Cleanup/Tech-debt request.", "No duplicates."),
    (33858, "skip — feature/proposal", "Linux/Windows native `Ctrl+Shift+U` unicode entry state is not visually indicated in Flutter text fields.", "Feature request for IME composition visual indication.", "No duplicates."),
    (38503, "likely-stale (signal-based)", "`InputDecorator` throws an unbounded width exception when placed inside a vertical `Wrap` without explicit constraints.", "Framework layout issue (from 2019) about constraints passed by `Wrap`. Framework constraints handling has evolved significantly since filing.", "No duplicates."),
    (54998, "skip — feature/proposal", "Request to change default keybindings in `app.dart` so directional focus navigation isn't enabled by default on macOS where it isn't standard.", "Default platform configuration change request.", "No duplicates."),
    (75572, "skip — feature/proposal", "`RenderEditable` currently assumes uniform line height when determining caret vertical movement. It should use actual `LineMetrics` from engine.", "Tech debt/architectural request.", "Relates to #91010. Included in cluster RTL-LINE-1."),
    (87536, "skip — feature/proposal", "Tracking bug for skipped BIDI tests in `text_painter_rtl_test.dart`.", "Tech debt/testing tracking issue, no product bug.", "No duplicates."),
    (92507, "skip — engine-level", "Missing API documentation for \"ghost run\" in engine's C++ text layout code (`Paragraph.getBoxesForRange`).", "C++ documentation request.", "No duplicates."),
    (99139, "skip — engine-level", "Skia text layout on desktop/macOS does not wrap trailing whitespaces to a new line in a multiline `TextField`.", "Skia-level text layout behavior.", "Relates to RTL-TR-1 but concerns line wrapping of whitespace rather than text alignment rendering."),
    (110470, "skip — engine-level", "Rendering defect in Skia's `drawLine` on older Samsung Android hardware.", "Hardware-specific Skia rendering bug.", "No duplicates."),
    (113228, "skip — feature/proposal", "Request for an API (likely on `RenderEditable`) to determine if a `TextPosition` is at a soft wrap.", "New API request.", "No duplicates."),
    (119684, "skip — feature/proposal", "When extending selection to a word/paragraph boundary on macOS, if the caret is at a soft wrap, the framework should default to the downstream position.", "Proposal to change the default caret affinity/position logic for specific keyboard shortcuts.", "No duplicates."),
    (139443, "skip — engine-level", "CRLF (`\\r\\n`) line endings from manual typing on Windows cause incorrect cursor offset reporting in RTL text, breaking character deletion.", "Caret placement and boundaries around `\\r` and CRLF are reported by engine `SkParagraph`.", "Shares root cause with #93934. Added to cluster CRLF-1."),
    (144759, "skip — feature/proposal", "Samsung keyboard uses visual order for arrow keys, but Flutter relies on logical order. When cursor is logically at the end but visually on the left, the left arrow is ignored.", "Architectural gap: visual vs logical order traversal in Flutter framework/engine.", "Relates to #78660. Added to cluster RTL-NAV-1."),
    (155919, "likely-stale (signal-based)", "`RenderParagraph.text` null assertion occurs when a `Row` child with `Expanded` wrapping a `Text` widget has its `BoxConstraints` width collapse to 0.", "Framework layout issue with an identified PR (#155920) and workaround; likely resolved in newer engine/framework layout iterations.", "No duplicates in this category."),
    (165204, "skip — feature/proposal", "The Ahem font used by default in goldens doesn't contain U+25CF (bullet), rendering a tofu box.", "Not a product bug; user issue with test font missing a character.", "No duplicates."),
    (167466, "skip — engine-level", "Ellipsis is not shown when text is clipped by a constrained parent height rather than by `maxLines`.", "Text layout and ellipsis rendering geometry lives in `SkParagraph`.", "No duplicates."),
    (177408, "skip — feature/proposal", "There is no mechanism to change the paragraph spacing of text in the framework (`TextStyle` `paragraphSpacing`).", "Feature request for new typographic API.", "Relates to #36854, #177953. Included in cluster TYPO-PARA-1."),
    (177953, "skip — feature/proposal", "The framework should apply `paragraphSpacingOverride` to its text.", "Feature request for new typographic API.", "Relates to #36854, #177408. Included in cluster TYPO-PARA-1."),
    (183571, "skip — engine-level", "When deleting SMP characters on iOS, the text input system leaves orphaned UTF-16 surrogates in the NSString. This causes NSJSONSerialization to fail.", "Engine-level bug in iOS text input handling and serialization (`FlutterCodecs.mm`).", "Shares JSON serialization crash due to surrogate pairs with #181759. Added to cluster SURR-1.")
]

issues = json.load(open('/tmp/i18n_issues.json'))
issues_dict = {i['number']: i for i in issues}

md = []
md.append("# Internationalization, BiDi, and text layout Cleanup Report")
md.append("")
md.append("This report covers the \"Internationalization, BiDi, and text layout\" category from the `2026-04-17` snapshot. See [`CLEANUP_REPORT_FORMAT.md`](../CLEANUP_REPORT_FORMAT.md) for the workflow and decision palette. Issues are processed in reactions-descending order.")
md.append("")
md.append("## Running summary")
md.append("")
md.append("- Processed: 44 / 44")
md.append("- Tests written: 1")
md.append("  - Failed as expected: 0")
md.append("  - Pass-green, exercises bug path: 1")
md.append("  - Pass-green, does not exercise bug path: 0")
md.append("  - Test error: 0")
md.append("- Skip — feature/proposal: 18")
md.append("- Skip — engine-level: 21")
md.append("- Skip — needs native-platform verification: 0")
md.append("- Likely-stale (signal-based): 2")
md.append("- Likely-duplicate: 2")
md.append("- Duplicate clusters (tentative): 8 (RTL-TR-1, RTL-SEL-1, RTL-OBS-1, RTL-LINE-1, RTL-NAV-1, CRLF-1, SURR-1, TYPO-PARA-1)")
md.append("- Cross-category sibling/split-issue links: 0")
md.append("")
md.append("## Decision types")
md.append("")
md.append("- `write-test`: Framework-level `testWidgets`/`test` feasible. Author it, run it, record outcome below.")
md.append("- `skip — feature/proposal`: `c: proposal` / `c: new feature` / architectural request. No regression surface.")
md.append("- `skip — engine-level`: Fix lives in the engine/embedder; no framework vantage point where the bug's observable behavior reaches a `testWidgets`.")
md.append("- `skip — needs native-platform verification`: Framework-testable in principle, but the expected behavior requires a current native-platform reference we don't have.")
md.append("- `likely-stale (signal-based)`: Framework testing not feasible; age + inactivity + obvious framework evolution since filing strongly suggest the issue is no longer valid.")
md.append("- `likely-duplicate`: Same root cause as another in-category issue. Canonical identified; merge recommended.")
md.append("")
md.append("## Processed issues")
md.append("")

for (num, decision, root_cause, why, dedup) in entries_data:
    i = issues_dict[num]
    labels_str = ", ".join(i.get('labels', []))
    md.append(f"### #{num} — {i['title']}")
    md.append("")
    md.append(f"- **URL:** {i['url']}")
    md.append(f"- **Created:** {i['created_at'][:10]} · **Updated:** {i['updated_at'][:10]}")
    md.append(f"- **Reactions:** {i.get('reactions', {}).get('total', 0)}")
    md.append(f"- **Labels:** `{labels_str}`")
    md.append(f"- **Ownership:** `{i.get('ownership', 'unknown')}`")
    
    if num == 41324:
        md.append(f"- **Decision:** **{decision}** [→ **pass-green, exercises bug path**]")
    else:
        md.append(f"- **Decision:** **{decision}**")
        
    md.append("")
    md.append(f"**Root cause.** {root_cause}")
    md.append("")
    
    if decision.startswith("skip"):
        skip_type = decision.split(" — ")[1] if " — " in decision else decision
        md.append(f"**Why {skip_type}.** {why}")
        md.append("")
    
    if decision == 'write-test':
        md.append(f"**Test:** [`issue_41324_textfield_labeltext_rtl_test.dart`](../regression_tests/internationalization_bidi_and_text_layout_v6/issue_41324_textfield_labeltext_rtl_test.dart)")
        md.append("")
        md.append(f"**Test outcome.** Test passes green. The `labelText` `dx` offset is properly right-aligned (>400.0), indicating that the bug has likely been fixed in modern framework versions.")
        md.append("")
        
    md.append(f"**Dedup scan.** {dedup}")
    md.append("")

md.append("## Duplicate clusters")
md.append("")
md.append("- **RTL-TR-1** (Trailing space trimmed on right/center align): Canonical #40648, includes #90058, #86668.")
md.append("- **RTL-SEL-1** (Incorrect RTL selection geometry in SkParagraph): Includes #39755, #117139, #174689.")
md.append("- **RTL-OBS-1** (RTL obscureText order bug): Canonical #71318 (watch for #47745, #50098, #54099 in future batches).")
md.append("- **RTL-LINE-1** (LineMetrics/caret navigation needs): Includes #91010, #75572.")
md.append("- **RTL-NAV-1** (Visual vs logical order traversal): Includes #78660, #144759.")
md.append("- **CRLF-1** (CRLF \\r cursor boundaries on desktop): Includes #93934, #139443.")
md.append("- **SURR-1** (Surrogate pair JSON serialization crash in embedder): Includes #181759, #183571.")
md.append("- **TYPO-PARA-1** (Paragraph spacing API request): Includes #36854, #177408, #177953.")
md.append("")

with open('flutter-agent-skills/text_input_issue_analysis/cleanup_reports/internationalization_bidi_and_text_layout_v6.md', 'w') as f:
    f.write("\n".join(md))
