import os
import time
import logging
import asyncio
import concurrent.futures
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Adjust path to import from src
import sys
sys.path.append(os.getcwd())

from src.ai.unified_client import UnifiedAIClient
from src.ai.models import UNIFIED_MODEL_CHAIN

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("PolymorphsGenerator")

OUTPUT_DIR = Path("polymorphs")
OUTPUT_DIR.mkdir(exist_ok=True)

COMMON_PROMPT = """
Create a single-file, premium, futuristic landing page for a company called '{model_display_name}'.
The design must be "Wow" quality:
1. Use a dark theme with vibrant, glowing gradients (neon blue, purple, magenta).
2. Implement Glassmorphism for cards and sections.
3. Add complex CSS animations (floating elements, smooth transitions, keyframes).
4. Sections: Hero (with headline), Features (3-4 glass cards), About (minimal), Contact.
5. Use highly polished typography (Inter or Roboto via Google Fonts).
6. Fully responsive.
7. Output pure HTML/CSS/JS in a single file. No external css/js files (except fonts).
"""

SIDEBAR_CSS = """
<style>
/* Polymorphs Sidebar */
#pm-sidebar {
    position: fixed;
    top: 0;
    right: 0;
    width: 260px;
    height: 100vh;
    background: rgba(10, 10, 10, 0.85);
    backdrop-filter: blur(12px);
    border-left: 1px solid rgba(255, 255, 255, 0.1);
    z-index: 9999;
    padding: 20px;
    overflow-y: auto;
    font-family: 'Inter', sans-serif;
    transform: translateX(100%);
    transition: transform 0.3s ease;
    box-shadow: -5px 0 25px rgba(0,0,0,0.5);
}
#pm-sidebar.open {
    transform: translateX(0);
}
#pm-toggle {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 10000;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(5px);
    border: 1px solid rgba(255,255,255,0.2);
    color: white;
    padding: 10px 15px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.2s;
}
#pm-toggle:hover {
    background: rgba(255, 255, 255, 0.2);
}
.pm-item {
    display: block;
    padding: 12px;
    margin-bottom: 8px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 6px;
    color: #ccc;
    text-decoration: none;
    transition: all 0.2s;
    font-size: 0.9em;
}
.pm-item:hover {
    background: rgba(255, 255, 255, 0.1);
    color: white;
    transform: translateX(-5px);
    border-color: rgba(64, 224, 208, 0.4);
}
.pm-item .size {
    font-size: 0.75em;
    color: rgba(255, 255, 255, 0.5);
    display: block;
    margin-top: 4px;
}
.pm-item.active {
    border-color: #00f2ea;
    background: rgba(0, 242, 234, 0.05);
    color: white;
}
.pm-title {
    color: white;
    font-size: 1.1em;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    letter-spacing: 1px;
    text-transform: uppercase;
    font-weight: 700;
}
</style>
"""

SIDEBAR_JS = """
<script>
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.createElement('button');
    btn.id = 'pm-toggle';
    btn.innerText = '🔮 POLYMORPHS';
    document.body.appendChild(btn);

    const sidebar = document.createElement('div');
    sidebar.id = 'pm-sidebar';
    sidebar.innerHTML = `{SIDEBAR_CONTENT}`;
    document.body.appendChild(sidebar);

    btn.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        btn.innerText = sidebar.classList.contains('open') ? '✕ CLOSE' : '🔮 POLYMORPHS';
    });
});
</script>
"""

