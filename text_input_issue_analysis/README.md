# Flutter Text Input Analysis — Working Directory

A local survey of every open GitHub issue on `flutter/flutter` that is labeled
`team-text-input` or `a: text input`, annotated with comment-discussion summaries
and unsupervised-discovery categories. Intended as the source material helping to
drive future text input strategy.

> **For current status, next steps, and accumulated process decisions, see
> [`STATUS.md`](STATUS.md).** This README describes what lives in the folder
> and how to (re-)run the pipeline.

## Dataset at a glance

- **1,122** deduplicated open issues as of snapshot `last_refreshed` in
  `text_input_issues.json`.
- **1,041** have real comment summaries; **13** have `comment_summary=null`
  (discussion was pure noise); **68** have no comments.
- **31** categories discovered without predefined guidance; every issue is
  assigned to exactly one category.
- **Ownership is derived from `team-*` labels.** Top owners: `team-text-input`
  383, `team-framework` 183, `team-design` 143, `team-web` 130, `team-ios` 87,
  `team-android` 74, `team-windows` 44, `team-engine` 35, `team-macos` 22,
  `team-linux` 13, smaller teams and 1 orphaned. Zero "undetermined" — every
  issue has at most one `team-*` label.

## Folder structure

```
text_input_issue_analysis/
├── README.md                       # this file — folder layout, schemas, pipeline
├── STATUS.md                       # where we are, what's next, process decisions
├── text_input_issues.json          # THE dataset: 1,122 issues with summaries + categories
├── text_input_taxonomy.json        # 31-category taxonomy with descriptions and examples
├── scripts/                        # pipeline steps (Python 3, stdlib-only)
│   ├── fetch_issues.py             # Step 1a: GraphQL fetch with cursor pagination + checkpointing
│   ├── merge_and_own.py            # Step 1b: dedupe by issue number, derive ownership
│   ├── split_batches.py            # Step 1c: token-bounded batching for summarization
│   ├── make_gapfill_batch.py       # Step 1d: target missing issues across batches for retry
│   ├── verify_summaries.py         # Step 1e: confirm every batch has a complete summary file
│   ├── build_compact.py            # Step 2a: compact the corpus for the categorization agent
│   ├── fetch_reactions.py          # supplementary: backfill per-issue reactions onto an existing snapshot
│   └── assemble_final.py           # Step 1f+2b: assemble the final text_input_issues.json
└── data/
    ├── raw/                        # raw GraphQL pulls (regenerable via fetch_issues.py)
    │   ├── team_text_input.json
    │   ├── a_text_input_old.json   # label "a: text input", created <= 2023-01-01
    │   └── a_text_input_new.json   # label "a: text input", created >  2023-01-01
    ├── merged_raw.json             # dedupe of the three raw pulls; carries raw comment text
    ├── compact_issues.json         # title + truncated body + summary, input to Step 2
    ├── batch_manifest.json         # index of the summarization batches
    ├── categorization.json         # {issue_number_str: category_name} from the discovery agent
    ├── reactions.json              # {issue_number_str: {total, by_type}} from fetch_reactions.py
    ├── batches/                    # 44 workload-balanced batches + 1 gapfill batch
    └── summaries/                  # 44 summary files + 1 gapfill; one 2–5-sentence paragraph per issue
```

## Pipeline (order matters when re-running from scratch)

```bash
# Step 1: survey
python3 scripts/fetch_issues.py   data/raw/team_text_input.json   'repo:flutter/flutter is:issue is:open label:team-text-input'
python3 scripts/fetch_issues.py   data/raw/a_text_input_old.json  'repo:flutter/flutter is:issue is:open label:"a: text input" created:<=2023-01-01'
python3 scripts/fetch_issues.py   data/raw/a_text_input_new.json  'repo:flutter/flutter is:issue is:open label:"a: text input" created:>2023-01-01'
python3 scripts/merge_and_own.py
python3 scripts/split_batches.py
# ... dispatch a summarization agent per batch, write data/summaries/summary_NNN.json ...
python3 scripts/verify_summaries.py
python3 scripts/make_gapfill_batch.py   # only if verify reports gaps
# ... dispatch gapfill agent, write data/summaries/summary_gapfill.json ...
python3 scripts/assemble_final.py   # produces text_input_issues.json with comment_summary populated

# Step 2: categorization
python3 scripts/build_compact.py
# ... dispatch categorization agent (single, Opus) with compact_issues.json as input ...
# ...   writes data/categorization.json + text_input_taxonomy.json ...
python3 scripts/assemble_final.py   # re-run to merge categories into text_input_issues.json

# (Optional) refresh reactions for an existing snapshot without re-fetching comments
python3 scripts/fetch_reactions.py              # resume-safe; add --refresh to re-fetch all
python3 scripts/assemble_final.py               # merge reactions into text_input_issues.json
```

