# Contributing to PRFusion

Thank you for your interest in contributing to PRFusion! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/PRFusion.git
   cd PRFusion
   ```
3. **Install dependencies**
   ```bash
   uv venv
   uv sync
   ```
4. **Create a branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```

## 📁 Project Structure

```
PRFusion/
├── apex_optimizer/     # Core library
├── templates/          # Astro website templates
├── tests/              # Test suite
├── .github/            # GitHub Actions & templates
└── joules_daily_runner.py  # Main orchestrator
```

## 🧪 Testing

Run tests before submitting:

```bash
python -m pytest tests/ -v
```

Target 100% branch coverage for core modules.

## 📝 Commit Messages

Follow [Conventional Commits](https://conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance

Example: `feat: add short naming for repositories`

## 🔀 Pull Requests

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Use the PR template

## 📜 Code Style

- **Python:** Follow PEP 8, use Ruff for linting
- **TypeScript:** Use Biome for formatting
- **Naming:** camelCase for functions, PascalCase for classes

## 🔒 Security

- Never commit API keys or secrets
- Use `.env` for local development
- Report vulnerabilities via [SECURITY.md](SECURITY.md)

## 📄 License

By contributing, you agree that your contributions will be licensed under CC BY-NC 4.0.

---

**Questions?** Open an issue or reach out to [@chirag127](https://github.com/chirag127).