def generate_content_for_target(client: UnifiedAIClient, target: Dict[str, Any]) -> Dict[str, Any]:
    """Generate content for a target. Returns dict with content/target if success, else None."""
    slug = target['slug']
    display_name = f"{target['name']} ({target['provider'].title()})"
    logger.info(f"🎨 Generating content for {display_name}...")

    prompt = COMMON_PROMPT.format(model_display_name=display_name)
    provider = client.providers.get(target['provider'])

    if not provider:
        return None

    try:
        # Use a generous timeout
        result = provider.chat_completion(
            prompt=prompt,
            system_prompt="You are a world-class frontend engineer and UI/UX designer.",
            model=target['model_id'],
            max_tokens=8000,
            temperature=0.7,
            timeout=180
        )

        if result.success:
            content = result.content
            if "```html" in content:
                content = content.split("```html")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            return {"target": target, "content": content}
        else:
            logger.warning(f"❌ Failed {slug}: {result.error}")
            return None
    except Exception as e:
        logger.error(f"❌ Exception {slug}: {e}")
        return None

def main():
    start_time = time.time()

    # Init client
    client = UnifiedAIClient()

    # 1. Identify ALL Targets (>100B)
    sorted_targets = []
    sorted_models = sorted([m for m in UNIFIED_MODEL_CHAIN if m.size_billions >= 100],
                          key=lambda x: x.size_billions, reverse=True)

    for model in sorted_models:
        # Slug from unique model name
        slug = model.name.lower().replace(".", "-").replace(" ", "-")
        sorted_targets.append({
            "slug": slug,
            "name": model.name,
            "provider": model.provider,
            "model_id": model.api_model_id,
            "size": model.size_billions,
            "include_in_sidebar": model.include_in_sidebar
        })

    logger.info(f"Targeting {len(sorted_targets)} model-provider pairs...")

    # 2. Concurrent Generation
    successful_results = []
    # Max workers increased slightly since we are mostly IO bound waiting for API
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        futures = {executor.submit(generate_content_for_target, client, t): t for t in sorted_targets}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                successful_results.append(res)

    # Sort successes by size again (to ensure sidebar order matches logic)
    successful_results.sort(key=lambda x: x['target']['size'], reverse=True)

    logger.info(f"✅ Successful Generations: {len(successful_results)}")

    if not successful_results:
        logger.error("No sites generated. Exiting.")
        return

    # 3. Build Sidebar (Only successes that opted-in)
    # The user asked for "Bing of the hundred billion parameter name... in the home page Only in the sidebar"
    # Sidebar lists all generated sites.
    sidebar_content = '<div class="pm-title">🔮 Polymorphs</div>'
    for item in successful_results:
        t = item['target']
        if t['include_in_sidebar']:
            disp = f"{t['name']} <span class='size'>{t['size']}B • {t['provider'].title()}</span>"
            link = f"../{t['slug']}.html"
            sidebar_content += f'<a href="{link}" data-slug="{t["slug"]}" class="pm-item">{disp}</a>'

    sidebar_content_js = sidebar_content.replace('`', '\\`').replace('$', '\\$')

    # 4. Inject and Write
    for item in successful_results:
        t = item['target']
        content = item['content']
        slug = t['slug']

        # Only inject sidebar if this model opted-in
        if t['include_in_sidebar']:
            final_sidebar = SIDEBAR_JS.replace("{SIDEBAR_CONTENT}", sidebar_content_js.replace(f'data-slug="{slug}"', 'data-slug="{slug}" class="pm-item active"'))

            if "</body>" in content:
                content = content.replace("</body>", f"{SIDEBAR_CSS}\n{final_sidebar}\n</body>")
            else:
                content += f"\n{SIDEBAR_CSS}\n{final_sidebar}"

        target_dir = OUTPUT_DIR / slug
        target_dir.mkdir(exist_ok=True)
        with open(target_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(content)

    # 5. Set Default (Largest Successful)
    largest = successful_results[0]
    slug = largest['target']['slug']
    logger.info(f"👑 Setting Default Site to: {slug}")

    src_path = OUTPUT_DIR / slug / "index.html"
    if src_path.exists():
        with open(src_path, "r", encoding="utf-8") as f:
            main_content = f.read()
        # Fix links for root index.html ( "../slug" -> "polymorphs/slug" )
        main_content = main_content.replace('href="../', 'href="polymorphs/')

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(main_content)

    logger.info(f"🚀 Done in {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    main()
