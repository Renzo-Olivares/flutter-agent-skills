# Category Profile Report — Format Specification

Portable spec for the markdown report `category_profiles.md`. The canonical
generator is `scripts/build_category_profiles.py`, but this spec is
generator-agnostic: any script (or agent) that respects the structure below
produces an equivalent report and can be diffed against existing output.

Use this spec when:

- Producing the same report for a different corpus (e.g., a future workstream
  on another issue cluster).
- Rewriting the generator in a different language.
- Editing `build_category_profiles.py` — update this spec in the same change
  so they don't drift.

## Inputs

Two JSON inputs are required, matching the schemas in this folder's README:

1. **Issue dataset** (e.g., `text_input_issues.json`):
   - `last_refreshed` (ISO-8601 string)
   - `total_count` (int)
   - `issues` (list), each with: `number`, `title`, `url`, `labels` (list of
     strings), `ownership` (string; `"orphaned"` if no `team-*` label),
     `created_at`, `updated_at`, `category`, `reactions` (`{total, by_type}`).

2. **Taxonomy** (e.g., `text_input_taxonomy.json`):
   - `categories` (list, sorted by issue count descending), each with: `name`,
     `description`, `count`, `examples` (optional).

Categories in the report appear **in taxonomy order** (count descending).

## Output structure (top to bottom)

1. **Title** — `# <Subject> — Category Profiles`.
2. **Intro paragraph** — one or two sentences naming what this file is and the
   generator that produced it.
3. **Metadata block** — bulleted list:
   - `Snapshot:` value of `last_refreshed` from the dataset.
   - `Generated:` ISO-8601 UTC timestamp of the script run.
   - `Total issues:` integer.
   - `Categories:` integer.
4. **How to read this file** — a `## How to read this file` section defining
   every per-category stat (see "Per-category sections" below). Keep
   definitions verbatim with the stat names used downstream.
5. **Ownership matrix** — `## Ownership matrix (issue counts)`. One markdown
   table, one row per category in taxonomy order, followed by a **totals row**
   at the bottom. Columns:
   - `#`, `n`, `category` (first three columns)
   - Then one column per team owner, in this fixed order for the major teams:
     `txt, fmw, des, web, ios, and, win, eng, mac, lin`
   - Followed by any remaining owners sorted alphabetically
     (e.g., `orp, a11y, eco, tool`).
   - Cells: the count; a middle-dot (`·`) for zero.
   - Precede the table with a legend mapping abbreviations → full
     `team-*` names.
   - Totals row: `#` = `—`, `n` = grand total issue count (bolded), `category`
     = `**Total**`, and each team cell holds that team's sum across all
     categories (bolded; `·` for zero). The grand total in `n` equals the
     total-issue count of the dataset, and each team column total equals that
     team's corpus-wide issue ownership.
6. **Reaction-weighted ranking** — `## Reaction-weighted ranking`. One table,
   columns `# | category | issues | reactions | avg`, sorted by reaction total
   descending. `avg` is `reactions / issues`, one decimal.
7. **Per-category profiles** — `## Per-category profiles`, then one `###`
   section per category in taxonomy order.

## Per-category sections

Each category section has this fixed structure and ordering. Literal strings
(bold labels) are part of the spec — downstream consumers grep for them.

```
### <Category name, verbatim from taxonomy>

*<Category description, verbatim from taxonomy, wrapped in italics>*

**Size:** N issues · **Reactions:** R total (avg X.X/issue) — <emoji>
<count> · <emoji> <count> · ...

**Ownership:**

| team | issues | % | reactions |
|---|---|---|---|
| `<team-name>` | <n> | <pct>% | <r> |
...

**Priority:** P1: <n> · P2: <n> · P3: <n> · unlabeled: <n>

**Platform labels:** <n>/<total> (<pct>%) have a `platform-*` label —
<name>: <n>, <name>: <n>, ...

**Issue-type tilt:** bug (<n>) · feature (<n>) · other-c-label (<n>) ·
no `c:` label (<n>) — top: `<c: label>` (<n>), `<c: label>` (<n>), ...

**Age:** median <n>d (~X.Xy) · oldest opened <YYYY> · >3y old: <n>
(<pct>%)

**Recency:** <n> issues (<pct>%) updated in the last 90 days

**Reproducibility:** <n>/<total> (<pct>%) have `has reproducible steps`

**Found in release (top 3):** <X.Y> (<n>), <X.Y> (<n>), <X.Y> (<n>)

**Top 5 issues by reactions:**

- [#<number> — <title>](<url>) — **<r>** reactions
- ...
```

