import json
import hashlib

def load_issues(path):
    with open(path, 'r') as f:
        data = json.load(f)
        if isinstance(data, dict) and "issues" in data:
            return data["issues"]
        return data

def save_issues(path, issues):
    with open(path, 'w') as f:
        json.dump(issues, f, indent=2)

def issue_signature(issue):
    """
    Generate a hashable signature based on the core content of the issue.
    This helps detect duplicates even from different tools.
    """
    fields = [
        issue.get("path", ""),
        str(issue.get("start", {}).get("line", "")),
        issue.get("check_id", ""),
        issue.get("extra", {}).get("message", ""),
        issue.get("extra", {}).get("lines", ""),
    ]
    fingerprint = "||".join(fields).strip()
    return hashlib.md5(fingerprint.encode()).hexdigest()

def deduplicate(issues):
    seen = set()
    unique_issues = []

    for issue in issues:
        sig = issue_signature(issue)
        if sig not in seen:
            seen.add(sig)
            unique_issues.append(issue)

    return unique_issues

def main():
    input_path = "reports/combined_issues.json"
    output_path = "reports/deduplicated_issues.json"

    print(f"🔄 Loading issues from: {input_path}")
    combined = load_issues(input_path)

    print(f"📊 Total issues before deduplication: {len(combined)}")
    deduped = deduplicate(combined)
    print(f"✅ Unique issues after deduplication: {len(deduped)}")

    print(f"💾 Saving deduplicated issues to: {output_path}")
    save_issues(output_path, deduped)

if __name__ == "__main__":
    main()
