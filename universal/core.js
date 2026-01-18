/* UNIVERSAL CORE ENGINE v3.0 - APEX ARCHITECTURE
   The Heart of the Universal Architecture following APEX TECHNICAL AUTHORITY principles.
   - Client-Side Only Architecture
   - Modular Integration System
   - Zero-Defect, High-Velocity, Future-Proof
   - AI-Native, Neuro-Inclusive, Ethical-First
   - 2026 Spatial Glass Design System
*/

(async function () {
  console.log("🚀 Launching Universal Engine v3.0 (APEX Architecture)...");

  // 1. APEX Configuration - Client-Side Only
  const isLocal = ['localhost', '127.0.0.1'].includes(window.location.hostname);
  const U_PATH = '/universal';

  // 2. Critical CSS Injection (FOUC Prevention)
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = `${U_PATH}/style.css`;
  document.head.appendChild(link);

  // 3. Typography System (Inter Font)
  const fontPreconnect = document.createElement('link');
  fontPreconnect.rel = 'preconnect';
  fontPreconnect.href = 'https://fonts.googleapis.com';
  document.head.appendChild(fontPreconnect);

  const fontLink = document.createElement('link');
  fontLink.rel = 'stylesheet';
  fontLink.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap';
  document.head.appendChild(fontLink);

  // 4. APEX UI Injection (Header & Footer)
  async function loadUI() {
    // Header - Spatial Glass Design
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
          <a href="https://github.com/chirag127" target="_blank" rel="noopener">GitHub</a>
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

    // Footer - Comprehensive Links
    const footer = document.createElement('footer');
    footer.className = 'apex-footer';
    footer.innerHTML = `
      <div class="apex-footer-content">
        <div class="apex-footer-col">
          <h4>Chirag Hub</h4>
          <p>Every tool you need. Free. Private. Forever. 100% browser-powered productivity with AI-native architecture.</p>
        </div>
        <div class="apex-footer-col">
          <h4>Community</h4>
          <a href="/voters.html">Voters</a>
          <a href="/contractors.html">Contractors</a>
          <a href="/about.html">About</a>
        </div>
        <div class="apex-footer-col">
          <h4>Legal</h4>
          <a href="/privacy.html">Privacy</a>
          <a href="/terms.html">Terms</a>
          <a href="/cookies.html">Cookies</a>
        </div>
        <div class="apex-footer-col">
            <h4>Connect</h4>
            <a href="/contact.html">Contact Us</a>
            <a href="https://github.com/chirag127" target="_blank" rel="noopener">GitHub</a>
        </div>
      </div>
      <div class="apex-copyright">
        © ${new Date().getFullYear()} Chirag Singhal. Open Source. APEX Architecture.
      </div>
    `;
    document.body.appendChild(footer);

    // Theme System - Dark Mode Default (OLED Saving)
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

    if (toggle) {
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

  // 5. APEX Script Loader (Promise-Based)
  function loadScript(src, attrs = {}) {
    return new Promise((resolve, reject) => {
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

  // 6. Safe Dynamic Import (ES2026 Modules)
  async function safeImport(path) {
    try {
      return await import(path);
    } catch (e) {
      console.warn(`Import failed: ${path}`, e.message);
      return null;
    }
  }

  // 7. APEX Configuration System (Modular)
  let SITE_CONFIG = window.SITE_CONFIG || {};
  let priorities = {};

  const configModule = await safeImport(`${U_PATH}/config/index.js`);
  if (configModule) {
    const modularConfig = configModule.SITE_CONFIG || {};
    SITE_CONFIG = { ...SITE_CONFIG, ...flattenConfig(modularConfig) };
    priorities = configModule.priorities || {};
  }

  // Make config globally available
  window.SITE_CONFIG = SITE_CONFIG;
  window.CONFIG_PRIORITIES = priorities;

  // Helper: Flatten nested config objects
  function flattenConfig(config) {
    const flat = {};

    function extractProviders(obj, depth = 0) {
      if (!obj || typeof obj !== 'object') return;

      for (const [key, value] of Object.entries(obj)) {
        if (value && typeof value === 'object') {
          if ('enabled' in value) {
            flat[key] = value;
          } else if (depth < 3) {
            extractProviders(value, depth + 1);
          }
        }
      }
    }

    extractProviders(config);
    return flat;
  }

  // Helper: Initialize integration stack
  async function initStack(integrations, config, loadScript, stackName) {
    if (!integrations) return 0;
    let count = 0;

    for (const [subCategory, subIntegrations] of Object.entries(integrations)) {
      if (subIntegrations && typeof subIntegrations === 'object') {
        for (const [providerName, provider] of Object.entries(subIntegrations)) {
          try {
            const providerConfig = config[providerName] || config[provider?.configKey];

            if (!providerConfig || providerConfig.enabled === false) continue;

            if (typeof provider?.init === 'function') {
              await provider.init(providerConfig, loadScript);
              count++;
              console.log(`   ✓ ${stackName}/${providerName} initialized`);
            }
          } catch (e) {
            console.warn(`   ⚠ ${stackName}/${providerName} failed:`, e.message);
          }
        }
      }
    }
    return count;
  }

  // 8. APEX Integration System (Modular)
  const integrationsModule = await safeImport(`${U_PATH}/integrations/index.js`);

  let trackingCount = 0, monetizationCount = 0, engagementCount = 0;

  if (integrationsModule) {
    const { tracking, monetization, engagement, communication, utility } = integrationsModule;

    // Initialize tracking integrations
    console.log("📊 Loading Tracking & Analytics...");
    trackingCount = await initStack(tracking, SITE_CONFIG, loadScript, 'Tracking');

    // Initialize monetization
    console.log("💰 Loading Monetization...");
    monetizationCount = await initStack(monetization, SITE_CONFIG, loadScript, 'Monetization');

    // Initialize engagement
    console.log("🎯 Loading Engagement...");
    engagementCount = await initStack(engagement, SITE_CONFIG, loadScript, 'Engagement');

    // Initialize communication
    console.log("💬 Loading Communication...");
    await initStack(communication, SITE_CONFIG, loadScript, 'Communication');

    // Initialize utility
    console.log("⚙️ Loading Utility...");
    await initStack(utility, SITE_CONFIG, loadScript, 'Utility');
  } else {
    console.warn("⚠️ Modular integrations not loaded, using fallback config.js only");
  }

  // 9. Load Sidebar Module (Polymorphs)
  await loadScript(`${U_PATH}/sidebar.js`);

  // 10. Universal Polymorph Button Injection
  await injectPolymorphButton();

  // 11. Report initialization stats
  console.log(`✨ Universal Engine v3.0 (APEX) initialized!`);
  console.log(`   📊 Tracking: ${trackingCount} providers`);
  console.log(`   💰 Monetization: ${monetizationCount} providers`);
  console.log(`   🎯 Engagement: ${engagementCount} providers`);

  // 12. Universal Polymorph Button Function
  async function injectPolymorphButton() {
    try {
      const currentPath = window.location.pathname;
      const isMainHub = currentPath === '/' || currentPath === '/index.html';
      const isPolymorphPage = currentPath.includes('/polymorphs/');

      const polymorphs = await discoverPolymorphs();

      if (polymorphs.length > 0) {
        let currentSlug = '';
        if (isPolymorphPage) {
          const filename = currentPath.split('/').pop();
          currentSlug = filename.replace('.html', '');
        }

        if (window.Polymorphs && typeof window.Polymorphs.init === 'function') {
          window.Polymorphs.init(polymorphs, {
            currentSlug: currentSlug,
            baseUrl: 'polymorphs',
            isHub: isMainHub
          });
          console.log(`🔮 Polymorphs button injected with ${polymorphs.length} variants`);
        } else {
          setTimeout(() => {
            if (window.Polymorphs) {
              window.Polymorphs.init(polymorphs, {
                currentSlug: currentSlug,
                baseUrl: 'polymorphs',
                isHub: isMainHub
              });
              console.log(`🔮 Polymorphs button injected (fallback) with ${polymorphs.length} variants`);
            }
          }, 100);
        }
      }
    } catch (error) {
      console.warn('⚠️ Polymorph button injection failed:', error.message);
    }
  }

  // 13. Discover Polymorphs Function (GitHub API)
  async function discoverPolymorphs() {
    try {
      const cacheKey = 'polymorphs_cache';
      const cached = localStorage.getItem(cacheKey);
      if (cached) {
        try {
          const { data, timestamp } = JSON.parse(cached);
          if (Date.now() - timestamp < 3600000) {
            return data;
          }
        } catch (e) { /* ignore invalid cache */ }
      }

      const response = await fetch('https://api.github.com/repos/chirag127/chirag127.github.io/contents/polymorphs');
      if (!response.ok) throw new Error('Failed to fetch polymorphs');

      const files = await response.json();
      const htmlFiles = files.filter(file => file.name.endsWith('.html'));

      const polymorphs = htmlFiles.map(file => {
        const slug = file.name.replace('.html', '');
        return mapSlugToModel(slug);
      }).filter(Boolean);

      localStorage.setItem(cacheKey, JSON.stringify({
        data: polymorphs,
        timestamp: Date.now()
      }));

      return polymorphs;
    } catch (error) {
      console.warn('Failed to discover polymorphs:', error.message);
      return await getFallbackPolymorphs();
    }
  }

  // 14. Map slug to model info
  function mapSlugToModel(slug) {
    const modelMap = {
      'deepseek-r1t2-chimera-openrouter': { name: 'DeepSeek R1T2 Chimera', size: 671, provider: 'OpenRouter' },
      'deepseek-v3-2-nvidia': { name: 'DeepSeek V3.2', size: 671, provider: 'NVIDIA' },
      'glm-4-7-1t-moe-cerebras': { name: 'GLM 4.7 1T MoE', size: 1000, provider: 'Cerebras' },
      'mistral-large-3-675b-instruct-mistral': { name: 'Mistral Large 3', size: 675, provider: 'Mistral' },
      'mistral-large-3-675b-instruct-nvidia': { name: 'Mistral Large 3', size: 675, provider: 'NVIDIA' },
      'qwen3-coder-480b-moe-openrouter': { name: 'Qwen3 Coder 480B MoE', size: 480, provider: 'OpenRouter' }
    };

    const model = modelMap[slug];
    if (model) {
      return {
        slug: slug,
        name: model.name,
        size: model.size,
        provider: model.provider
      };
    }

    const parts = slug.split('-');
    return {
      slug: slug,
      name: parts.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join(' '),
      size: 70,
      provider: 'AI'
    };
  }

  // 15. Fallback polymorphs
  // 15. Fallback polymorphs (Dynamic)
  async function getFallbackPolymorphs() {
    // Try to load dynamic config first
    const modelsConfig = await safeImport(`${U_PATH}/config/models.js`);
    if (modelsConfig && modelsConfig.models) {
      console.log(`✨ Using ${modelsConfig.models.length} dynamic fallback models`);
      return modelsConfig.models;
    }

    console.warn("⚠️ Dynamic models config not found, using minimal fallback");
    return [
      { slug: 'glm-4-7-1t-moe-cerebras', name: 'GLM 4.7 1T MoE', size: 1000, provider: 'Cerebras' },
      { slug: 'deepseek-r1t2-chimera-openrouter', name: 'DeepSeek R1T2 Chimera', size: 671, provider: 'OpenRouter' },
    ];
  }

})();
