# Chirag Hub Generation Prompts

This document contains all prompts used to generate websites for Chirag Hub and tool projects.

---

## 1. Hub Homepage Generation Prompt

Used by `scripts/generate_multiverse_hub.py` to generate alternative hub homepages.

```text
ROLE: You are the Apex Technical Authority (Jan 2026 Standards).
Expert Frontend Architect with 40+ years experience at Google/DeepMind.

TASK: Generate a COMPLETE, PRODUCTION-READY Chirag Hub homepage.

CONTEXT:
- Chirag Hub is a collection of 450+ free, privacy-focused browser tools
- All tools run 100% client-side (no server uploads)
- The homepage displays all GitHub repositories as tool cards
- Users can filter by category and search

REQUIREMENTS:

1. DATA FETCHING:
   - Fetch repos from: https://api.github.com/users/chirag127/repos
   - Paginate (100 per page, up to 10 pages)
   - Filter out forks and excluded repos: ['chirag127.github.io', 'chirag127']
   - Extract: name, description, stars, has_pages, pushed_at

2. UI COMPONENTS:
   - Hero section with gradient text and ambient glow
   - Stats bar: Tool count, Stars, "0 Trackers"
   - Search box with glass effect (pill shape, focus glow)
   - Category filter pills: All, PDF, Image, Media, Dev, Text, Math, Finance, Health, Convert, Security, Games
   - Responsive grid of tool cards (min-width 340px)
   - Each card: icon, title, badge, description, stars, date

3. CATEGORY DETECTION:
   Use keywords to auto-categorize repos:
   - pdf: ['pdf', 'document', 'split', 'merge']
   - image: ['image', 'photo', 'png', 'jpg', 'svg', 'crop', 'resize']
   - media: ['video', 'audio', 'mp3', 'mp4', 'youtube']
   - dev: ['json', 'xml', 'sql', 'html', 'css', 'uuid', 'api']
   - text: ['text', 'word', 'markdown', 'diff', 'ascii']
   - math: ['math', 'calculator', 'algebra', 'geometry']
   - finance: ['loan', 'mortgage', 'tax', 'salary', 'investment']
   - health: ['bmi', 'calorie', 'body', 'health']
   - converter: ['convert', 'unit', 'length', 'weight']
   - security: ['password', 'hash', 'encrypt']
   - game: ['game', 'puzzle', 'sudoku', 'wordle']

4. DESIGN (2026 SPATIAL-GLASS):
   - Background: #030712 (dark)
   - Glass effects: backdrop-filter: blur(20px)
   - Primary gradient: linear-gradient(135deg, #6366f1, #ec4899)
   - Card hover: translateY(-8px), glow shadow
   - Animations: fadeInUp, scale on click

5. CRITICAL REQUIREMENTS:
   - Single index.html file (inline CSS + JS)
   - Include Universal Engine scripts in <head>:
     <script src="https://chirag127.github.io/universal/config.js" defer></script>
     <script src="https://chirag127.github.io/universal/core.js" defer></script>
   - NO <header> or <footer> tags (Universal Engine injects them)
   - Wrap content in <main> with padding-top: 80px

6. MULTIVERSE SIDEBAR:
   Include a right-side toggle sidebar with these alternative hub links:
   {sidebar_links}

OUTPUT: Complete index.html with all HTML, CSS (in <style>), and JS (in <script>).
Return ONLY the code, wrapped in ```html blocks.
```

---

## 2. Tool Website Generation Prompt

Used by `scripts/generate_projects.py` to generate individual tool websites.

```text
ROLE: You are the Apex Technical Authority (Jan 2026 Standards).

TASK: Generate a COMPLETE, PRODUCTION-READY tool website for: "{tool_name}"

METADATA:
- Title: {title}
- Description: {description}
- Features: {features}
- Category: {category}

RESEARCH CONTEXT:
{research_context}

REQUIREMENTS:

1. ARCHITECTURE (FRONTEND-ONLY):
   - ALL processing runs client-side in the browser
   - NO fetch() to external APIs for processing
   - Use approved libraries via CDN

2. UNIVERSAL ENGINE INTEGRATION:
   - Include in <head>:
     <script src="https://chirag127.github.io/universal/config.js" defer></script>
     <script src="https://chirag127.github.io/universal/core.js" defer></script>
   - DO NOT create <header> or <footer> (injected by Universal Engine)
   - Wrap ALL content in <main> with padding-top: 80px

