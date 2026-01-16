/**
 * Chirag Hub - Integrations Entry Point
 *
 * This file loads the modular integration system.
 * All integrations are now in separate files under shared/integrations/
 *
 * Structure:
 *   /analytics - GA4, Yandex, Clarity, Mixpanel, etc.
 *   /chat      - Tawk.to
 *   /ads       - Monetization
 *   /monitoring - Cronitor, Beam, Counter.dev
 *
 * Configuration is in loader.js
 */

// Load the modular integrations loader
(function() {
  const script = document.createElement('script');
  script.src = 'https://chirag127.github.io/shared/integrations/loader.js';
  script.defer = true;
  document.head.appendChild(script);
})();
