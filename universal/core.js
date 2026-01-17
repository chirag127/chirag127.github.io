/* UNIVERSAL CORE ENGINE v2.1
   The Heart of the Universal Architecture.
   - Injects Global Styles
   - Injects Header/Footer
   - Loads Modular Configuration
   - Orchestrates ALL Integrations with Fallback Support
*/

(async function() {
  console.log("🚀 Launching Universal Engine v2.1 (Comprehensive)...");

  // 1. Determine Base URL
  const isLocal = ['localhost', '127.0.0.1'].includes(window.location.hostname);
  const U_PATH = '/universal';

  // 2. Inject CSS
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = `${U_PATH}/style.css`;
  document.head.appendChild(link);

  // 3. Inject Google Fonts (Inter)
  const fontPreconnect = document.createElement('link');
  fontPreconnect.rel = 'preconnect';
  fontPreconnect.href = 'https://fonts.googleapis.com';
  document.head.appendChild(fontPreconnect);

  const fontLink = document.createElement('link');
  fontLink.rel = 'stylesheet';
  fontLink.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap';
  document.head.appendChild(fontLink);

  // 4. Inject Header & Footer (Shared UI)
  async function loadUI() {
    // Header
    const header = document.createElement('header');
    header.className = 'apex-header';
    header.innerHTML = `
      <div class="apex-nav-container">
        <a href="/" class="apex-logo">
          <div class="apex-logo-icon">C</div>
          <span>Chirag Hub</span>
        </a>
        <nav class="apex-nav-links">
          <a href="/">Tools</a>
          <a href="https://github.com/chirag127" target="_blank">GitHub</a>
        </nav>
        <div class="apex-controls">
            <button id="themeToggle" class="theme-toggle" aria-label="Toggle Theme">
                <svg class="sun-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" width="20" height="20"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                <svg class="moon-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" width="20" height="20" style="display:none;"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
            </button>
        </div>
      </div>
    `;
    document.body.insertBefore(header, document.body.firstChild);

    // Footer
    const footer = document.createElement('footer');
    footer.className = 'apex-footer';
    footer.innerHTML = `
      <div class="apex-footer-content">
        <div class="apex-footer-col">
          <h4>Chirag Hub</h4>
          <p>Every tool you need. Free. Private. Forever. 100% browser-powered productivity.</p>
        </div>
        <div class="apex-footer-col">
          <h4>Legal</h4>
          <a href="/privacy">Privacy</a>
          <a href="/terms">Terms</a>
        </div>
        <div class="apex-footer-col">
            <h4>Connect</h4>
            <a href="https://github.com/chirag127" target="_blank">GitHub</a>
        </div>
      </div>
      <div class="apex-copyright">
        © ${new Date().getFullYear()} Chirag Singhal. Open Source.
      </div>
    `;
    document.body.appendChild(footer);

    // Theme Logic
    const toggle = document.getElementById('themeToggle');
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);

    const updateIcons = (theme) => {
        const sun = toggle.querySelector('.sun-icon');
        const moon = toggle.querySelector('.moon-icon');
        if (theme === 'light') {
            document.body.classList.add('light-theme');
            sun.style.display = 'none';
            moon.style.display = 'block';
        } else {
            document.body.classList.remove('light-theme');
            sun.style.display = 'block';
            moon.style.display = 'none';
        }
    };

    updateIcons(savedTheme);

    if(toggle) {
        toggle.addEventListener('click', () => {
          const current = document.documentElement.getAttribute('data-theme');
          const next = current === 'dark' ? 'light' : 'dark';
          document.documentElement.setAttribute('data-theme', next);
          localStorage.setItem('theme', next);
          updateIcons(next);
        });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadUI);
  } else {
    loadUI();
  }

  // 5. Script Loader Helper (returns Promise)
  function loadScript(src, attrs = {}) {
    return new Promise((resolve, reject) => {
      // Check if already loaded
      if (document.querySelector(`script[src="${src}"]`)) {
        resolve(null);
        return;
      }

      const s = document.createElement('script');
      s.src = src;
      Object.keys(attrs).forEach(k => s.setAttribute(k, attrs[k]));
      s.async = true;
      s.onload = () => resolve(s);
      s.onerror = (e) => {
        console.warn(`Failed to load: ${src}`);
        reject(e);
      };
      document.head.appendChild(s);
    });
  }

  // 6. Safe Dynamic Import Helper
  async function safeImport(path) {
    try {
      return await import(path);
    } catch (e) {
      console.warn(`Import failed: ${path}`, e.message);
      return null;
    }
  }

  // 7. Load Modular Configuration
  const configModule = await safeImport(`${U_PATH}/config/index.js`);
  if (!configModule) {
    console.error("❌ Failed to load configuration");
    return;
  }

  const { SITE_CONFIG, priorities } = configModule;

  // Make config globally available
  window.SITE_CONFIG = SITE_CONFIG;
  window.CONFIG_PRIORITIES = priorities;

  // 8. Load and Initialize All Integrations
  const integrationsModule = await safeImport(`${U_PATH}/integrations/index.js`);

  if (integrationsModule) {
    const {
      analyticsProviders,
      monitoringProviders,
      adsProviders,
      chatProviders,
      engagementProviders,
      initCategory,
      initWithFallback
    } = integrationsModule;

    // Initialize all analytics (ALL enabled for maximum data)
    console.log("📊 Loading Analytics...");
    initCategory(analyticsProviders, SITE_CONFIG, loadScript, 'Analytics');

    // Initialize all monitoring (redundancy is good)
    console.log("🔍 Loading Monitoring...");
    initCategory(monitoringProviders, SITE_CONFIG, loadScript, 'Monitoring');

    // Initialize all ads (maximize revenue)
    console.log("💰 Loading Monetization...");
    initCategory(adsProviders, SITE_CONFIG, loadScript, 'Ads');

    // Chat - use fallback pattern (only one widget)
    console.log("💬 Loading Chat...");
    if (priorities?.chat) {
      initWithFallback(priorities.chat, chatProviders, SITE_CONFIG, loadScript, 'Chat');
    } else {
      initCategory(chatProviders, SITE_CONFIG, loadScript, 'Chat');
    }

    // Engagement
    console.log("🎯 Loading Engagement...");
    if (engagementProviders) {
      initCategory(engagementProviders, SITE_CONFIG, loadScript, 'Engagement');
    }
  }

  // 9. Load Firebase (ES Module) - Optional
  safeImport(`${U_PATH}/firebase-modules.js`)
    .then(fb => {
      if (fb) console.log("🔥 Firebase Modules Loaded");
    });

  // 10. Report loaded stats
  const countEnabled = (config) => {
    return Object.values(config || {}).filter(v => v && typeof v === 'object' && v.enabled).length;
  };

  console.log(`✨ Universal Engine v2.1 initialized!`);
  console.log(`   📊 Analytics: ${countEnabled(SITE_CONFIG)} providers`);
  console.log(`   💰 Monetization active`);
  console.log(`   🔍 Monitoring active`);

})();
