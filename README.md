# 🔐 AI-SAST-DAST-Pipeline

A CI/CD-driven security automation project that integrates **SAST**, **DAST**, and **AI/NLP classification** for early detection and smart remediation of code vulnerabilities — built under the **Samsung PRISM 2025** program.



## 🚀 Project Overview

This project aims to:
- Shift security **left** in the software lifecycle
- Automatically run **SAST** and **DAST** during CI/CD
- Use **AI/NLP** to categorize vulnerabilities and suggest fixes
- Report issues via **ChatOps** (Slack/MS Teams) with severity summaries


## ✅ Phase 1: Bandit & Semgrep SAST Integration

### 📌 Tasks

- [ ] Create demo Python app with known vulnerabilities
- [ ] Set up **Bandit** to scan Python code in GitHub Actions
- [ ] Set up **Semgrep** to scan for general static issues across languages
- [ ] View results from Actions tab in GitHub after each PR/push

---

## ⚙️ GitHub Actions Setup (CI/CD)

### 🔹 Bandit (`.github/workflows/bandit.yml`)
- Scans Python code for security flaws (e.g., hardcoded passwords, dangerous functions)

### 🔹 Semgrep (`.github/workflows/semgrep.yml`)
- Scans multiple languages with customizable rules
- Uses Semgrep's auto-config for broad coverage

---

## 🔮 Upcoming Features (In Progress)

### ✅ Phase 2: DAST Integration
- [ ] Use **OWASP ZAP** to scan deployed app (staging URL or container)
- [ ] Automate DAST runs in GitHub Actions
- [ ] Extract and store reports (HTML/JSON format)

### ✅ Phase 3: AI/NLP-Based Classification
- [ ] Create JSON schema to represent security findings
- [ ] Classify vulnerabilities using keywords, regex, or transformer models
- [ ] Assign severity levels (Low/Medium/High/Critical)
- [ ] Generate fix suggestions via LLMs or prompt-based guidance

### ✅ Phase 4: ChatOps & Notifications
- [ ] Set up Slack/MS Teams webhook
- [ ] Send scan summaries like:
  > `"3 High, 2 Medium issues found in PR #23 (Bandit + Semgrep)"`

### ✅ Phase 5: Reporting & Documentation
- [ ] Collect and unify scan results into a Markdown report
- [ ] Auto-comment on PRs with a summary of detected issues
- [ ] Add screenshots, diagrams, and architecture to this README

---

## 🛠 Tools & Technologies

| Area        | Tools/Tech                         |
|-------------|------------------------------------|
| Language    | Python 3.10                        |
| SAST        | Bandit, Semgrep                    |
| DAST        | OWASP ZAP, Arachni (planned)       |
| CI/CD       | GitHub Actions                     |
| AI/NLP      | NLTK, Regex, LLMs (OpenAI API)     |
| ChatOps     | Slack Webhook, MS Teams Webhook    |
| Others      | Docker, Markdown, GitHub API       |

---

## 🗓️ Timeline Breakdown

| Month | Milestone                                         |
|-------|--------------------------------------------------|
| 1️⃣    | Setup demo repo, Bandit + Semgrep integration   |
| 2️⃣    | AI/NLP-based classification module              |
| 3️⃣    | DAST scanning & CI integration with ZAP         |
| 4️⃣    | ChatOps + full pipeline + documentation         |

