import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

RESOLUTION_PATH = "reports/resolution.json"
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
GITHUB_SHA = os.environ.get("GITHUB_SHA")
GITHUB_EVENT_NAME = os.environ.get("GITHUB_EVENT_NAME")
GITHUB_SERVER_URL = os.environ.get("GITHUB_SERVER_URL", "https://github.com")

# Load issues count
def get_issues_count():
    try:
        with open(RESOLUTION_PATH, encoding="utf-8") as f:
            data = json.load(f)
            return len(data.get("issues", []))
    except Exception:
        return 0


def main():
    issues_count = get_issues_count()
    event_type = "PR" if GITHUB_EVENT_NAME == "pull_request_target" else "push"
    repo_url = f"{GITHUB_SERVER_URL}/{GITHUB_REPOSITORY}"
    security_tab_url = f"{repo_url}/security/code-scanning"
    commit_url = f"{repo_url}/commit/{GITHUB_SHA}"

    msg = (
        f"*Detected {issues_count} security issues in {event_type}.*\n"
        f"\n"
        f"• View all security issues: <{security_tab_url}|GitHub Security Tab>\n"
        f"• View commit: <{commit_url}|{GITHUB_SHA[:7]}>\n"
    )

    payload = {"text": msg}
    resp = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if resp.status_code != 200:
        print(f"Failed to send Slack notification: {resp.text}")
    else:
        print("✅ Slack notification sent.")

if __name__ == "__main__":
    main()