3. HTML STRUCTURE:
   - <input type="file" id="fileInput"> (hidden)
   - <label id="dropZone"> (drag-drop area)
   - <button id="actionBtn"> (main CTA, disabled by default)
   - <div id="statusArea"> (progress, file list)
   - <div id="resultsContent"> (output/download)

4. JAVASCRIPT QUALITY (ZERO RUNTIME ERRORS):
   - Validate all inputs before processing
   - Check element existence: if (element) { ... }
   - Wrap async operations in try-catch
   - Show user-friendly errors in UI
   - Use IIFE pattern, no global variables

5. DESIGN (2026 SPATIAL-ADAPTIVE):
   - Dark theme (#030712 background)
   - Glass effects (backdrop-filter: blur)
   - Gradient accents
   - Kinetic feedback (scale on click)
   - Smooth transitions (0.3s cubic-bezier)

6. MULTIVERSE SIDEBAR:
   Include right-side toggle sidebar with alternative versions:
   {sidebar_links}

OUTPUT: Single index.html with all HTML, CSS (in <style>), JS (in <script>).
Return ONLY the code in ```html blocks.
```

---

## 3. Sidebar HTML Template

Injected into all generated pages:

```html
<style>
/* Multiverse Sidebar */
#mv-sidebar {
    position: fixed;
    top: 0;
    right: 0;
    width: 280px;
    height: 100vh;
    background: rgba(10, 10, 10, 0.92);
    backdrop-filter: blur(16px);
    border-left: 1px solid rgba(255, 255, 255, 0.08);
    z-index: 9999;
    padding: 24px 16px;
    overflow-y: auto;
    font-family: 'Inter', system-ui, sans-serif;
    transform: translateX(100%);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: -8px 0 32px rgba(0,0,0,0.5);
}
#mv-sidebar.open { transform: translateX(0); }
#mv-toggle {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 10000;
    background: rgba(99, 102, 241, 0.15);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #a5b4fc;
    padding: 10px 16px;
    border-radius: 12px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.85rem;
    transition: all 0.2s;
}
#mv-toggle:hover {
    background: rgba(99, 102, 241, 0.25);
    transform: scale(1.02);
}
.mv-title {
    color: #f9fafb;
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.mv-item {
    display: block;
    padding: 14px 12px;
    margin-bottom: 8px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 10px;
    color: #9ca3af;
    text-decoration: none;
    transition: all 0.2s;
    font-size: 0.9rem;
}
.mv-item:hover {
    background: rgba(99, 102, 241, 0.1);
    border-color: rgba(99, 102, 241, 0.3);
    color: #f9fafb;
    transform: translateX(-4px);
}
.mv-item.active {
    background: rgba(99, 102, 241, 0.15);
    border-color: rgba(99, 102, 241, 0.4);
    color: #f9fafb;
}
.mv-item .mv-size {
    display: block;
    font-size: 0.75rem;
    color: rgba(255,255,255,0.4);
    margin-top: 4px;
}
</style>

<script>
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.createElement('button');
    btn.id = 'mv-toggle';
    btn.innerHTML = '⚡ MULTIVERSE';
    document.body.appendChild(btn);

    const sidebar = document.createElement('div');
    sidebar.id = 'mv-sidebar';
    sidebar.innerHTML = `
        <div class="mv-title">🌐 Multiverse</div>
        {sidebar_items}
    `;
    document.body.appendChild(sidebar);

    btn.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        btn.innerHTML = sidebar.classList.contains('open') ? '✕ CLOSE' : '⚡ MULTIVERSE';
    });
});
</script>
```

---

## Variables Reference

| Variable | Description |
|----------|-------------|
| `{tool_name}` | Repository/tool name (e.g., "pdf-merger") |
| `{title}` | Display title (e.g., "PDF Merger Pro") |
| `{description}` | SEO meta description |
| `{features}` | List of features to implement |
| `{category}` | Tool category (pdf, image, etc.) |
| `{research_context}` | Web research results for libraries/best practices |
| `{sidebar_links}` | JSON array of sidebar model links |
| `{sidebar_items}` | Pre-rendered HTML sidebar link items |
