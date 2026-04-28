import json
import os

repo_dir = "../../"
with open(os.path.join(repo_dir, "text_input_issues.json")) as f:
    data = json.load(f)

categories = set(i.get("category", "") for i in data["issues"])
target_cat = [c for c in categories if "bidi" in c.lower() or "internationalization" in c.lower()][0]

issues = [i for i in data["issues"] if i.get("category") == target_cat]
issues.sort(key=lambda x: x.get("reactions", {}).get("total", 0), reverse=True)
batch = issues[20:30]

with open(os.path.join(repo_dir, "data/merged_raw.json")) as f:
    raw_data = json.load(f)

raw_dict = {i["number"]: i for i in raw_data["issues"]}

batch_out = []
for i in batch:
    num = i["number"]
    comments = []
    if num in raw_dict:
        issue_node = raw_dict[num]
        comments_field = issue_node.get("comments", {})
        if "nodes" in comments_field:
            comments = [c.get("body", "") for c in comments_field["nodes"]]
        elif "edges" in comments_field:
            comments = [e.get("node", {}).get("body", "") for e in comments_field["edges"]]
    i["comments_raw"] = comments
    batch_out.append(i)

with open("batch_v4_3.json", "w") as f:
    json.dump(batch_out, f, indent=2)
