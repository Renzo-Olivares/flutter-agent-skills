# Category Cleanup Report — Format and Workflow Specification

Portable spec for the per-category cleanup experiment — the process that
produces one `cleanup_reports/<category_slug>.md` file per taxonomy category
(see `text_input_taxonomy.json`) by auditing each issue for duplicates,
staleness, and regression-test feasibility.

Pair file: [`CATEGORY_PROFILE_FORMAT.md`](CATEGORY_PROFILE_FORMAT.md) covers
the read-only per-category statistics report. *This* document covers the
write-side audit that produces merge/close/test recommendations.

Use this spec when:

- Starting a cleanup report for a new category.
- Dispatching an agent (or running manually) to process issues in an
  existing category.
- Reviewing an in-progress cleanup report for consistency.
- Editing the workflow or the report shape — update this spec in the same
  commit so conventions stay locked.

## Inputs

For each issue the process needs:

1. **Structured snapshot fields** from `text_input_issues.json`:
   `number`, `title`, `url`, `created_at`, `updated_at`, `state`, `labels`,
   `assignees`, `ownership`, `body`, `comment_summary`, `reactions`,
   `category`.
2. **Raw comments** from `data/merged_raw.json` (`comments_raw`). The
   comment summary is the primary classification input, but raw comments
   must be consulted whenever the summary hints at platform/engine layer
   work — see convention **C1** below.
3. **The current taxonomy** (`text_input_taxonomy.json`) for category name
   and description, and **the full `text_input_issues.json` issue list** for
   intra-category dedup scans.

## Output

