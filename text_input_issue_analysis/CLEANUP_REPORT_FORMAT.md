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
