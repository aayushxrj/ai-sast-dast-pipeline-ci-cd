import os
import json
import requests
import subprocess
from collections import defaultdict

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]
PR_NUMBER = os.environ["PR_NUMBER"]

# Load detected issues
with open("reports/resolution.json", encoding="utf-8") as f:
    issues = json.load(f)["issues"]

# Get latest commit SHA
headers = {"Authorization": f"token {GITHUB_TOKEN}"}
pr_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
pr_resp = requests.get(pr_url, headers=headers)
pr_resp.raise_for_status()
commit_sha = pr_resp.json()["head"]["sha"]

# Get diff of PR (unified=0 gives precise line numbers)
diff_output = subprocess.run(
    ["git", "diff", "origin/main", commit_sha, "--unified=0"],
    stdout=subprocess.PIPE, text=True
).stdout

# Parse changed lines from diff
changed_lines = defaultdict(set)
current_file = None
for line in diff_output.splitlines():
    if line.startswith("+++ b/"):
        current_file = line[6:]
    elif line.startswith("@@"):
        parts = line.split(" ")
        if len(parts) >= 3 and current_file:
            new_file_range = parts[2]
            if new_file_range.startswith("+"):
                parts = new_file_range[1:].split(",")
                start = int(parts[0])
                count = int(parts[1]) if len(parts) > 1 else 1
                for i in range(start, start + count):
                    changed_lines[current_file].add(i)

# ✅ Debug output for changed lines
print("📄 Detected changed lines:")
for path, lines in changed_lines.items():
    print(f"  {path}: {sorted(lines)}")

# Only comment on changed lines
comments = []
for issue in issues:
    path = issue["file"]
    line = issue["end_line"]
    if line in changed_lines.get(path, set()):
        comments.append({
            "path": path,
            "side": "RIGHT",
            "line": line,
            "body": f'{issue["message"]}\n\n**Suggested Fix:**\n{issue["resolution"]}'
        })

# If no eligible comments, skip review
if not comments:
    print("⚠️ No commentable issues found on changed lines.")
    exit(0)

# Send PR review
review_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/reviews"
review_data = {
    "commit_id": commit_sha,
    "body": "🔐 Automated security review comments.",
    "event": "COMMENT",
    "comments": comments
}
resp = requests.post(review_url, headers=headers, json=review_data)
resp.raise_for_status()
print("✅ PR review comments posted.")
