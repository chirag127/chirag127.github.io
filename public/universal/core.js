/**
 * APEX UNIVERSAL CORE (v3.0.0 - Jan 2026)
 * ==========================================
 * The single source of truth for 450+ tool sites.
 * Handles:
 * 1. Configuration Loading (SITE_CONFIG)
 * 2. Analytics Injection (Privacy-First)
 * 3. Shared UI (Header, Footer, Glassmorphism)
 * 4. Theme State (Dark Mode default)
 */

(function() {
    console.log("🚀 Initializing Apex Universal Engine...");

    // ===========================================
    // 1. CONFIGURATION & HELPERS
    // ===========================================
    const c = window.SITE_CONFIG || {};

    // Inject CSS
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://chirag127.github.io/universal/style.css'; // Will be strictly relative in dev? No, absolute for autonomy.
    // For local dev, we might fallback or assumed relative path if running on localhost.
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        link.href = '/universal/style.css';
    }
    document.head.appendChild(link);

    function loadScript(src, attrs = {}) {
        const s = document.createElement('script');
        s.src = src;
        Object.keys(attrs).forEach(k => s.setAttribute(k, attrs[k]));
        s.async = true;
        document.head.appendChild(s);
    }

    // ===========================================
    // 2. ANALYTICS STACK (GDPR COMPLIANT)
    // ===========================================
    function initAnalytics() {
        if (!c) return;

        // GA4
        if (c.ga4 && c.ga4.id) {
            loadScript(`https://www.googletagmanager.com/gtag/js?id=${c.ga4.id}`);
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', c.ga4.id);
        }

        // Clarity
        if (c.clarity && c.clarity.id) {
            (function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];
            y.parentNode.insertBefore(t,y);})(window, document, "clarity", "script", c.clarity.id);
        }

        // Cloudflare
        if (c.cloudflare && c.cloudflare.token) {
            loadScript('https://static.cloudflareinsights.com/beacon.min.js', {'data-cf-beacon': `{"token": "${c.cloudflare.token}"}`});
        }

        // PostHog
        if (c.posthog && c.posthog.key) {
             !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
             posthog.init(c.posthog.key,{api_host:c.posthog.host || 'https://us.i.posthog.com'});
        }

        // Tawk.to
        if (c.tawk && c.tawk.src) {
            var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
            s1.async=true; s1.src=c.tawk.src; s1.charset='UTF-8'; s1.setAttribute('crossorigin','*');
            s0.parentNode.insertBefore(s1,s0);
        }
    }

    // ===========================================
    // 3. UI INJECTION (HEADER/FOOTER)
    // ===========================================
    function injectUI() {
        // Header
        const header = document.createElement('header');
        header.className = 'apex-header';
        header.innerHTML = `
            <div class="apex-nav-container">
                <a href="/" class="apex-logo">
                    <span class="apex-logo-icon">⚡</span>
                    <span class="apex-logo-text">127.0.0.1</span>
                </a>
                <nav class="apex-nav-links">
                    <a href="https://chirag127.github.io/tools">Tools</a>
                    <a href="https://chirag127.github.io/portfolio">Portfolio</a>
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
                    <a href="https://github.com/chirag127">GitHub</a>
                    <a href="#">Support</a>
                </div>
                <div class="apex-footer-col">
                    <h4>Legal</h4>
                    <a href="#">Privacy</a>
                    <a href="#">Terms</a>
                </div>
            </div>
            <div class="apex-copyright">
                © ${new Date().getFullYear()} Chirag127. Crafted with the Singularity.
            </div>
        `;
        document.body.append(footer);

        // Theme Toggle Logic
        const btn = document.getElementById('apex-theme-toggle');
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

    // ===========================================
    // 4. BOOTSTRAP
    // ===========================================
    document.addEventListener('DOMContentLoaded', () => {
        initAnalytics();
        injectUI();
        console.log("✨ Apex Engine Loaded.");
    });

})();
