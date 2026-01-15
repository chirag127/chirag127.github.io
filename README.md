# PRFusion 🚀

**AI-Powered GitHub Automation Toolkit for Repository Management & Tool Generation**

![PRFusion Banner](https://placehold.co/800x200/1E293B/FFFFFF?text=PRFusion)

[![Build Status](https://img.shields.io/github/actions/workflow/status/chirag127/PRFusion/ci.yml?style=flat-square&logo=github)](https://github.com/chirag127/PRFusion/actions)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-blue?style=flat-square)](LICENSE)

<p align="center">
  <a href="https://buymeacoffee.com/chirag127"><img src="https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me A Coffee"/></a>
  <a href="https://github.com/sponsors/chirag127"><img src="https://img.shields.io/badge/Sponsor-EA4AAA?style=for-the-badge&logo=github-sponsors&logoColor=white" alt="Sponsor"/></a>
</p>

---

## 🌟 Features

### Core Automation
| Feature | Description |
|---------|-------------|
| **PR Batch Merger** | Automatically merge PRs across all your repositories |
| **PR Batch Closer** | Close stale/conflicting PRs in bulk |
| **Jules Integration** | Orchestrate Google Jules AI for intelligent code generation |
| **Trend Discovery** | Aggregate trending topics from 15+ sources |
| **AI Selection** | Use top-tier AI to select best project ideas |

### Repository Generation
| Feature | Description |
|---------|-------------|
| **Short Naming** | SEO-friendly names like `pdf-compress`, `png-jpg`, `yt-download` |
| **Private-First** | New repos created private, manual approval to go public |
| **GitHub Pages** | Automatic static website deployment via Actions |
| **Monetization** | Pre-integrated A-Ads, BuyMeCoffee, Crypto donations |

### AI Providers (6-Provider Fallback)
| Provider | Models | Free Tier |
|----------|--------|-----------|
| **Cerebras** | zai-glm-4.6 (357B), qwen-3-235b, gpt-oss-120b | 30 RPM, 1M tokens/day |
| **Groq** | gpt-oss-120b, llama-3.3-70b | 20 RPM |
| **Gemini** | gemma-3-27b, gemma-3-12b | 30 RPM, 14,400 RPD |
| **Mistral** | mistral-small-3.1-24b | Experiment plan |
| **NVIDIA** | llama-3.3-70b-instruct | 40 RPM |
| **Cloudflare** | llama-3.1-8b | 100k req/day |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git
- GitHub Personal Access Token (with `repo` scope)

### Installation

```bash
# Clone
git clone https://github.com/chirag127/PRFusion.git
cd PRFusion

# Create virtual environment (using uv)
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
uv sync

# Copy environment file
cp .env.example .env
# Edit .env with your API keys
```

### Required API Keys

```env
# REQUIRED
GH_TOKEN=ghp_your_github_token
CEREBRAS_API_KEY=your_cerebras_key

# OPTIONAL but recommended
JULES_API_KEY=your_jules_key
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
```

---

## 📖 Usage

### PR Batch Merger

```bash
# Dry-run (safe - shows what would be merged)
python pr_batch_merger.py --dry-run

# Actually merge PRs
python pr_batch_merger.py --no-dry-run

# Merge with specific method
python pr_batch_merger.py --no-dry-run --merge-method squash

# Filter by repository pattern
python pr_batch_merger.py --repo-filter "pdf-*"
```

### PR Batch Closer

```bash
# Dry-run
DRY_RUN=true python pr_batch_closer.py

# Close all open PRs
DRY_RUN=false python pr_batch_closer.py
```

### Jules Daily Runner

```bash
# Full run (all phases)
python joules_daily_runner.py

# Dry-run mode
python joules_daily_runner.py --dry-run

# Create new repos only
python joules_daily_runner.py --new-only

# Optimize existing repos only
python joules_daily_runner.py --optimize

# Monitor stuck sessions
python joules_daily_runner.py --monitor
```

---

## 📁 Project Structure

```
PRFusion/
├── apex_optimizer/
│   ├── ai/                 # Multi-provider AI clients
│   │   ├── unified_client.py   # 6-provider fallback
│   │   └── providers/      # Individual providers
│   ├── clients/            # External API clients
│   │   ├── github.py       # GitHub REST/GraphQL
│   │   └── jules.py        # Google Jules API
│   ├── trend_discovery/    # 15+ trend sources
│   ├── monetization.py     # Centralized monetization config
│   ├── content_generator.py # Project content generation
│   ├── repository_factory.py # Repo creation with short naming
│   ├── session_manager.py  # Jules session lifecycle
│   └── deduplication.py    # Trend deduplication
├── pr_batch_merger.py      # Batch merge PRs
├── pr_batch_closer.py      # Batch close PRs
├── joules_daily_runner.py  # Main orchestrator
├── .env.example            # Environment template
└── tests/                  # Test suite
```

---

## 💰 Monetization

All generated repositories include pre-configured monetization:

### Integrated Platforms
| Platform | Configuration |
|----------|--------------|
| **A-Ads** | Unit ID: `2424216` (Crypto ads) |
| **Buy Me a Coffee** | [@chirag127](https://buymeacoffee.com/chirag127) |
| **GitHub Sponsors** | [Sponsor](https://github.com/sponsors/chirag127) |
| **Amazon Associates** | Store ID: `chirag127-21` |

### Crypto Donations

| Currency | Address |
|----------|---------|
| **BTC** | `bc1qextzy9thrsta6l355kuwdvggehkkmky0zzjnfl` |
| **ETH** | `0xee4e65aa41bfb2d6649c9d3787ff4747704198de` |
| **SOL** | `C4nXxdbUrpTHsEHm5kPfqCVgVbx5cbD5yZNeBbyzyQSi` |

### UPI (India)
UPI ID: `jiochirag127@ybl`

---

## 🏷️ Repository Naming Convention

**New Short Naming (Jan 2026):**

| Old Name | New Name |
|----------|----------|
| PDF-Compressor-Tool-Web-App | `pdf-compress` |
| PNG-to-JPG-Converter-Online | `png-jpg` |
| YouTube-Video-Downloader-CLI | `yt-download` |
| Password-Generator-Secure | `pass-gen` |
| QR-Code-Generator-Tool | `qr-gen` |

**Rules:**
- Maximum 2-3 words
- Lowercase with hyphens
- Immediately clear purpose
- SEO-friendly and searchable

---

## 🔧 Configuration

### Budget Management

The system enforces a daily session budget (default: 100 sessions/day):

- **10%** for new repository creation
- **90%** for existing repository optimization

### Session States

| State | Auto-Action |
|-------|-------------|
| `AWAITING_PLAN_APPROVAL` | Auto-approve |
| `AWAITING_USER_FEEDBACK` | AI-generated response |
| `PAUSED` | Recovery message |
| `COMPLETED` | Merge PR & cleanup |
| `FAILED` | Log and archive |

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_deduplication.py -v

# With coverage
python -m pytest tests/ --cov=apex_optimizer --cov-report=html
```

---

## 📊 Trend Sources

The system aggregates trends from **15+ sources**:

| Source | Type | Requires API Key |
|--------|------|------------------|
| GitHub Trending | Repositories | No (uses GH_TOKEN) |
| Hacker News | Tech News | No |
| Reddit | Discussions | Optional |
| Product Hunt | Products | Optional |
| arXiv | Research Papers | No |
| Papers With Code | ML Papers | No |
| Dev.to | Articles | Optional |
| Hashnode | Blogs | No |
| Lobsters | Tech Links | No |
| Stack Overflow | Questions | No |
| Hugging Face | Models | Optional |
| Kaggle | Datasets | Optional |
| Semantic Scholar | Academic | Optional |

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feat/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](.github/CONTRIBUTING.md) for detailed guidelines.

---

## 🔒 Security

- All API keys stored in `.env` (never committed)
- Private-first repository creation
- Rate limiting and exponential backoff
- See [SECURITY.md](.github/SECURITY.md) for reporting vulnerabilities

---

## 📄 License

This project is licensed under the [CC BY-NC 4.0](LICENSE) license.

---

## 👤 Author

**Chirag Singhal** - Software Engineer · Backend & GenAI Specialist

- 🌐 Website: [chirag127.github.io](https://chirag127.github.io)
- 💼 GitHub: [@chirag127](https://github.com/chirag127)
- 💼 LinkedIn: [chirag-singhal1](https://linkedin.com/in/chirag-singhal1)
- ☕ Buy Me a Coffee: [chirag127](https://buymeacoffee.com/chirag127)
- ❤️ Sponsor: [GitHub Sponsors](https://github.com/sponsors/chirag127)

---

<p align="center">
  <strong>Made with ❤️ by Chirag Singhal</strong><br>
  <sub>Powered by Cerebras, Gemini, Groq, and Jules AI</sub>
</p>