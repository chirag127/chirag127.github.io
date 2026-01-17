# Chirag Hub

**Every tool you need. Free. Private. Forever.**

This repository is the central hub powering an ever-growing ecosystem of browser-based utilities. PDF editing, image conversion, developer tools, calculators, games—all running 100% in your browser with zero uploads.

## Universal Architecture
This project utilizes a unique **Frontend-Only Universal Architecture** to ensure consistency, privacy, and zero server management across hundreds of repositories.

### Core Components
- **`public/universal/config.js`**: The central brain. Defines keys/tokens for all 20+ tracked SaaS services (Analytics, Auth, Ads).
- **`public/universal/core.js`**: The engine. Injected into every satellite tool site. It dynamically builds the Header/Footer and loads the services defined in `config.js`.
- **`public/universal/style.css`**: The skin. Provides the shared "Spatial Glass" design system and dark mode logic.
- **`public/universal/firebase-modules.js`**: The spine. Handles complex Firebase logic (Auth/Firestore) as a native ES Module.

### How it Works
1.  **Hub (`chirag127.github.io`)**: Loads the universal engine to render itself.
2.  **Satellites (e.g., `pdf-merge`)**: Import the engine via `<script src="https://chirag127.github.io/universal/core.js"></script>`.
3.  **Updates**: A single change propagates across the entire network instantly.

## The Complete Toolkit
From PDF manipulation to code formatting—if you need a browser tool, it's here.

| Category | Example Tools |
| :--- | :--- |
| **PDF** | Merge, Split, Compress, OCR, Convert |
| **Image** | Converter, Resize, Crop, SVG Editor, Palette |
| **Dev** | JSON Formatter, Regex Tester, Base64, Cron |
| **Audio** | Cutter, Recorder, BPM Counter |

## Development
To run locally:
```bash
# Clone
git clone https://github.com/chirag127/chirag127.github.io.git
cd chirag127.github.io

# Serve (e.g., using Python)
python -m http.server 8000
```
Open `http://localhost:8000`. The Universal Engine detects `localhost` and loads assets relatively.

## Privacy
- **Client-Side First**: File processing (PDF merging, Image conversion) happens in the browser via WebAssembly/JS libraries. Files are NOT uploaded to our servers.
- **Analytics**: We use privacy-friendly analytics (Plausible, Umami) alongside standard ones to improve the tools.

## License
MIT (c) 2026 Chirag Singhal