### Rules per field

- **Size + Reactions** — one line combining size and reaction summary.
  Reaction avg to one decimal. The emoji list uses this mapping and is sorted
  by count descending; zero-count types omitted:
  `THUMBS_UP → 👍`, `THUMBS_DOWN → 👎`, `LAUGH → 😄`, `HOORAY → 🎉`,
  `CONFUSED → 😕`, `HEART → ❤️`, `ROCKET → 🚀`, `EYES → 👀`.
- **Ownership** — markdown table. Rows sorted by issue count descending,
  tie-broken by reaction total descending. `team` cell uses inline code
  (backticks). `%` is whole-number percent of the category's issue count.
  Include every team that owns ≥1 issue, even at 1. `orphaned` rendered
  verbatim (not a real team name).
- **Priority** — `P1/P2/P3` counts always shown, even if zero. `P0` is shown
  only when non-zero, inserted before `P1`. `unlabeled` is appended only when
  non-zero.
- **Platform labels** — `<n>/<total>` is "issues with ≥1 `platform-*` label"
  over "total issues in category". The trailing list is sorted by count
  descending, `platform-` prefix stripped. Omit the trailing list entirely if
  no platform labels exist in the category.
- **Issue-type tilt** — buckets an issue by its `c:` labels:
  - `bug`: any of `c: crash`, `c: fatal crash`, `c: regression`,
    `c: performance`, `c: flake`.
  - `feature`: any of `c: proposal`, `c: new feature`, `c: new widget`.
  - An issue counted in both `bug` and `feature` is counted in both (rare).
  - `other-c-label`: has ≥1 `c:` label but none in bug/feature.
  - `no c: label`: no `c:` label at all.
  - The "top" trailing list is the top five `c:` labels by frequency, each
    wrapped in inline code.
- **Age** — `median` in whole days, followed by years to one decimal.
  `oldest opened <YYYY>` is the 4-digit year of the earliest `created_at`.
  `>3y old` uses a 1095-day threshold, with percent of the category.
- **Recency** — `updated_at` within the last 90 days of the script run.
  Always include the count and percent, even at zero.
- **Reproducibility** — share with the literal label `has reproducible steps`.
  Always include both count and percent.
- **Found in release** — top 3 `found in release: X.Y` labels by frequency;
  render the version string without the prefix. Line reads `—` (em dash) when
  no such labels exist.
- **Top 5 issues by reactions** — bulleted list, issues sorted by reaction
  total descending. Title truncated to ~100 chars with an ellipsis. Use the
  exact markdown link format shown, with `**R**` for the reaction total.
  Always list up to 5 items; list may be shorter for small categories.

## Counting invariants

The generator (and any reimplementation) must satisfy these per category:

- `Priority` counts plus `unlabeled` sum to the category size.
- `Issue-type tilt` buckets sum to the category size (with `bug` + `feature`
  possibly double-counting the rare issue in both).
- `Ownership` issue counts sum to the category size.
- Platform-label counts in the trailing list may exceed category size (an
  issue can carry multiple `platform-*` labels), but the `<n>/<total>` prefix
  must be `≤ total`.

## Regenerating

From the analysis-folder root:

```bash
python3 scripts/build_category_profiles.py   # writes category_profiles.md
```

The script reads `text_input_issues.json` + `text_input_taxonomy.json` by
default. Output is deterministic except for the `Generated:` timestamp.

## Evolving the format

When editing the generator:

- Update this spec in the same change.
- If a field is added, document it in both the "How to read this file" section
  of the generated report and in the "Per-category sections" block here.
- Prefer additive changes (new fields at the end of a section) so existing
  grep-based consumers keep working.