`cleanup_reports/<category_slug>.md` — one Markdown file per category.
Snake-case the category name (e.g. "IME, CJK composing, and dead keys/
accents" → `ime_cjk.md`).

When a regression test is authored, it is co-located with the category's
test bundle at
`regression_tests/<category_slug>/issue_<number>_<slug_of_title>_test.dart`.

## Per-issue workflow

Processed **one issue at a time**. Each iteration produces exactly one entry
appended to the report's "Processed issues" section and one update to the
running-summary counters.

1. **Fetch the issue.** Pull the structured snapshot fields + raw comments.
2. **Layer check (C1).** If the summary or body mentions `metaState`,
   `keycode`, a file path ending in `.java`/`.m`/`.mm`/`.cc`/`.h`/`.kt`, or
   named classes like `KeyEmbedderResponder` / `TextInputPlugin` /
   `KeyboardManager`, or platform-specific label phrases (e.g. "engine
   side", "embedder"), read the raw comments before classifying. Summary
   compression often strips the layer signal.
3. **Classify** into one of the decision types (see palette below).
4. **If `write-test`:**
   a. Draft a framework-level `testWidgets` or `test` that captures the
      observable failure mode.
   b. Place it at
      `regression_tests/<category_slug>/issue_<n>_<slug>_test.dart`.
   c. Run `flutter test <absolute path>`. Use absolute paths.
   d. Record the outcome in the entry (see field shape below).
5. **Dedup scan** — search *within the current category* for issues that
   share the root cause. The scan is symptom-and-terminology grep, not
   semantic clustering (see convention **C2** for scope).
6. **Write the entry** per the per-issue schema.
7. **Update running-summary counters** at the top of the report.
8. **If a related issue was noticed in a different category**, record it in
   the "Cross-category sibling / split-issue links" section but do **not**
   expand the dedup scan beyond the current category.

## Decision type palette

Every processed issue carries exactly one decision. The palette is closed
— do not invent new types without updating this spec.

| Decision | Meaning |
|---|---|
| `write-test` | Framework-level `testWidgets`/`test` feasible. Author it, run it, record outcome below. |
| `skip — feature/proposal` | `c: proposal` / `c: new feature` / architectural request. No regression surface. |
| `skip — engine-level` | Fix lives in the engine/embedder; no framework vantage point where the bug's observable behavior reaches a `testWidgets`. Write a framework-level gate only if it's useful as a future guard, and note it's orthogonal to the actual bug path. |
| `skip — needs native-platform verification` | Framework-testable in principle, but the *expected* behavior requires a current native-platform reference we don't have (e.g. iOS composing style in the current OS). Deferred pending that baseline. |
| `likely-stale (signal-based)` | Framework testing not feasible; age + inactivity + obvious framework evolution since filing strongly suggest the issue is no longer valid. |
| `likely-duplicate` | Same root cause as another in-category issue. Canonical identified; merge recommended. |

### `write-test` outcomes (sub-classification)

- `fail-as-expected` — test fails, confirming the bug is real and
  framework-observable.
- `pass-green, exercises bug path` — test passes; the test exercises the
  bug's code path. Strong likely-stale signal.
- `pass-green, does not exercise the real bug path` — test passes but the
  actual bug lives below the framework's vantage point (usually an
  embedder issue that got mis-classified before the layer-check finding).
  Retain the test as a framework-level regression gate, but the pass is
  *not* a staleness signal.
- `test-error` — could not run (compile failure, API mismatch, timeout).

## Report structure (top to bottom)

1. **Title** — `# <Category name> Cleanup Report`.
2. **Intro** — one paragraph: which category, snapshot source, link to this
   spec, link to the per-issue workflow.
3. **Running summary** — counters, updated after each processed issue:
   - `Processed: N / <category total>`
   - `Tests written: N`
     - `Failed as expected: N`
     - `Pass-green, exercises bug path: N`
     - `Pass-green, does not exercise bug path: N`
     - `Test error: N`
   - One line per other decision type with counts.
   - `Duplicate clusters (tentative): N (<short names>)`
   - `Cross-category sibling/split-issue links: N`
4. **Decision types** — the palette above restated concisely (the report's
   own readers need it without leaving the file).
5. **Processed issues** — append-only. `### #<number> — <title>`, one
   entry per issue. See per-issue schema below.
6. **Duplicate clusters** — named clusters (tight duplicates or shared-
   root-cause groupings). Each cluster gets a short code (`DK-1`, `WKI-1`,
   etc.) and lists canonical + members + coordination notes.
7. **Likely-stale candidates for closure review** — any issue whose
   decision or test outcome suggests it may no longer be valid.
   Consolidates both signal-based stale flags and test-pass-exercises-bug-
   path cases.
8. **Cross-category sibling / split-issue links** — pairs/groups where the
   same root cause is represented in multiple taxonomy categories. Per
   convention **C2** we don't expand the scan to find these, but we
   record any we stumble across.
9. **Skipped — engine-level** — optional roll-up list of all skip-engine
   decisions for quick scanning. Empty is fine.

## Per-issue entry schema

One `### #<number> — <title>` block per issue, containing the fields below
in order. Bold labels are literal; downstream tools grep for them.

```markdown
### #<number> — <title verbatim from dataset>

- **URL:** <github url>
- **Created:** <YYYY-MM-DD> (~<N.N> y old) · **Updated:** <YYYY-MM-DD>
- **Reactions:** <total> (<emoji> <count>, …)
- **Labels:** <comma-separated labels in inline code>
- **Ownership:** `<team-name>`
- **Decision:** **<decision type>** [→ **<sub-outcome>**]

**Root cause.** 2–5 sentences. Cite comment-summary or raw-comment
observations that led to the classification.

**Why <skip-type> / Test approach.** One of the following:
  - For `skip-engine`: name the file/class/module the fix would target
    and explain why no framework vantage point reaches it.
  - For `skip-proposal`: summarize the API request shape.
  - For `skip — needs native-platform verification`: explain what native
    reference is missing.
  - For `write-test`: describe the test shape in 3–5 bullets.

**Test:** [`issue_<n>_<slug>_test.dart`](relative/path) — only when a test
is authored.

**Test outcome.** Required when a test is authored. Include:
  - The observed result (pass / fail, with assertion that fired).
  - Interpretation: which `write-test` sub-outcome applies.
  - Any caveats (e.g. "passes but does not exercise the real bug path").

**Dedup scan.** Describe what was searched (terms, scope) and what turned
up. If no in-category duplicates, say so explicitly. List weak
related-issue candidates with one-line reasons so a future editor can
re-verify.

**Cross-category siblings (optional).** Only if a non-IME/CJK sibling was
noticed. Name the issue, its category, and the shared surface. Do **not**
expand the scan for siblings; this field is for things that fell into
our lap.

**Notes / process learnings (optional).** Any insight about the workflow
that emerged from this issue. Keep brief; the spec is the canonical home
for conventions, not per-issue notes.
```

## Regression test co-location

- **Directory:** `regression_tests/<category_slug>/`.
- **Filename:** `issue_<number>_<slug_of_title>_test.dart`. Slug is
  snake_case, punctuation stripped; truncate if the title is absurdly
  long.
- **Header comment block** at the top of the test file must include:
  - The GitHub issue URL.
  - A 2–6 sentence summary of the bug.
  - The *expected failure mode* today (so a later reader can tell whether
    a pass is evidence of a fix or a broken test).
  - A brief note on what the test asserts and why it's the right probe.
- **Test style:** prefer narrow `test(...)` blocks with a single
  assertion when possible (easier to interpret pass/fail). Use
  `testWidgets(...)` when the bug requires a pumped widget tree.
- **Imports:** only `package:flutter/*` and `package:flutter_test/*`. The
  tests run from the Flutter SDK pubspec; no extra dependencies.
- **Running tests:** `flutter test <absolute path>` from anywhere inside
  the flutter repo. Relative paths from the wrong cwd silently resolve to
  bogus locations — always use absolute paths.

## Conventions (locked)

Add new conventions here as they emerge. Every convention gets a short
identifier and a rationale so it can be cited in issue entries.

### C1 — Layer-check raw comments before committing to `write-test`

**Rule.** If the summary mentions `metaState`, `keycode`, a `.java`/`.m`/
`.mm`/`.cc`/`.h`/`.kt` file path, named embedder/engine classes
(`KeyEmbedderResponder`, `TextInputPlugin`, `KeyboardManager`, etc.), or
phrases like "engine side" / "embedder", read the raw comments before
classifying.

**Why.** Summary compression can strip layer/owner signals while
preserving mechanism. Our summarization pass lost the "engine side"
framing on #98720, producing a framework-sounding classification for what
is actually an embedder bug in `KeyEmbedderResponder.java`.

**How to apply.** In the `Layer check` step of the per-issue workflow,
scan the raw `comments_raw` list for these terms. If any hit, weight the
classification toward `skip — engine-level`.

### C2 — Per-category dedup scope is one category at a time

**Rule.** The dedup scan searches within the current category only, not
the whole dataset. Cross-category siblings are recorded when noticed but
are not actively sought.

**Why.** Keeps scope bounded. Cross-category dedup is a future dedicated
pass once all categories have been individually audited.

**How to apply.** Grep titles, bodies, and comment summaries within the
category. If a cross-category sibling surfaces from an issue's own text
(e.g. it references another issue number explicitly), record it under
"Cross-category sibling / split-issue links" — don't expand the scan to
go hunting.

## Worked example: dedup-scan depth of judgement

The `Dedup scan` field is where cross-issue analysis lives. Two ways to
fill it produce very different downstream outcomes — both are
syntactically valid, but only one moves the audit forward. Examples
below are drawn from real audit prose on the same issue.

### Scenario

Auditing **#177408** ("framework should provide a mechanism to change
the paragraph spacing of text"). Body proposes adding a
`paragraphSpacing` field on `TextStyle`, modeled on `letterSpacing` /
`wordSpacing`. The grep over titles, bodies, and comment summaries
within the same category returns two hits:

- **#36854** ("Setting paragraph distance in Text and TextField", filed
  2019, R=12).
