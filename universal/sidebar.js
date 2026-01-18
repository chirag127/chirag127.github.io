/**
 * Polymorphs Sidebar Component
 *
 * Automatically adds a toggle sidebar with links to alternative
 * AI-generated versions of the current page.
 *
 * Usage: Include this script and call:
 *   Polymorphs.init(models, options)
 *
 * Where models is an array of:
 *   { name: "Model Name", slug: "model-slug", size: 405.0, provider: "Nvidia" }
 */

const Polymorphs = (function() {
    'use strict';

    const STYLES = `
        #pm-sidebar {
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
        #pm-sidebar.open {
            transform: translateX(0);
        }
        #pm-toggle {
            position: fixed;
            bottom: 20px;
            left: 20px;
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
        #pm-toggle:hover {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.35), rgba(168, 85, 247, 0.35));
            transform: scale(1.03);
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
        }
        #pm-toggle:active {
            transform: scale(0.98);
        }
        .pm-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }
        .pm-title {
            color: #f9fafb;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .pm-count {
            background: rgba(99, 102, 241, 0.2);
            color: #a5b4fc;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .pm-section-title {
            color: rgba(255,255,255,0.5);
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin: 20px 0 12px;
            padding: 0 4px;
        }
        .pm-item {
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
        .pm-item:hover {
            background: rgba(99, 102, 241, 0.12);
            border-color: rgba(99, 102, 241, 0.35);
            color: #f9fafb;
            transform: translateX(-4px);
        }
        .pm-item.active {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(168, 85, 247, 0.15));
            border-color: rgba(99, 102, 241, 0.5);
            color: #f9fafb;
        }
        .pm-item .pm-model-name {
            font-weight: 500;
            margin-bottom: 4px;
            display: block;
        }
        .pm-item .pm-model-meta {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.75rem;
            color: rgba(255,255,255,0.4);
        }
        .pm-item .pm-size {
            background: rgba(255,255,255,0.06);
            padding: 2px 8px;
            border-radius: 4px;
        }
        .pm-item .pm-provider {
            text-transform: capitalize;
        }
        .pm-item.active .pm-model-meta {
            color: rgba(255,255,255,0.6);
        }
        .pm-close-btn {
            background: none;
            border: none;
            color: rgba(255,255,255,0.4);
            cursor: pointer;
            padding: 8px;
            border-radius: 8px;
            transition: all 0.2s;
        }
        .pm-close-btn:hover {
            background: rgba(255,255,255,0.1);
            color: #fff;
        }
    `;

    function injectStyles() {
        if (document.getElementById('pm-styles')) return;
        const style = document.createElement('style');
        style.id = 'pm-styles';
        style.textContent = STYLES;
        document.head.appendChild(style);
    }

    function createToggleButton() {
        const btn = document.createElement('button');
        btn.id = 'pm-toggle';
        btn.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/>
            </svg>
            <span>POLYMORPHS</span>
        `;
        return btn;
    }

    function createSidebar(models, options) {
        const sidebar = document.createElement('div');
        sidebar.id = 'pm-sidebar';

        const currentSlug = options.currentSlug || '';
        const baseUrl = options.baseUrl || 'polymorphs';
        const isHub = options.isHub !== false;

        let itemsHtml = '';
        models.forEach((model, index) => {
            const isActive = model.slug === currentSlug;

            // Smart path resolution based on current location
            const currentPath = window.location.pathname;
            const isInPolymorphs = currentPath.includes('/polymorphs/');

            // If we're in polymorphs directory, use relative paths
            // Otherwise use absolute paths from root
            const href = isInPolymorphs
                ? `${model.slug}.html`
                : `/${baseUrl}/${model.slug}.html`;

            itemsHtml += `
                <a href="${href}"
                   class="pm-item ${isActive ? 'active' : ''}"
                   data-slug="${model.slug}">
                    <span class="pm-model-name">${model.name}</span>
                    <span class="pm-model-meta">
                        <span class="pm-size">${model.size}B</span>
                        <span class="pm-provider">${model.provider}</span>
                    </span>
                </a>
            `;
        });

        sidebar.innerHTML = `
            <div class="pm-header">
                <div class="pm-title">
                    🔮 Polymorphs
                    <span class="pm-count">${models.length}</span>
                </div>
                <button class="pm-close-btn" id="pm-close">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 6L6 18M6 6l12 12"/>
                    </svg>
                </button>
            </div>
            <div class="pm-section-title">AI Versions</div>
            ${itemsHtml}
        `;

        return sidebar;
    }

    function init(models, options = {}) {
        if (!models || !models.length) {
            console.warn('[Polymorphs] No models provided');
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
                sidebar.classList.contains('open') ? 'CLOSE' : 'POLYMORPHS';
        });

        sidebar.querySelector('#pm-close').addEventListener('click', () => {
            sidebar.classList.remove('open');
            btn.querySelector('span').textContent = 'POLYMORPHS';
        });

        // Close on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && sidebar.classList.contains('open')) {
                sidebar.classList.remove('open');
                btn.querySelector('span').textContent = 'POLYMORPHS';
            }
        });

        // Close when clicking outside
        document.addEventListener('click', (e) => {
            if (sidebar.classList.contains('open') &&
                !sidebar.contains(e.target) &&
                !btn.contains(e.target)) {
                sidebar.classList.remove('open');
                btn.querySelector('span').textContent = 'POLYMORPHS';
            }
        });
    }

    return { init };
})();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Polymorphs;
}
