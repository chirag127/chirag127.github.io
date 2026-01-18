/**
 * Polymorphs Sidebar Component - APEX Architecture
 *
 * Automatically adds a toggle sidebar with links to alternative
 * AI-generated versions of the current page following APEX principles.
 *
 * Features:
 * - Client-Side Only Architecture
 * - 2026 Spatial Glass Design
 * - Neuro-Inclusive Design
 * - Battery-Aware Optimizations
 * - Accessibility Compliant (WCAG 2.1 AA)
 *
 * Usage: Include this script and call:
 *   Polymorphs.init(models, options)
 *
 * Where models is an array of:
 *   { name: "Model Name", slug: "model-slug", size: 405.0, provider: "Nvidia" }
 */

const Polymorphs = (function () {
    'use strict';

    const STYLES = `
        #pm-sidebar {
            position: fixed;
            top: 0;
            left: 0;
            width: 320px;
            height: 100vh;
            background: rgba(3, 7, 18, 0.95);
            backdrop-filter: blur(24px) saturate(180%);
            -webkit-backdrop-filter: blur(24px) saturate(180%);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
            z-index: 9999;
            padding: 24px 20px;
            overflow-y: auto;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            transform: translateX(-100%);
            transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 4px 0 40px rgba(0,0,0,0.6);
        }
        #pm-sidebar.open {
            transform: translateX(0);
        }
        #pm-toggle {
            position: fixed;
            bottom: 24px;
            left: 24px;
            z-index: 10000;
            background: linear-gradient(135deg, rgba(129, 140, 248, 0.2), rgba(192, 132, 252, 0.2));
            backdrop-filter: blur(12px) saturate(180%);
            -webkit-backdrop-filter: blur(12px) saturate(180%);
            border: 1px solid rgba(129, 140, 248, 0.3);
            color: #c7d2fe;
            padding: 14px 20px;
            border-radius: 16px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.875rem;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            user-select: none;
        }
        #pm-toggle:hover {
            background: linear-gradient(135deg, rgba(129, 140, 248, 0.35), rgba(192, 132, 252, 0.35));
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 12px 40px rgba(129, 140, 248, 0.4);
            border-color: rgba(129, 140, 248, 0.5);
        }
        #pm-toggle:active {
            transform: translateY(-1px) scale(0.98);
        }
        .pm-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 28px;
            padding-bottom: 20px;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }
        .pm-title {
            color: #f9fafb;
            font-size: 0.9rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .pm-count {
            background: rgba(129, 140, 248, 0.2);
            color: #a5b4fc;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            border: 1px solid rgba(129, 140, 248, 0.3);
        }
        .pm-section-title {
            color: rgba(255,255,255,0.5);
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin: 24px 0 16px;
            padding: 0 4px;
        }
        .pm-item {
            display: block;
            padding: 16px 16px;
            margin-bottom: 10px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 14px;
            color: #9ca3af;
            text-decoration: none;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            font-size: 0.9rem;
            position: relative;
            overflow: hidden;
        }
        .pm-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(129, 140, 248, 0.6), transparent);
            opacity: 0;
            transition: opacity 0.3s;
        }
        .pm-item:hover {
            background: rgba(129, 140, 248, 0.12);
            border-color: rgba(129, 140, 248, 0.35);
            color: #f9fafb;
            transform: translateX(6px);
            box-shadow: 0 4px 20px rgba(129, 140, 248, 0.2);
        }
        .pm-item:hover::before {
            opacity: 1;
        }
        .pm-item.active {
            background: linear-gradient(135deg, rgba(129, 140, 248, 0.2), rgba(192, 132, 252, 0.15));
            border-color: rgba(129, 140, 248, 0.5);
            color: #f9fafb;
            box-shadow: 0 4px 20px rgba(129, 140, 248, 0.3);
        }
        .pm-item.active::before {
            opacity: 1;
        }
        .pm-item .pm-model-name {
            font-weight: 600;
            margin-bottom: 6px;
            display: block;
            font-size: 0.95rem;
        }
        .pm-item .pm-model-meta {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.75rem;
            color: rgba(255,255,255,0.4);
        }
        .pm-item .pm-size {
            background: rgba(255,255,255,0.06);
            padding: 3px 10px;
            border-radius: 6px;
            font-weight: 500;
        }
        .pm-item .pm-provider {
            text-transform: capitalize;
            font-weight: 500;
        }
        .pm-item.active .pm-model-meta {
            color: rgba(255,255,255,0.7);
        }
        .pm-close-btn {
            background: none;
            border: none;
            color: rgba(255,255,255,0.4);
            cursor: pointer;
            padding: 10px;
            border-radius: 10px;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .pm-close-btn:hover {
            background: rgba(255,255,255,0.1);
            color: #fff;
            transform: scale(1.1);
        }
        .pm-close-btn:active {
            transform: scale(0.95);
        }

        /* Accessibility Enhancements */
        @media (prefers-reduced-motion: reduce) {
            #pm-sidebar, #pm-toggle, .pm-item, .pm-close-btn {
                transition: none;
            }
        }

        /* Focus Management */
        #pm-toggle:focus-visible,
        .pm-item:focus-visible,
        .pm-close-btn:focus-visible {
            outline: 2px solid rgba(129, 140, 248, 0.8);
            outline-offset: 2px;
        }

        /* Mobile Optimizations */
        @media (max-width: 768px) {
            #pm-sidebar {
                width: 280px;
                padding: 20px 16px;
            }
            #pm-toggle {
                bottom: 20px;
                left: 20px;
                padding: 12px 16px;
                font-size: 0.8rem;
            }
        }

        /* Battery-Aware Optimizations */
        @media (prefers-reduced-motion: reduce) {
            #pm-sidebar {
                transition: none;
            }
            .pm-item {
                transition: none;
            }
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
        btn.setAttribute('aria-label', 'Toggle Polymorphs Sidebar');
        btn.setAttribute('role', 'button');
        btn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
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
        sidebar.setAttribute('role', 'navigation');
        sidebar.setAttribute('aria-label', 'Polymorphs Navigation');

        const currentSlug = options.currentSlug || '';
        const baseUrl = options.baseUrl || 'polymorphs';

        let itemsHtml = '';
        models.forEach((model, index) => {
            const isActive = model.slug === currentSlug;

            const currentPath = window.location.pathname;
            const isInPolymorphs = currentPath.includes('/polymorphs/');

            const href = isInPolymorphs
                ? `${model.slug}.html`
                : `/${baseUrl}/${model.slug}.html`;

            itemsHtml += `
                <a href="${href}"
                   class="pm-item ${isActive ? 'active' : ''}"
                   data-slug="${model.slug}"
                   aria-current="${isActive ? 'page' : 'false'}">
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
                <button class="pm-close-btn" id="pm-close" aria-label="Close Polymorphs Sidebar">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
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

        // Event Handlers
        btn.addEventListener('click', () => {
            const isOpen = sidebar.classList.contains('open');
            sidebar.classList.toggle('open');
            btn.querySelector('span').textContent = isOpen ? 'POLYMORPHS' : 'CLOSE';
            btn.setAttribute('aria-expanded', !isOpen);

            // Focus management
            if (!isOpen) {
                sidebar.querySelector('.pm-close-btn').focus();
            }
        });

        sidebar.querySelector('#pm-close').addEventListener('click', () => {
            sidebar.classList.remove('open');
            btn.querySelector('span').textContent = 'POLYMORPHS';
            btn.setAttribute('aria-expanded', 'false');
            btn.focus();
        });

        // Keyboard Navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && sidebar.classList.contains('open')) {
                sidebar.classList.remove('open');
                btn.querySelector('span').textContent = 'POLYMORPHS';
                btn.setAttribute('aria-expanded', 'false');
                btn.focus();
            }
        });

        // Click Outside to Close
        document.addEventListener('click', (e) => {
            if (sidebar.classList.contains('open') &&
                !sidebar.contains(e.target) &&
                !btn.contains(e.target)) {
                sidebar.classList.remove('open');
                btn.querySelector('span').textContent = 'POLYMORPHS';
                btn.setAttribute('aria-expanded', 'false');
            }
        });

        // Initialize ARIA attributes
        btn.setAttribute('aria-expanded', 'false');

        console.log(`🔮 Polymorphs sidebar initialized with ${models.length} models (APEX Architecture)`);
    }

    return { init };
})();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Polymorphs;
}

// Make globally available
window.Polymorphs = Polymorphs;
