# STATUS

Where we are and what's next. Update this file each working session.

**Snapshot date:** `last_refreshed` inside `text_input_issues.json` is authoritative; current value as of this STATUS is `2026-04-17`.

---

## Step status

### ✅ Step 1 — Full pull + comment summarization

Completed 2026-04-16.

- Fetched via GitHub GraphQL with cursor pagination (not `--paginate` — it
  produces duplicates).
- The `a: text input` label was split by `created_at ≤ 2023-01-01` vs `>
  2023-01-01` because GitHub search caps at 1,000 results.
- 1,122 unique issues after dedupe. 1,041 have real comment summaries; 13 are
  `null` (pure-noise discussion); 68 have no comments.
- Ownership derived from `team-*` labels: every issue has ≤1 team label (zero
  "undetermined"), one issue ended up "orphaned".

### ✅ Step 2 — Agent-driven categorization

Completed 2026-04-17.

- Unbiased discovery: a single Opus-class agent read the compacted corpus
  (~370k tokens of title + truncated body + comment summary) without being
  shown any predefined category list.
- 31 categories produced; every issue assigned to exactly one; taxonomy
  declared counts match actual counts exactly.
- Top five by count: IME/CJK/dead-keys (104), Hardware keyboard (99), Keyboard
  visibility/insets (91), Selection toolbar/handles/magnifier (66), Focus
  management (57).

### ⏳ Step 3 — Iterate on taxonomy

Not started. See "Next up" below.

---

## Next up — Step 3 plan

Goal: compare the 31 discovered categories against the 9 predefined categories
below, decide keep/merge/split/rename, and produce the final taxonomy that
will drive the strategy document.

### Tasks in order

1. **Side-by-side comparison.** For each of the 9 predefined categories, find
   the closest discovered categories and list them with counts. For each
   discovered category that has no clear match among the 9, flag it as "new
   territory" for a decision.
2. **Decide keep/merge/split** for the discovered set, using the predefined
   categories as one input but not as a hard constraint. Record the reasoning
   (a merge because two clusters were too thin; a split because a discovered
   category actually mixes two strategic bets).
3. **Compute per-category ownership breakdowns** for the retained set — see
   "Process decisions" below for the rule. Publish these alongside the
   category definitions.
4. **Write the final taxonomy artifact.** Overwrite or version
   `text_input_taxonomy.json`, and re-run `scripts/assemble_final.py` after
   updating `data/categorization.json` so the dataset stays consistent.

### User's 9 predefined categories (reference set)

| # | Category | Description |
|---|---|---|
| 1 | **Keyboard shortcuts** | TextField / EditableText interaction with keyboards. |
| 2 | **Text selection gestures** | Tap-to-set, drag-select, double-tap word, triple-tap paragraph, etc. |
| 3 | **Parent scrolling** | Text input components interacting with a surrounding `Scrollable`. |
| 4 | **Inner scrolling** | Text input components scrolling their own long content. |
| 5 | **Text selection context menus** | The menu shown on long-press / right-click on text. |
| 6 | **Text selection handles** | The drag handles shown on mobile during selection. |
| 7 | **CJK** | Input / manipulation / selection of Chinese, Japanese, Korean text. |
| 8 | **Autofill** | Autofill functionality. |
| 9 | **Undo/Redo** | Undo/redo functionality. |

These are candidate strategic themes. They are NOT constraints on the
discovered set — they are what the discovered set should be triangulated
against.

---

## Process decisions

Accumulated conventions for this workstream. Add entries here as new
decisions are made. Every entry gets a date and a rationale.

### 2026-04-17 — Per-category ownership breakdown

For every category retained in the final taxonomy, publish an ownership
(team) breakdown alongside the category definition and count.

**Why:** The android, iOS, and web platform teams are moving toward larger
ownership over text input issues on their platform. Knowing how each
category's issues distribute across teams reveals where a platform team is
already de-facto involved vs. where a nominally-owned issue probably belongs
to a platform team instead.

**How to apply:** Order categories by count descending; within each category,
order owners by count descending. Call out `team-text-input`-owned issues
that are plainly platform-specific (iOS VoiceOver, Android TalkBack, Windows
Narrator, etc.) as re-homing candidates.

### 2026-04-16 — Verify after every agent batch

Agent runs that hit usage or rate limits can produce partial files on disk
even when the completion notification says success. Always run
`scripts/verify_summaries.py` after a batch of summarization agents. For
anything that verifies OK but still looks suspicious, rerun one at a time
with explicit permission rather than in parallel.

### 2026-04-19 — This folder is the long-lived home

`text_input_issue_analysis/` is the canonical home for the entire workstream —
survey, taxonomy, and any future analysis or strategy artifacts. New
deliverables go here (top level for canonical outputs, `data/` for
intermediates). The user commits selected files to git manually; see the
README for the canonical keep/ignore guidance.

### 2026-04-22 — Reactions captured per issue

Added per-issue reaction counts to the snapshot. `fetch_issues.py` now
requests `reactionGroups`, and `scripts/fetch_reactions.py` backfills an
existing snapshot in ~15s (aliased GraphQL, batch=50, cost=1/batch). Each
issue in `text_input_issues.json` now carries `reactions: {total, by_type}`
with zero-count types elided.

**Why:** Reactions (especially `THUMBS_UP`) are a proxy for user-facing impact
that comment volume alone doesn't capture, and is useful as a prioritization
signal in Step 3 (taxonomy iteration) and beyond.

**How to apply:** When comparing categories, report reaction totals and
per-issue averages alongside counts. High-average categories (e.g.
Input types ~10.6, Form validation ~9.7) cluster user frustration on fewer
issues; high-total-but-low-average categories (e.g. IME/CJK) have a long
tail without concentrated votes.

---

## Snapshot-freshness policy

The current `last_refreshed` value inside `text_input_issues.json` is the
authoritative timestamp. Categorization and summaries still apply as long as
the underlying issues haven't materially drifted — a few weeks is fine;
months warrants a refresh via `scripts/fetch_issues.py` followed by
`merge_and_own.py`, `split_batches.py`, and the agent-driven steps. An
incremental-refresh pipeline (pull only issues changed since
`last_refreshed`, re-summarize only the changed ones) is a future
improvement, not yet implemented.
