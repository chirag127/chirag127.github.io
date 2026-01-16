/**
 * Cronitor RUM (Real User Monitoring)
 * Client Key: 205a4c0b70da8fb459aac415c1407b4d
 */
(function() {
  const CRONITOR_KEY = '205a4c0b70da8fb459aac415c1407b4d';

  const script = document.createElement('script');
  script.async = true;
  script.src = 'https://rum.cronitor.io/script.js';
  document.head.appendChild(script);

  window.cronitor = window.cronitor || function() {
    (window.cronitor.q = window.cronitor.q || []).push(arguments);
  };
  cronitor('config', { clientKey: CRONITOR_KEY });

  console.log('[Monitoring] Cronitor RUM loaded');
})();
