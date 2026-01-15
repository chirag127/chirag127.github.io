# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.x.x   | :white_check_mark: |
| < 2.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: **whyiswhen@gmail.com**

Include:
- Type of issue (e.g., API key exposure, injection, etc.)
- Full paths of source file(s) related to the issue
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue

## Response Timeline

- **Acknowledgment:** Within 48 hours
- **Initial assessment:** Within 7 days
- **Resolution:** Dependent on severity, typically within 30 days

## Security Best Practices

This project follows these security practices:

1. **API Keys:** All API keys are stored in environment variables, never in code
2. **Input Validation:** All user inputs are sanitized
3. **Dependencies:** Regular dependency audits via Dependabot
4. **No Server Side:** Frontend-only architecture minimizes attack surface

## Scope

The following are in scope for security reports:
- Main PRFusion repository
- Generated tool repositories
- GitHub Actions workflows

Out of scope:
- Third-party services (GitHub, Jules, Cerebras, etc.)
- Social engineering attacks
- Denial of service attacks

---

Thank you for helping keep PRFusion and its users safe!
