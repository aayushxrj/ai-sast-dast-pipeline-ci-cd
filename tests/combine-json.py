import json
from pathlib import Path

def load_json(path):
    with open(path) as f:
        return json.load(f)

bandit_data = load_json("reports/bandit_report.json")
semgrep_data = load_json("reports/semgrep_report.json")
gitleaks_data = load_json("reports/gitleaks_report.json")

combined_issues = []

# Bandit normalization
for item in bandit_data.get("results", []):
    combined_issues.append({
        "tool": "bandit",
        "file": item["filename"],
        "line": item["line_number"],
        "column": item.get("col_offset", 0),
        "severity": item["issue_severity"],
        "confidence": item["issue_confidence"],
        "rule_id": item["test_id"],
        "message": item["issue_text"],
        "cwe": item.get("issue_cwe", {}).get("id", ""),
        "source_url": item.get("more_info", ""),
        "code": item.get("code", "")
    })

# Semgrep normalization
for item in semgrep_data.get("results", []):
    combined_issues.append({
        "tool": "semgrep",
        "file": item["path"],
        "line": item["start"]["line"],
        "column": item["start"]["col"],
        "severity": item["extra"].get("severity", "UNKNOWN"),
        "confidence": item["extra"].get("metadata", {}).get("confidence", ""),
        "rule_id": item["check_id"],
        "message": item["extra"]["message"],
        "cwe": item["extra"].get("metadata", {}).get("cwe", [""])[0],
        "source_url": item["extra"].get("metadata", {}).get("source", ""),
        "code": None  # Semgrep doesn't always return the code snippet
    })

# Gitleaks normalization
for item in gitleaks_data:
    combined_issues.append({
        "tool": "gitleaks",
        "file": item["File"],
        "line": item["StartLine"],
        "column": item["StartColumn"],
        "severity": "HIGH",
        "confidence": "HIGH",
        "rule_id": item["RuleID"],
        "message": item["Description"],
        "cwe": None,
        "source_url": None,
        "code": item["Match"]
    })

# Output
Path("reports").mkdir(exist_ok=True)
with open("reports/combined_issues.json", "w") as f:
    json.dump({"issues": combined_issues}, f, indent=2)

print(f"Combined {len(combined_issues)} issues into reports/combined_issues.json")
