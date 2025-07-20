# classify_and_comment_gemini.py

import json
import os
from github import Github
import google.generativeai as genai

# GitHub setup
REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = int(os.getenv("PR_NUMBER"))
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Gemini setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO)
pr = repo.get_pull(PR_NUMBER)

def load_findings(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def generate_comment(issue_text, code_snippet):
    prompt = f"""You're a security expert AI assistant.

The following code has a security issue:
{code_snippet}

markdown
Copy
Edit

Issue description:
{issue_text}

Explain the issue in simple terms, and suggest how to fix it.
"""
    response = model.generate_content(prompt)
    return response.text

def comment_on_file(path, line, message):
    for file in pr.get_files():
        if file.filename == path:
            pr.create_review_comment(
                body=message,
                commit_id=pr.head.sha,
                path=path,
                line=line,
                side='RIGHT'
            )
            return

def main():
    semgrep_issues = load_findings("reports/semgrep_report.json")
    for result in semgrep_issues.get('results', []):
        file_path = result['path']
        line = result['start']['line']
        issue = result['check_id'] + ": " + result['extra']['message']
        snippet = result.get('extra', {}).get('lines', '')

        suggestion = generate_comment(issue, snippet)
        comment_on_file(file_path, line, suggestion)

if __name__ == "__main__":
    main()