- **#177953** ("framework should apply `paragraphSpacingOverride` to its
  text", filed 2025, R=0).

### Shallow take (declines the cluster)

> **Dedup scan.** Scanned for "paragraph spacing", "paragraphSpacing".
> Found #36854 (very similar proposal, but a distinct issue tracking
> the same request) and #177953 (related but a different scope —
> applying overrides to framework widgets). No duplicates.

Satisfies the field's stated requirements (terms searched, hits listed,
conclusion stated) but drops the actual signal: three reporters over
six years all asking for the same surface on `TextStyle`. The phrasing
*"tracking the same request" + "no duplicates"* is internally
self-contradictory, and the contradiction goes unexamined. Downstream
the strategy review still has three independent items in its queue.

### Deeper take (records the cluster)

> **Dedup scan.** Scanned for "paragraph spacing", "paragraphSpacing".
> Two cluster members under the "Paragraph Spacing API" theme:
>
> - **#36854** (R=12, filed 2019) — oldest framing. Asks for "control
>   over paragraph spacing in both Text and TextField"; same surface,
>   less concrete than this issue's named `paragraphSpacing` field.
> - **#177953** (R=0, filed 2025) — follow-on to PR #172915 which
>   exposed `MediaQueryData.paragraphSpacingOverride`. Asks the
>   framework's own widgets to consume that override. Distinct scope
>   (apply override to existing widgets) but blocked on the same
>   missing `TextStyle` field this issue and #36854 propose; cannot be
>   implemented without it.
>
> Recording as cluster **PS-1** (Paragraph Spacing API). Canonical:
> #36854 (oldest framing). Coordination note: merging into one
> canonical proposal collapses six years of duplicate review queues.

