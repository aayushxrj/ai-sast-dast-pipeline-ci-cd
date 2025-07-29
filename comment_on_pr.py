import os
import json
import requests

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]
PR_NUMBER = os.environ["PR_NUMBER"]

with open("reports/resolution.json", encoding="utf-8") as f:
    issues = json.load(f)["issues"]

# Get the latest commit SHA for the PR
headers = {"Authorization": f"token {GITHUB_TOKEN}"}
pr_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
pr_resp = requests.get(pr_url, headers=headers)
pr_resp.raise_for_status()
commit_sha = pr_resp.json()["head"]["sha"]

comments = []
for issue in issues:
    path = issue["file"]
    start_line = issue["start_line"]
    end_line = issue["end_line"]
    message = issue["message"]
    resolution = issue["resolution"]
    # GitHub API only supports single-line or multi-line comments (start_line to end_line)
    comments.append({
        "path": path,
        "side": "RIGHT",
        "start_line": start_line if start_line != end_line else None,
        "line": end_line,
        "body": f"{message}\n\n**Suggested Fix:**\n{resolution}"
    })

review_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/reviews"
review_data = {
    "commit_id": commit_sha,
    "body": "Automated security review comments.",
    "event": "COMMENT",
    "comments": comments
}
resp = requests.post(review_url, headers=headers, json=review_data)
resp.raise_for_status()
print("✅ PR review comments posted.")