/**
 * APEX UNIVERSAL CORE (v3.1.0 - Jan 2026)
 * ==========================================
 * The single source of truth for 450+ tool sites.
 * Handles:
 * 1. Configuration Loading (SITE_CONFIG has already been loaded by config.js)
 * 2. Shared UI (Header, Footer, Glassmorphism)
 * 3. Theme State (Dark Mode default)
 * 4. Firebase Module Loading
 */

(function() {
    console.log("🚀 Initializing Apex Universal Core...");

    // ===========================================
    // 1. CONFIGURATION & HELPERS
    // ===========================================

    // Determine Base URL (handle local vs production)
    const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    const baseUrl = isLocal ? '' : 'https://chirag127.github.io';

    // Inject CSS
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = `${baseUrl}/universal/style.css`;
    document.head.appendChild(link);

    // Inject Fonts (Outfit)
    const fontPreconnect1 = document.createElement('link');
    fontPreconnect1.rel = 'preconnect';
    fontPreconnect1.href = 'https://fonts.googleapis.com';
    document.head.appendChild(fontPreconnect1);

    const fontPreconnect2 = document.createElement('link');
    fontPreconnect2.rel = 'preconnect';
    fontPreconnect2.href = 'https://fonts.gstatic.com';
    fontPreconnect2.crossOrigin = 'anonymous';
    document.head.appendChild(fontPreconnect2);

    const fontLink = document.createElement('link');
    fontLink.href = 'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap';
    fontLink.rel = 'stylesheet';
    document.head.appendChild(fontLink);


    // ===========================================
    // 2. UI INJECTION (HEADER/FOOTER)
    // ===========================================
    function injectUI() {
        // Header
        const header = document.createElement('header');
        header.className = 'apex-header';
        header.innerHTML = `
            <div class="apex-nav-container">
                <a href="${baseUrl}/" class="apex-logo">
                    <span class="apex-logo-icon">⚡</span>
                    <span class="apex-logo-text">127.0.0.1</span>
                </a>
                <nav class="apex-nav-links">
                    <a href="${baseUrl}/">Tools</a>
                    <a href="${baseUrl}/#portfolio">Portfolio</a>
                    <a href="https://github.com/chirag127" target="_blank">GitHub</a>
                </nav>
                <div class="apex-controls">
                     <button id="apex-theme-toggle" aria-label="Toggle Theme">☀</button>
                </div>
            </div>
        `;
        document.body.prepend(header);

        // Footer
        const footer = document.createElement('footer');
        footer.className = 'apex-footer';
        footer.innerHTML = `
            <div class="apex-footer-content">
                <div class="apex-footer-col">
                    <h4>About</h4>
                    <p>Free, client-side tools for everyone. Zero servers, zero data tracking.</p>
                </div>
                <div class="apex-footer-col">
                    <h4>Network</h4>
                    <a href="https://github.com/chirag127" target="_blank">GitHub</a>
                    <a href="mailto:contact@chirag127.com">Contact</a>
                </div>
                <div class="apex-footer-col">
                    <h4>Legal</h4>
                    <a href="${baseUrl}/privacy.html">Privacy</a>
                    <a href="${baseUrl}/terms.html">Terms</a>
                </div>
            </div>
            <div class="apex-copyright">
                © ${new Date().getFullYear()} Chirag127. Crafted with the Singularity.
            </div>
        `;
        document.body.append(footer);

        // Theme Toggle Logic
        const btn = document.getElementById('apex-theme-toggle');
        if (btn) {
            btn.onclick = () => {
                document.body.classList.toggle('light-theme');
                const isLight = document.body.classList.contains('light-theme');
                btn.textContent = isLight ? '☾' : '☀';
                localStorage.setItem('apex-theme', isLight ? 'light' : 'dark');
            };

            // Initialize Theme from Storage
            if (localStorage.getItem('apex-theme') === 'light') {
                document.body.classList.add('light-theme');
                btn.textContent = '☾';
            }
        }
    }

    // ===========================================
    // 3. LOAD FIREBASE MODULE (ESM)
    // ===========================================
    function loadFirebaseEngine() {
        const script = document.createElement('script');
        script.type = 'module';
        script.src = `${baseUrl}/universal/firebase-modules.js`;
        document.body.appendChild(script);
    }

    // ===========================================
    // 4. BOOTSTRAP
    // ===========================================
    document.addEventListener('DOMContentLoaded', () => {
        injectUI();
        loadFirebaseEngine();
        console.log("✨ Apex Engine UI Injected.");
    });

})();
