import json

def main():
    with open('data/merged_raw.json') as f:
        merged_raw = json.load(f)
    raw_comments_map = {str(item['number']): item.get('comments_raw', []) for item in merged_raw.get('issues', [])}

    with open('text_input_issues.json') as f:
        data = json.load(f)

    issues = []
    for issue in data['issues']:
        if issue.get('category') == "Internationalization, BiDi, and text layout":
            issue['comments_raw'] = raw_comments_map.get(str(issue['number']), [])
            issues.append(issue)

    issues.sort(key=lambda x: x.get('reactions', {}).get('total', 0), reverse=True)

    with open('data/bidi_issues_v3.json', 'w') as f:
        json.dump(issues, f, indent=2)

    with open('top_10_bidi_v3.txt', 'w') as f:
        for i, issue in enumerate(issues[:10]):
            f.write(f"### #{issue['number']} - {issue['title']}\n")
            f.write(f"URL: {issue['url']}\n")
            f.write(f"Created: {issue['created_at']} Updated: {issue['updated_at']}\n")
            f.write(f"Reactions: {issue.get('reactions', {})}\n")
            f.write(f"Labels: {issue.get('labels', [])}\n")
            f.write(f"Ownership: {issue.get('ownership')}\n")
            f.write(f"Summary: {issue.get('comment_summary', '')}\n")
            f.write(f"Body snippet: {issue.get('body', '')[:500]}...\n")
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
