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

## Cleanup workstream — in progress

A parallel track to Step 3 (taxonomy iteration). Audits each of the 31
discovered categories one issue at a time, producing per-category
recommendations: dedup-and-merge, close-as-stale, or write a framework-
level regression test. Output per category is a single markdown file in
`cleanup_reports/` plus any authored tests in `regression_tests/`.

### Spec
- **Format and workflow:** [`CLEANUP_REPORT_FORMAT.md`](CLEANUP_REPORT_FORMAT.md).
  Locks the decision-type palette (write-test, skip-engine,
  skip-proposal, skip-needs-native-verification, likely-stale,
  likely-duplicate), the per-issue entry schema, and accumulated
  conventions (C1 layer-check raw comments before classifying;
  C2 per-category dedup scope).

### Outputs
- `cleanup_reports/<category_slug>.md` — one per audited category
  (snake-case-of-taxonomy-name; e.g. `ime_cjk.md`, `scrolling_containers.md`).
- `regression_tests/<category_slug>/issue_<number>_<slug>_test.dart` —
  framework-level regression tests authored during cleanup.

### Status as of 2026-04-26

| # | Category | Issues | Tests | Skip-engine % | Notes |
|---|---|---|---|---|---|
| ✅ | IME, CJK composing, and dead keys/accents | 104 | 3 | 73% | 10 clusters, 13 likely-duplicate merges identified |
| ✅ | Hardware keyboard, key events, and shortcuts | 99 | 2 | 70% | 3 clusters (PKC-1, NKI-1, WKR-1) |
| ✅ | Text selection behavior and gestures | 28 | 0 | 71% | Hypothesis miss — see report's retrospective section |
| ✅ | Scrolling containers and ensureVisible with text fields | 24 | 2 | 71% | Best write-test rate so far (8.3%) |
| ⏳ | (27 remaining categories) | 839 | — | — | See `category_profiles.md` |

**Totals so far:** 4 / 31 categories complete, 255 / 1,122 issues processed
(23%), 7 regression tests authored (5 fail-as-expected confirming real
bugs, 1 pass-green-exercises-bug-path likely-stale, 1 test-error harness
gap).

### How to resume
1. Read [`CLEANUP_REPORT_FORMAT.md`](CLEANUP_REPORT_FORMAT.md) to refresh
   on the workflow and decision palette.
2. Pick the next category (see "Pending decision" below).
3. Initialize `cleanup_reports/<slug>.md` from the spec template.
4. Process issues in batches of up to 10, reactions-descending order.
5. For each issue: fetch from `text_input_issues.json` (and raw comments
   from `data/merged_raw.json` when C1 layer-check fires) → classify →
   dedup-scan within category → optionally author + run a regression
   test → append entry → update running summary counters.

### Pending decision (paused on)
Which category next. Recommendations from the last session, ordered by
predicted framework-testability after recalibrating on Scrolling
containers' 8.3% rate:

| Candidate | Issues | Why |
|---|---|---|
| TextEditingController, values, and deltas | 25 | Pure framework code, framework-heavy ownership |
| TextSpan, WidgetSpan, and rich text in editable/selectable widgets | 12 | Small, observable widget/render state |
| Form, FormField, and validation | 20 | Pure framework but proposal-heavy |
| Autocomplete widget | 17 | Pure framework widget |
| TextInputFormatter and input masks | 4 | Tiny, pure framework code |

User may pivot to a different criterion (biggest remaining = Keyboard
visibility 91 issues / 579 reactions; highest reaction concentration =
Input types 10.6 avg; etc.).

### Cross-category process learnings
- **Skip-engine rate is consistently ~70-73%** across the four categories
  audited so far. The text-input domain is dominated by embedder/engine
  bugs; framework-only fixes are the minority.
- **Write-test rate varies sharply** (0% – 8.3%) depending on whether the
  category's bugs surface through observable framework state (good:
  `ScrollController.offset`, `controller.selection`, `FocusNode.hasFocus`)
  vs. require simulating triggers `testWidgets` doesn't have primitives
  for (bad: selection-handle drag, embedder-side key-event synthesis,
  IME composition state).
