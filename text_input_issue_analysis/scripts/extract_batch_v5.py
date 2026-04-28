import json
import sys

def main():
    # Read main dataset
    with open('flutter-agent-skills/text_input_issue_analysis/text_input_issues.json', 'r') as f:
        issues_data = json.load(f)['issues']

    # Read raw comments
    with open('flutter-agent-skills/text_input_issue_analysis/data/merged_raw.json', 'r') as f:
        raw_issues_list = json.load(f)['issues']
        raw_data = {str(i['number']): i for i in raw_issues_list}

    # Filter by category
    cat_name = "Internationalization, BiDi, and text layout"
    cat_issues = [i for i in issues_data if i.get('category') == cat_name]

    # Sort by reactions descending, then number descending
    cat_issues.sort(key=lambda x: (x.get('reactions', {}).get('total', 0), x.get('number', 0)), reverse=True)

    # We want to process batch 1 (issues 0 to 9)
    batch = cat_issues[40:44]
    
    print(f"Total issues in category: {len(cat_issues)}")
    
    for idx, issue in enumerate(batch):
        num = str(issue['number'])
        raw_issue = raw_data.get(num, {})
        raw_comments = raw_issue.get('comments_raw', [])
        
        print(f"\n=========================================")
        print(f"BATCH 1 - ISSUE {idx+1}: #{num} - {issue['title']}")
        print(f"URL: {issue['url']}")
        print(f"Created: {issue['created_at']} | Updated: {issue['updated_at']}")
        print(f"Reactions: {issue.get('reactions', {})}")
        print(f"Labels: {issue.get('labels', [])}")
        print(f"Ownership: {issue.get('ownership')}")
        print(f"Summary: {issue.get('comment_summary')}")
        print(f"Body snippet (first 1000 chars):\n{issue.get('body', '')[:1000]}")
        
        # Layer check triggers
        text_to_check = str(issue.get('comment_summary', '')) + " " + str(issue.get('body', ''))
        triggers = ['metaState', 'keycode', '.java', '.m', '.mm', '.cc', '.h', '.kt', 'KeyEmbedderResponder', 'TextInputPlugin', 'KeyboardManager', 'engine side', 'embedder']
        triggered = [t for t in triggers if t.lower() in text_to_check.lower()]
        if triggered:
            print(f"LAYER CHECK TRIGGERED BY: {triggered}")
            print(f"Raw Comments ({len(raw_comments)}):")
            for c in raw_comments:
                print(f" - {c[:500]}...") # truncate for sanity
                print("---")

if __name__ == '__main__':
    main()
