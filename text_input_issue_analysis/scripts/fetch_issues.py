#!/usr/bin/env python3
"""
Fetch Flutter issues for a given label via GitHub GraphQL.

Fetches metadata + comments in a single query per page.
Uses manual cursor pagination (gh --paginate is unreliable with GraphQL).
Checkpoints progress to disk after every page.

Usage:
  fetch_issues.py <output_path> <search_query> [--max-pages N]

Example:
  fetch_issues.py team_text_input.json "repo:flutter/flutter is:issue is:open label:team-text-input"
  fetch_issues.py a_text_input_old.json 'repo:flutter/flutter is:issue is:open label:"a: text input" created:<=2023-06-01'
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path


QUERY_TEMPLATE = """
query($q: String!, $after: String) {
  search(query: $q, type: ISSUE, first: 100, after: $after) {
    issueCount
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on Issue {
        number
        title
        url
        state
        createdAt
        updatedAt
        body
        labels(first: 30) { nodes { name } }
        assignees(first: 10) { nodes { login } }
        comments(first: 100) {
          totalCount
          pageInfo { hasNextPage endCursor }
          nodes { body }
        }
      }
    }
  }
  rateLimit { remaining resetAt cost }
}
"""

COMMENT_PAGE_QUERY = """
query($number: Int!, $after: String) {
  repository(owner: "flutter", name: "flutter") {
    issue(number: $number) {
      comments(first: 100, after: $after) {
        pageInfo { hasNextPage endCursor }
        nodes { body }
      }
    }
  }
}
"""


def gh_graphql(query, variables):
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        if v is None:
            continue
        if isinstance(v, int):
            cmd.extend(["-F", f"{k}={v}"])
        else:
            cmd.extend(["-f", f"{k}={v}"])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"gh api graphql failed: rc={result.returncode}\nSTDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout}"
        )
    data = json.loads(result.stdout)
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {json.dumps(data['errors'], indent=2)}")
    return data["data"]


def fetch_remaining_comments(issue_number, cursor):
    """Continue paginating comments for an issue with more than 100 comments."""
    out = []
    while True:
        data = gh_graphql(COMMENT_PAGE_QUERY, {"number": issue_number, "after": cursor})
        comments = data["repository"]["issue"]["comments"]
        out.extend(c["body"] for c in comments["nodes"])
        if not comments["pageInfo"]["hasNextPage"]:
            break
        cursor = comments["pageInfo"]["endCursor"]
    return out


def flatten_issue(node):
    """Transform GraphQL node to our schema (comment_summary/category/ownership filled later)."""
    labels = [l["name"] for l in node["labels"]["nodes"]]
    assignees = [a["login"] for a in node["assignees"]["nodes"]]
    comment_bodies = [c["body"] for c in node["comments"]["nodes"]]

    # Handle issues with more than 100 comments.
    if node["comments"]["pageInfo"]["hasNextPage"]:
        extra = fetch_remaining_comments(
            node["number"], node["comments"]["pageInfo"]["endCursor"]
        )
        comment_bodies.extend(extra)

    return {
        "number": node["number"],
        "title": node["title"],
        "url": node["url"],
        "state": node["state"].lower(),
        "labels": labels,
        "assignees": assignees,
        "ownership": None,  # filled during merge step
        "created_at": node["createdAt"],
        "updated_at": node["updatedAt"],
        "body": node["body"],
        "comments_raw": comment_bodies,  # kept temporarily, removed before final output
        "comment_count": node["comments"]["totalCount"],
        "comment_summary": None,
        "category": None,
    }


def fetch_all(search_query, out_path, max_pages=None):
    """Paginate through all results matching search_query, checkpointing as we go."""
    # Resume support: if an in-progress file exists, pick up the cursor.
    cursor = None
    issues_by_number = {}
    issue_count = None
    pages_done = 0

    if out_path.exists():
        state = json.loads(out_path.read_text())
        cursor = state.get("_next_cursor")
        for iss in state.get("issues", []):
            issues_by_number[iss["number"]] = iss
        issue_count = state.get("_issue_count")
        pages_done = state.get("_pages_done", 0)
        done = state.get("_done", False)
        if done:
            print(f"Already complete: {len(issues_by_number)} issues in {out_path.name}")
            return state
        print(f"Resuming from cursor={cursor!r} with {len(issues_by_number)} issues so far")

    while True:
        if max_pages is not None and pages_done >= max_pages:
            print(f"Reached max_pages={max_pages}, stopping")
            break

        t0 = time.time()
        data = gh_graphql(QUERY_TEMPLATE, {"q": search_query, "after": cursor})
        search = data["search"]
        rl = data["rateLimit"]
        if issue_count is None:
            issue_count = search["issueCount"]

        for node in search["nodes"]:
            if not node:
                continue
            flat = flatten_issue(node)
            issues_by_number[flat["number"]] = flat

        pages_done += 1
        elapsed = time.time() - t0
        print(
            f"  page {pages_done}: +{len(search['nodes'])} nodes  "
            f"total={len(issues_by_number)}/{issue_count}  "
            f"rl_remaining={rl['remaining']} cost={rl['cost']}  "
            f"{elapsed:.1f}s"
        )

        cursor = search["pageInfo"]["endCursor"]
        has_next = search["pageInfo"]["hasNextPage"]

        checkpoint = {
            "query": search_query,
            "_issue_count": issue_count,
            "_pages_done": pages_done,
            "_next_cursor": cursor,
            "_done": not has_next,
            "issues": list(issues_by_number.values()),
        }
        out_path.write_text(json.dumps(checkpoint, indent=2))

        if not has_next:
            print(f"Done. Fetched {len(issues_by_number)} issues (GitHub reported {issue_count}).")
            break

    final = json.loads(out_path.read_text())
    return final


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("output", type=Path)
    ap.add_argument("query")
    ap.add_argument("--max-pages", type=int, default=None)
    args = ap.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fetch_all(args.query, args.output, args.max_pages)


if __name__ == "__main__":
    main()
