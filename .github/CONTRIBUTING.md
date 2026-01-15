# Contributing to PRFusion-AI-Powered-GitHub-Automation-CLI-Toolkit

Welcome to the PRFusion project! We are thrilled you're interested in contributing to this advanced AI-powered GitHub automation CLI toolkit. Your contributions help us build a more efficient, intelligent, and scalable solution for repository management.

This document outlines guidelines for contributing to PRFusion. Please read through it carefully before making any contributions.

## 🚀 Getting Started

### 💡 Code of Conduct

We are committed to fostering an open and welcoming environment. All contributors are expected to adhere to our [Code of Conduct](https://github.com/chirag127/PRFusion-AI-Powered-GitHub-Automation-CLI-Toolkit/blob/main/.github/CODE_OF_CONDUCT.md). Please read it to understand the expected behavior and how to report issues.

### 🛠️ Setting Up Your Development Environment

PRFusion is built with Python and utilizes `uv` for dependency management, `Ruff` for linting, and `Pytest` for testing.

1.  **Fork and Clone the Repository:**

    bash
    git clone https://github.com/chirag127/PRFusion-AI-Powered-GitHub-Automation-CLI-Toolkit.git
    cd PRFusion-AI-Powered-GitHub-Automation-CLI-Toolkit
    

2.  **Install `uv`:**

    If you don't have `uv` installed, you can get it via `pip` or other methods:

    bash
    pip install uv
    

3.  **Install Dependencies:**

    Use `uv` to install all project dependencies, including development tools:

    bash
    uv sync
    

4.  **Environment Variables:**

    PRFusion requires certain environment variables for operation, such as your GitHub Personal Access Token and Google Gemini API Key. Create a `.env` file in the root of your project or set these in your shell environment:

    dotenv
    GITHUB_TOKEN=your_github_personal_access_token
    GEMINI_API_KEY=your_google_gemini_api_key
    

    Ensure your GitHub token has the necessary scopes (e.g., `repo`, `workflow`) for the actions you intend to perform.

## ✨ How Can You Contribute?

There are many ways to contribute to PRFusion:

*   **Reporting Bugs:** If you find a bug, please open an issue using our [bug report template](https://github.com/chirag127/PRFusion-AI-Powered-GitHub-Automation-CLI-Toolkit/blob/main/.github/ISSUE_TEMPLATE/bug_report.md). Provide clear steps to reproduce, expected behavior, and actual behavior.
*   **Suggesting Enhancements:** Have an idea for a new feature or an improvement? Open an issue to discuss it.
*   **Writing Code:** Implement new features, fix bugs, or improve existing code.
*   **Improving Documentation:** Help us make our documentation clearer, more complete, or more user-friendly.

## 📝 Development Workflow

### Branching Strategy

We use a `main` branch for stable releases and feature branches for ongoing development:

1.  **Create a new branch** from `main` for your changes:
    bash
    git checkout main
    git pull origin main
    git checkout -b feature/your-feature-name-or-bugfix/issue-number
    
2.  **Make your changes.**
3.  **Commit your changes** with a clear and descriptive message (see [Commit Guidelines](#commit-guidelines)).
4.  **Push your branch** to your forked repository.
5.  **Open a Pull Request** to the `main` branch of the upstream repository.

### Commit Guidelines

We encourage the use of [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) to ensure clear and consistent commit history. Examples:

*   `feat: add new CLI command for batch PR approval`
*   `fix(parser): handle empty response from GitHub API`
*   `docs: update contributing guidelines`
*   `refactor: improve Gemini API error handling`

### Running Tests

Before submitting a Pull Request, ensure all tests pass.

bash
uv run test


We use `Pytest` for unit and integration testing. Please add tests for new features and bug fixes.

### Linting and Formatting

Maintain code quality and consistency with `Ruff`:

bash
uv run lint
uv run format


Ensure your code passes all lint checks and is properly formatted before committing.

### Architectural Principles

We adhere to principles such as SOLID, DRY (Don't Repeat Yourself), and YAGNI (You Aren't Gonna Need It). Prioritize modular, testable, and maintainable code. For AI integrations, ensure clear separation of concerns and robust API contracts for model interactions.

## 📥 Submitting Changes (Pull Requests)

When you're ready to submit your changes, create a Pull Request (PR) to the `main` branch of the `chirag127/PRFusion-AI-Powered-GitHub-Automation-CLI-Toolkit` repository.

*   **Use our [Pull Request Template](https://github.com/chirag127/PRFusion-AI-Powered-GitHub-Automation-CLI-Toolkit/blob/main/.github/PULL_REQUEST_TEMPLATE.md)** to provide all necessary information.
*   **Ensure your PR addresses a single concern** (feature, bug fix, etc.).
*   **All tests must pass.** Our CI pipeline (`.github/workflows/ci.yml`) will run tests and lint checks automatically.
*   **Provide a clear description** of your changes and why they are necessary.
*   **Link to any relevant issues** that your PR resolves.

## 🔒 Security

If you discover any security vulnerabilities, please refer to our [Security Policy](https://github.com/chirag127/PRFusion-AI-Powered-GitHub-Automation-CLI-Toolkit/blob/main/.github/SECURITY.md) for instructions on how to report them responsibly.

## ⚖️ License

By contributing to PRFusion, you agree that your contributions will be licensed under the [CC BY-NC 4.0 License](https://github.com/chirag127/PRFusion-AI-Powered-GitHub-Automation-CLI-Toolkit/blob/main/LICENSE).

Thank you for contributing to PRFusion!