- **Cluster patterns can span categories.** First example: #98720
  (IME/CJK) ↔ #184744 (Hardware keyboard) — same `KeyEmbedderResponder.java`
  fix target. Per-category dedup misses these; recorded under "Cross-
  category sibling/split-issue links" in each report.
- **Per-batch velocity is the right shape.** Batches of 10, processed
  in one conversation turn each, with cluster bookkeeping between
  batches. Smaller batches risk losing context; bigger batches
  saturate the conversation context window.

### Test-harness primitive gaps that block more write-tests
Captured here for a possible future investment in `flutter_test`:

1. **Selection-overlay handle drag.** ~4 deferred candidates across
   Selection gestures and Scrolling containers (#89024, #100319,
   #143479, #132042). A `tester.dragSelectionHandle(handleType, offset)`
   primitive would unlock these.
2. **viewInsets / keyboard-animation simulation.** Several Scrolling
   containers issues (#50329 ensureVisible, #130259
   SliverPersistentHeader, #172437 Drawer scrollPadding) are testable
   in principle but not without simulating a keyboard show/hide
   animation. Currently blocked by `MediaQuery.viewInsets` being
   read-only at the test-harness level.
3. **`KeyEventSimulator` completeness gaps.** Tracked in-tree as
   #96021 (uppercase), #96022 (macOS shifted-keys map), #133954
   (Windows numpadEnter). Each unlocks a slice of Hardware keyboard
   tests.
4. **Mocked-channel `TextInput.setComposingRect` round-trip.** Blocked
   #92050 (DSK-IME-1 cluster canonical) in IME/CJK. The platform-
   channel mock suppresses the exact connection state that triggers
   the periodic post-frame callback under test.

### Cluster watchlist (across done categories)
Tentative clusters that may grow as remaining categories are audited:

- **PKC-1** Pressed-keys state corruption from engine-side sequencing
  (Hardware keyboard, 9 members + watch for more)
- **NKI-1** Non-keyboard input device mis-mapping (Hardware keyboard,
  5 members + watch)
- **DK-1** Dead-key composition on mobile (IME/CJK, 5 members + watch
  for more iOS / Android dead-key issues across remaining categories)
- **MCIME-1** macOS CJK IME composing state (IME/CJK, 6 members +
  watch for more `FlutterTextInputPlugin.mm` symptoms)
- **WKI-1** Windows Korean IME family (IME/CJK, 5/5 processed; closed)
- **DSK-IME-1** Desktop IME candidate-window positioning (IME/CJK,
  5 members + watch for more `setComposingRect`-surface bugs)
- **CWB-1** CJK word breaks (IME/CJK, 2 members)
- **CRC-1** Composing-region cursor clamping (IME/CJK, 3 members)
- **IHK-1** iOS hardware-keyboard IME candidate navigation (IME/CJK,
  3 members)
- **AIR-1** Android IME restart on composing-region change (IME/CJK,
  3 members)
- **CSR-1** Composing state not reset on disruptive event (IME/CJK,
  5 members)
- **DKD-1** Desktop dead-key composition (IME/CJK, 2 members)
- **WKR-1** Windows synthesized key-event ordering (Hardware keyboard,
  2 members; sub-cluster of PKC-1)

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

### 2026-04-26 — Cleanup workstream paused for resumption

Per-category cleanup audit (the workstream tracked in the
"Cleanup workstream — in progress" section above) is paused with 4 of
31 categories complete. State is fully recoverable from disk:
`cleanup_reports/`, `regression_tests/`, and `CLEANUP_REPORT_FORMAT.md`
are all the resumer needs. Pending decision is which category to do
next; defaults and alternatives listed in the "Pending decision" subsection
above.

**Why:** Long-running multi-session workstream — paused to let the user
return on their own schedule without losing context.

**How to apply:** Resumer reads `STATUS.md` (this section + the cleanup
workstream section) and `CLEANUP_REPORT_FORMAT.md`. No memory or chat-
history is required — every decision and accumulated learning is on
disk.

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
