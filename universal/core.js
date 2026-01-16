/* UNIVERSAL CORE ENGINE
   The Heart of the Universal Architecture.
   - Injects Global Styles
   - Injects Header/Footer
   - Loads Configuration
   - Orchestrates Modular Integrations
*/

(async function() {
  console.log("🚀 Launching Universal Engine...");

  // 1. Determine Base URL
  const isLocal = ['localhost', '127.0.0.1'].includes(window.location.hostname);

  // Correction: Since 'universal' is now at the root of the repo (github.io),
  // on production it is at /universal.
  // Locally (if serving root): /universal.
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
          <p>The Singularity of Free Tools. 450+ privacy-focused utilities running entirely in your browser.</p>
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

  // 5. Config Loading Helper
  function waitForConfig() {
    return new Promise(resolve => {
      if (window.SITE_CONFIG) return resolve(window.SITE_CONFIG);
      let interval = setInterval(() => {
        if (window.SITE_CONFIG) {
          clearInterval(interval);
          resolve(window.SITE_CONFIG);
        }
      }, 50);
    });
  }

  const config = await waitForConfig();

  // 6. Helper: Script Loader
  function loadScript(src, attrs = {}) {
      const s = document.createElement('script');
      s.src = src;
      Object.keys(attrs).forEach(k => s.setAttribute(k, attrs[k]));
      s.async = true;
      document.head.appendChild(s);
  }

  // 7. Dynamic Module Loader
  const integrations = [
    // Analytics
    { key: 'ga4', path: '/integrations/analytics/ga4.js' },
    { key: 'yandex', path: '/integrations/analytics/yandex.js' },
    { key: 'clarity', path: '/integrations/analytics/clarity.js' },
    { key: 'cloudflare', path: '/integrations/analytics/cloudflare.js' },
    { key: 'mixpanel', path: '/integrations/analytics/mixpanel.js' },
    { key: 'amplitude', path: '/integrations/analytics/amplitude.js' },
    { key: 'posthog', path: '/integrations/analytics/posthog.js' },
    { key: 'umami', path: '/integrations/analytics/umami.js' },
    { key: 'goatcounter', path: '/integrations/analytics/goatcounter.js' },
    { key: 'heap', path: '/integrations/analytics/heap.js' },
    { key: 'logrocket', path: '/integrations/analytics/logrocket.js' },
    { key: 'beam', path: '/integrations/analytics/beam.js' },
    { key: 'counter_dev', path: '/integrations/analytics/counterdev.js' },
    { key: 'cronitor', path: '/integrations/analytics/cronitor.js' },

    // Monetization
    { key: 'propeller', path: '/integrations/ads/monetization.js' },

    // Chat
    { key: 'tawk', path: '/integrations/chat/tawkto.js' },

    // Monitoring
    { key: 'sentry', path: '/integrations/monitoring/sentry.js' },
    { key: 'honeybadger', path: '/integrations/monitoring/honeybadger.js' },
    { key: 'bugsnag', path: '/integrations/monitoring/bugsnag.js' },
    { key: 'glitchtip', path: '/integrations/monitoring/glitchtip.js' }
  ];

  for (const item of integrations) {
    const serviceConfig = config[item.key];
    if (serviceConfig && serviceConfig.enabled) {
      try {
        const modulePath = `${U_PATH}${item.path}`;
        import(modulePath)
          .then(module => {
            if (module && module.init) {
              module.init(serviceConfig, loadScript, config);
              console.log(`✅ Loaded ${item.key}`);
            }
          })
          .catch(e => console.error(`❌ Failed to load ${item.key}:`, e));
      } catch (e) {
        console.error(`Error initiating ${item.key}`, e);
      }
    }
  }

  // 8. Load Firebase (ES Module)
  import(`${U_PATH}/firebase-modules.js`)
    .then(fb => console.log("🔥 Firebase Modules Loaded"))
    .catch(e => console.error("Firebase load error:", e));

})();