Same factual observations as the shallow take ("very similar",
"different scope") but commits to what they imply: three issues
describing the same API gap from different angles is a cluster, not
three independent items. The cluster code travels into the report's
"Duplicate clusters" section, which is what makes the consolidation
visible to whoever reads the report next.

### The judgement behind the difference

When a dedup grep returns hits, ask: *would I expect these issues to
close together?*

- **Yes** — same fix surface, same proposed API, same upstream bug —
  they are cluster members regardless of how the prose in each issue
  varies. Record as a cluster. If two issues would close together, the
  fact that one is a "proposal" and the other is "tracking the same
  request" is rhetorical packaging, not separate root causes.
- **No** — different fixes, different layers, different platforms —
  they are adjacent. Adjacent entries owe the reader a one-line
  distinguisher: *"different surface (engine layout vs framework
  widget)"*, *"different platform (Windows clipboard vs macOS keystroke)"*,
  *"different mechanism (Skia trim vs Skia justification)"*. "Very
  similar but distinct" without naming the distinction is restating
  the observation, not making the call.

The shortcut to avoid: classifying every overlapping hit as "related but
distinct" so that the conclusion can be "no duplicates." That phrasing
makes the audit feel thorough while leaving the cross-issue structure
of the category invisible. A category audit that ends with one cluster
or zero clusters when the body of evidence shows three or four
overlapping themes is almost certainly under-clustered, not lucky.

## Regenerating / resuming

Cleanup reports are incremental — each issue entry is append-only, and the
running-summary counters are updated in place. To resume a partially-
processed category:

1. Re-open `cleanup_reports/<category>.md`.
2. Find the latest processed-issue entry. The next issue to process is the
   next-highest-priority one per the category's chosen order (typically
   reactions descending; state that order in the report intro).
3. Continue the workflow from step 1 above.

No automated regenerator exists — the process is interactive because the
classification requires judgment that a mechanical run cannot reproduce.

## Evolving the format

- If a new decision type genuinely needs to exist, document it in the
  palette with a definition, then add it to the running-summary counter
  list, then use it in the next entry.
- If a new convention emerges, add it as `C<N>` with rule / why / how.
- Breaking structural changes to the report (renaming top-level sections,
  changing per-issue field order) require updating this spec in the same
  commit. Additive changes (new optional field at the end of a section) are
  fine without spec churn.
