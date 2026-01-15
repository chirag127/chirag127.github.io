# Security Policy for PRFusion-AI-Powered-GitHub-Automation-CLI-Toolkit

As the Apex Technical Authority, security is our paramount concern. PRFusion, which handles sensitive GitHub API tokens and interacts with sophisticated LLMs, demands stringent security protocols. This document outlines the procedures for reporting vulnerabilities and maintaining the security of this high-velocity toolkit.

## 1. Reporting a Vulnerability

We utilize the GitHub Security Advisory feature for swift, confidential resolution of security flaws. **This is the mandatory and preferred method for reporting.**

If you believe you have found a security vulnerability in this project, please report it immediately:

1.  **Use GitHub Private Vulnerability Reporting:** Navigate to the project’s **Security tab** on GitHub at `https://github.com/chirag127/PRFusion-AI-Powered-GitHub-Automation-CLI-Toolkit/security` and select **"Report a vulnerability."**
2.  **Provide Details:** Clearly describe the vulnerability, the steps required to reproduce it, the affected versions, and the potential impact.
3.  **Discretion:** Please do not disclose the vulnerability publicly until it has been patched and announced by the maintenance team. Public disclosure of confirmed, unpatched vulnerabilities will be treated as a violation of this policy.

We aim to acknowledge receipt of the report within 48 hours and provide an estimated timeline for remediation.

## 2. Supported Versions

Only the most recent major and minor versions of Python are actively supported and receive security patches. Using an unsupported version poses a significant security risk due to lack of updates for known vulnerabilities.

| Version | Status | Supported Python Range |
| :--- | :--- | :--- |
| **Latest Major Release** | :white_check_mark: Maintained | Python 3.11, 3.12 |
| **Previous Major Release** | :x: Unsupported | Python 3.10 and older |

We strongly recommend upgrading to the latest stable Python environment as defined in the project's dependency specifications (`pyproject.toml`).

## 3. Security Architecture and Best Practices

### A. CI/CD Pipeline Scrutiny
Our continuous integration process (`.github/workflows/ci.yml`) includes mandatory security checks:
*   **Dependency Scanning:** We utilize `uv` and automated tools (such as Bandit, Trivy, or Snyk) to scan dependencies against known CVE databases during every build.
*   **Static Analysis:** Code is regularly scanned for common security anti-patterns and injection risks.
*   **Secret Management:** GitHub Actions secrets are strictly limited in scope and time-bound. Access tokens are never hardcoded and are masked in logs.

### B. API Key Management (Zero Trust)
*   **Environment Variables:** All sensitive keys (GitHub PATs, Gemini API keys) MUST be loaded exclusively via secure environment variables (`$GITHUB_TOKEN`, `$GEMINI_API_KEY`).
*   **Principle of Least Privilege (PoLP):** The application design adheres to PoLP, requesting only the minimum required GitHub scopes necessary for automation tasks (e.g., read/write access only to pull request metadata).

### C. Dependency Auditing
We maintain deterministic and verifiable dependency trees using `uv`'s locking mechanisms. Any third-party dependencies flagged by automated scanners must be promptly evaluated, updated, or replaced if a security risk is identified.

## 4. Security Updates and Disclosure

Once a vulnerability is confirmed and a patch is ready, the following rigorous steps ensure secure deployment:

1.  A new patch release (or minor version) of `PRFusion-AI-Powered-GitHub-Automation-CLI-Toolkit` is immediately published.
2.  A GitHub Security Advisory is publicly disclosed, detailing the vulnerability and the fix, allowing users to rapidly assess risk and update.
3.  Release notes explicitly mention security fixes and required user actions.