`assemble_final.py` is idempotent — re-run it any time `data/summaries/*`,
`data/categorization.json`, or `data/merged_raw.json` changes.

## Schema of `text_input_issues.json`

```jsonc
{
  "last_refreshed": "ISO-8601 UTC",           // regenerated by assemble_final.py
  "query": "repo:flutter/flutter is:issue is:open (label:team-text-input OR label:\"a: text input\")",
  "total_count": 1122,
  "issues": [
    {
      "number": 12345,
      "title": "...",
      "url": "https://github.com/flutter/flutter/issues/12345",
      "state": "open",
      "labels": ["team-text-input", "P2", "found in release: 3.x"],
      "assignees": ["username"],
      "ownership": "team-text-input",         // derived from team-* labels
      "created_at": "ISO-8601 UTC",
      "updated_at": "ISO-8601 UTC",
      "body": "...",                          // full issue body
      "reactions": {                          // per-issue reaction counts; by_type elides zero-count types
        "total": 42,
        "by_type": { "THUMBS_UP": 30, "HEART": 5, "ROCKET": 6, "HOORAY": 1 }
      },
      "comment_summary": "...",               // 2–5 sentence paragraph, or null
      "category": "..."                       // one of the 31 discovered category names
    }
  ]
}
```

## Schema of `text_input_taxonomy.json`

```jsonc
{
  "discovered_at": "ISO-8601 UTC",
  "summary": "3–5 sentence meta-description of the landscape",
  "categories": [
    {
      "name": "IME, CJK composing, and dead keys/accents",
      "description": "...what belongs here and what does not...",
      "count": 104,
      "examples": [12345, 23456, 34567, 45678, 56789]
    }
  ]
}
```

Categories are sorted by `count` descending.

## Reproducibility notes

- `fetch_issues.py` uses manual cursor pagination (the GitHub CLI's
  `--paginate` produced duplicates in testing). It checkpoints to the output
  file after every page so an interrupted run can resume.
- GitHub's `search` caps results at 1,000. The `a: text input` label has
  ~1,049 open issues, so it is split by `created_at` around `2023-01-01`.
- Summarization is stochastic. `assemble_final.py` will reproduce the same
  `text_input_issues.json` *given the same inputs*, but re-running the
  summarization or categorization agents will produce different (not
  necessarily worse) outputs.
- The summarization prompt lives inside the orchestrating Claude Code
  session, not in a script — the scripts only do the mechanical pre/post
  processing.

## What is safe to git-ignore

If `data/` bloats the repo, the regenerable pieces are:

- `data/raw/*.json` — re-fetchable via `fetch_issues.py`
- `data/merged_raw.json` — re-derivable via `merge_and_own.py`
- `data/batches/*.json` — re-derivable via `split_batches.py`
- `data/compact_issues.json` — re-derivable via `build_compact.py`
- `data/reactions.json` — re-fetchable in ~15s via `fetch_reactions.py`

What to keep in git (expensive to regenerate or canonical):

- `text_input_issues.json` and `text_input_taxonomy.json` — the canonical
  outputs.
- `data/summaries/*.json` — the LLM comment summaries (~3 hours of agent
  work). Technically redundant with `text_input_issues.json`, but the
  per-batch structure is useful for auditing and partial re-runs.
- `data/categorization.json` — the LLM category assignments (also encoded
  in `text_input_issues.json`, but keeping the standalone map makes
  re-categorization cheaper to mix in).
- `data/batch_manifest.json` — the per-batch issue index used for auditing.
