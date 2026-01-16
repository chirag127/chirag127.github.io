/**
 * Google Analytics 4 (GA4)
 * ID: G-PQ26TN1XJ4
 */
(function() {
  const GA4_ID = 'G-PQ26TN1XJ4';

  // Load gtag.js
  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${GA4_ID}`;
  document.head.appendChild(script);

  // Initialize
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('config', GA4_ID);

  window.gtag = gtag;
  console.log('[Analytics] GA4 loaded');
})();
