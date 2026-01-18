# Chirag Hub (chirag127.github.io)

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Websites-450+-blue?style=for-the-badge" alt="Websites Count">
  <img src="https://img.shields.io/badge/Privacy-100%25-green?style=for-the-badge" alt="Privacy">
  <br>
  <strong>The Infinite Website Collection: Free, Private, Browser-Based Generators.</strong>
</p>

[Chirag Hub](https://chirag127.github.io/) is a centralized platform hosting a vast collection of browser-based websites. From PDF manipulation and image conversion to developer utilities and games, every website runs 100% client-side, ensuring your data never leaves your device.

This repository serves as the **central command center** for the Chirag Hub ecosystem. It hosts the main landing page, the "Universal Engine" shared library, and the AI-powered automation scripts that generate and manage the individual website repositories.

---

## ✨ Key Features

### 1. The Universal Engine (`universal/`)
A powerful, modular JavaScript framework that unifies the user experience across all websites.
-   **Consistent UI**: Automatically pushes a shared header, footer, and theme system (Dark/Light mode) to every website.
-   **Global Styling**: Injects premium "Spatial Glass" design tokens.
-   **Integration Stack**: Manages analytics, monetization, and engagement features centrally.

### 2. Polymorphs (The Multiverse)
A cutting-edge feature where websites are generated in multiple "variants" by different AI models (e.g., GPT-4, Claude 3.5, Llama 3).
-   **Compare Models**: See how different AIs solve the same coding problem.
-   **AI Native**: The UI allows seamless switching between these AI-generated realities.

### 3. AI-Native "Factory"
The entire ecosystem is self-expanding. Python scripts (`scripts/generate_projects.py`) leverage LLMs to:
-   **Research**: Analyze requirements using web search.
-   **Generate**: Write complete, single-file HTML/JS applications.
-   **Deploy**: Automate GitHub repository creation and Pages deployment.

---

## 🛠️ Architecture

The project follows a **Hub-and-Spoke** model:

```mermaid
graph TD
    A[This Repo (Hub)] -->|Universal Engine| B[Website A]
    A -->|Universal Engine| C[Website B]
    A -->|Universal Engine| D[Website C]
    E[Python Scripts] -->|Generates| B
    E -->|Generates| C
    E -->|Generates| D
    F[index.html] -->|Fetches| B
    F -->|Fetches| C
    F -->|Fetches| D
```

-   **Frontend**: Vanilla HTML5/CSS3/JS. No heavy frameworks.
-   **Automation**: Python 3.10+ (AsyncIO, Pydantic).
-   **Data Source**: GitHub API (The hub fetches your repos dynamically).

---

## 🚀 Getting Started

### Prerequisites
-   Python 3.10+
-   Node.js (optional, for some specific internal scripts)
-   GitHub Personal Access Token (for the generator scripts)

### Installation
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/chirag127/chirag127.github.io.git
    cd chirag127.github.io
    ```

2.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment**:
    Create a `.env` file (see `.env.example`) with your `GH_TOKEN`.

### Usage
-   **Run the Hub Locally**:
    ```bash
    npx serve .
    ```
    Visit `http://localhost:3000` to see the hub.

-   **Generate a New Website** (for authorized users):
    ```bash
    python scripts/generate_projects.py --website "image-compressor"
    ```

---

## 📚 Documentation
For a detailed deep-dive into the repository structure and analysis, see:
👉 [**Repository Review**](docs/REPOSITORY_REVIEW.md)

---

## 🤝 Contributing
We welcome contributions! Please see `CONTRIBUTING.md` (if available) or open an issue to discuss your ideas.
Since this is an automated repo, please be careful when modifying the `scripts/` directory.

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center">
  Made with ❤️ & 🤖 by <a href="https://github.com/chirag127">Chirag Singhal</a>
</p>
