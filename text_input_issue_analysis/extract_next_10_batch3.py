import json

def main():
    with open('data/bidi_issues_v3.json') as f:
        issues = json.load(f)

    # I processed 19 issues in the first two batches (indices 0 to 18).
    # Now I will process the next 10 (indices 19 to 28).
    batch = issues[19:29]

    with open('next_10_bidi_v3_batch3.txt', 'w') as f:
        for i, issue in enumerate(batch):
            f.write(f"### #{issue['number']} - {issue['title']}\n")
            f.write(f"URL: {issue['url']}\n")
            f.write(f"Created: {issue['created_at']} Updated: {issue['updated_at']}\n")
            f.write(f"Reactions: {issue.get('reactions', {})}\n")
            f.write(f"Labels: {issue.get('labels', [])}\n")
            f.write(f"Ownership: {issue.get('ownership')}\n")
            f.write(f"Summary: {issue.get('comment_summary', '')}\n")
            f.write(f"Body snippet: {issue.get('body', '')[:1000]}...\n")
            comments = issue.get('comments_raw', [])
            f.write(f"Raw Comments Count: {len(comments)}\n")
            for c in comments:
                if isinstance(c, dict):
                    f.write(f"  Comment ({c.get('author')}): {c.get('body', '')}\n")
                else:
                    f.write(f"  Comment: {c}\n")
                f.write(f"  ---\n")
            f.write("="*80 + "\n\n")

if __name__ == "__main__":
    main()
