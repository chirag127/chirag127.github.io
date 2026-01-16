/**
 * Chirag Hub - Integrations Loader
 *
 * Modular integration system for:
 * - Analytics (GA4, Yandex, Clarity, Mixpanel, etc.)
 * - Chat (Tawk.to)
 * - Monetization (Ads, Donations)
 * - Monitoring (Cronitor, Beam)
 *
 * Each integration is loaded from a separate file for modularity.
 * To disable an integration, comment out the corresponding line below.
 */

(function() {
  const BASE_URL = 'https://chirag127.github.io/shared/integrations';

  // Configuration: Enable/disable integrations
  const CONFIG = {
    analytics: {
      ga4: true,           // Google Analytics 4
      yandex: true,        // Yandex Metrica (Webvisor)
      clarity: true,       // Microsoft Clarity
      cloudflare: true,    // Cloudflare Web Analytics
      mixpanel: true,      // Mixpanel
      amplitude: true,     // Amplitude
      posthog: true,       // PostHog
      umami: true,         // Umami Cloud
      goatcounter: true,   // GoatCounter
      heap: true,          // Heap
      logrocket: false     // LogRocket (disable for performance)
    },
    chat: {
      tawkto: true         // Tawk.to Live Chat
    },
    ads: {
      monetization: true   // Monetization (BuyMeACoffee button)
    },
    monitoring: {
      cronitor: true,      // Cronitor RUM
      beam: true,          // Beam Analytics
      counterdev: true     // Counter.dev
    }
  };

  // Script loader utility
  function loadScript(url) {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = url;
      script.async = true;
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  // Load enabled integrations
  async function loadIntegrations() {
    const loads = [];

    // Analytics
    for (const [key, enabled] of Object.entries(CONFIG.analytics)) {
      if (enabled) loads.push(loadScript(`${BASE_URL}/analytics/${key}.js`));
    }

    // Chat
    for (const [key, enabled] of Object.entries(CONFIG.chat)) {
      if (enabled) loads.push(loadScript(`${BASE_URL}/chat/${key}.js`));
    }

    // Ads
    for (const [key, enabled] of Object.entries(CONFIG.ads)) {
      if (enabled) loads.push(loadScript(`${BASE_URL}/ads/${key}.js`));
    }

    // Monitoring
    for (const [key, enabled] of Object.entries(CONFIG.monitoring)) {
      if (enabled) loads.push(loadScript(`${BASE_URL}/monitoring/${key}.js`));
    }

    try {
      await Promise.allSettled(loads);
      console.log('[Integrations] All modules loaded');
    } catch (e) {
      console.error('[Integrations] Some modules failed to load:', e);
    }
  }

  // Load on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadIntegrations);
  } else {
    loadIntegrations();
  }
})();
