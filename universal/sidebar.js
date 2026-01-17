/**
 * Multiverse Sidebar Component
 *
 * Automatically adds a toggle sidebar with links to alternative
 * AI-generated versions of the current page.
 *
 * Usage: Include this script and call:
 *   MultiverseSidebar.init(models, options)
 *
 * Where models is an array of:
 *   { name: "Model Name", slug: "model-slug", size: 405.0, provider: "Nvidia" }
 */

const MultiverseSidebar = (function() {
    'use strict';

    const STYLES = `
        #mv-sidebar {
            position: fixed;
            top: 0;
            right: 0;
            width: 300px;
            height: 100vh;
            background: rgba(10, 10, 10, 0.95);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-left: 1px solid rgba(255, 255, 255, 0.08);
            z-index: 9999;
            padding: 24px 16px;
            overflow-y: auto;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            transform: translateX(100%);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: -10px 0 40px rgba(0,0,0,0.6);
        }
        #mv-sidebar.open {
            transform: translateX(0);
        }
        #mv-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(168, 85, 247, 0.2));
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(99, 102, 241, 0.3);
            color: #c7d2fe;
            padding: 12px 18px;
            border-radius: 14px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.85rem;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        #mv-toggle:hover {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.35), rgba(168, 85, 247, 0.35));
            transform: scale(1.03);
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
        }
        #mv-toggle:active {
            transform: scale(0.98);
        }
        .mv-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }
        .mv-title {
            color: #f9fafb;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .mv-count {
            background: rgba(99, 102, 241, 0.2);
            color: #a5b4fc;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .mv-section-title {
            color: rgba(255,255,255,0.5);
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin: 20px 0 12px;
            padding: 0 4px;
        }
        .mv-item {
            display: block;
            padding: 14px 14px;
            margin-bottom: 8px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 12px;
            color: #9ca3af;
            text-decoration: none;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            font-size: 0.9rem;
        }
        .mv-item:hover {
            background: rgba(99, 102, 241, 0.12);
            border-color: rgba(99, 102, 241, 0.35);
            color: #f9fafb;
            transform: translateX(-4px);
        }
        .mv-item.active {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(168, 85, 247, 0.15));
            border-color: rgba(99, 102, 241, 0.5);
            color: #f9fafb;
        }
        .mv-item .mv-model-name {
            font-weight: 500;
            margin-bottom: 4px;
            display: block;
        }
        .mv-item .mv-model-meta {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.75rem;
            color: rgba(255,255,255,0.4);
        }
        .mv-item .mv-size {
            background: rgba(255,255,255,0.06);
            padding: 2px 8px;
            border-radius: 4px;
        }
        .mv-item .mv-provider {
            text-transform: capitalize;
        }
        .mv-item.active .mv-model-meta {
            color: rgba(255,255,255,0.6);
        }
        .mv-close-btn {
            background: none;
            border: none;
            color: rgba(255,255,255,0.4);
            cursor: pointer;
            padding: 8px;
            border-radius: 8px;
            transition: all 0.2s;
        }
        .mv-close-btn:hover {
            background: rgba(255,255,255,0.1);
            color: #fff;
        }
    `;

    function injectStyles() {
        if (document.getElementById('mv-styles')) return;
        const style = document.createElement('style');
        style.id = 'mv-styles';
        style.textContent = STYLES;
        document.head.appendChild(style);
    }

    function createToggleButton() {
        const btn = document.createElement('button');
        btn.id = 'mv-toggle';
        btn.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/>
            </svg>
            <span>MULTIVERSE</span>
        `;
        return btn;
    }

    function createSidebar(models, options) {
        const sidebar = document.createElement('div');
        sidebar.id = 'mv-sidebar';

        const currentSlug = options.currentSlug || '';
        const baseUrl = options.baseUrl || 'multiverse_sites';
        const isHub = options.isHub !== false;

        let itemsHtml = '';
        models.forEach((model, index) => {
            const isActive = model.slug === currentSlug;
            const href = isHub
                ? `${baseUrl}/${model.slug}/index.html`
                : `multiverse/${model.slug}/index.html`;

            itemsHtml += `
                <a href="${href}"
                   class="mv-item ${isActive ? 'active' : ''}"
                   data-slug="${model.slug}">
                    <span class="mv-model-name">${model.name}</span>
                    <span class="mv-model-meta">
                        <span class="mv-size">${model.size}B</span>
                        <span class="mv-provider">${model.provider}</span>
                    </span>
                </a>
            `;
        });

        sidebar.innerHTML = `
            <div class="mv-header">
                <div class="mv-title">
                    🌐 Multiverse
                    <span class="mv-count">${models.length}</span>
                </div>
                <button class="mv-close-btn" id="mv-close">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 6L6 18M6 6l12 12"/>
                    </svg>
                </button>
            </div>
            <div class="mv-section-title">Alternative Versions</div>
            ${itemsHtml}
        `;

        return sidebar;
    }

    function init(models, options = {}) {
        if (!models || !models.length) {
            console.warn('[MultiverseSidebar] No models provided');
            return;
        }

        injectStyles();

        const btn = createToggleButton();
        const sidebar = createSidebar(models, options);

        document.body.appendChild(btn);
        document.body.appendChild(sidebar);

        btn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            btn.querySelector('span').textContent =
                sidebar.classList.contains('open') ? 'CLOSE' : 'MULTIVERSE';
        });

        sidebar.querySelector('#mv-close').addEventListener('click', () => {
            sidebar.classList.remove('open');
            btn.querySelector('span').textContent = 'MULTIVERSE';
        });

        // Close on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && sidebar.classList.contains('open')) {
                sidebar.classList.remove('open');
                btn.querySelector('span').textContent = 'MULTIVERSE';
            }
        });

        // Close when clicking outside
        document.addEventListener('click', (e) => {
            if (sidebar.classList.contains('open') &&
                !sidebar.contains(e.target) &&
                !btn.contains(e.target)) {
                sidebar.classList.remove('open');
                btn.querySelector('span').textContent = 'MULTIVERSE';
            }
        });
    }

    return { init };
})();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MultiverseSidebar;
}
