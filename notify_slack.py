import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

RESOLUTION_PATH = "reports/resolution.json"
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
GITHUB_EVENT_NAME = os.environ.get("GITHUB_EVENT_NAME")
GITHUB_SERVER_URL = os.environ.get("GITHUB_SERVER_URL", "https://github.com")

# PR-specific (if pull_request_target)
PR_NUMBER = os.environ.get("GITHUB_PR_NUMBER")
PR_TITLE = os.environ.get("GITHUB_PR_TITLE")
PR_AUTHOR = os.environ.get("GITHUB_PR_AUTHOR")

# Push-specific
PUSH_AUTHOR = os.environ.get("GITHUB_PUSH_AUTHOR")
PUSH_BRANCH = os.environ.get("GITHUB_PUSH_BRANCH")

def get_issues_count():
    try:
        with open(RESOLUTION_PATH, encoding="utf-8") as f:
            data = json.load(f)
            return len(data.get("issues", []))
    except Exception:
        return 0

def main():
    issues_count = get_issues_count()
    repo_url = f"{GITHUB_SERVER_URL}/{GITHUB_REPOSITORY}"
    security_tab_url = f"{repo_url}/security/code-scanning"

    if GITHUB_EVENT_NAME == "pull_request_target":
        event_type = "PR"
        msg = f"*Detected {issues_count} security issues in {event_type}.*\n"
        if PR_NUMBER:
            pr_url = f"{repo_url}/pull/{PR_NUMBER}"
            msg += f"• PR: <{pr_url}|#{PR_NUMBER} - {PR_TITLE}> by `{PR_AUTHOR}`\n"
    else:
        event_type = "Push"
        msg = f"*Detected {issues_count} security issues in {event_type}.*\n"
        msg += f"• Branch: `{PUSH_BRANCH}`\n"
        msg += f"• Author: `{PUSH_AUTHOR}`\n"

    msg += f"• View all security issues: <{security_tab_url}|GitHub Security Tab>\n"

    payload = {"text": msg}
    resp = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if resp.status_code != 200:
        print(f"Failed to send Slack notification: {resp.text}")
    else:
        print("✅ Slack notification sent.")

if __name__ == "__main__":
    main()
