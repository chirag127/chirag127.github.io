/**
 * Cloudflare Web Analytics
 * Token: 333c0705152b4949b3eb0538cd4c2296
 */
(function() {
  const CF_TOKEN = '333c0705152b4949b3eb0538cd4c2296';

  const script = document.createElement('script');
  script.defer = true;
  script.src = 'https://static.cloudflareinsights.com/beacon.min.js';
  script.setAttribute('data-cf-beacon', JSON.stringify({ token: CF_TOKEN }));
  document.head.appendChild(script);

  console.log('[Analytics] Cloudflare Analytics loaded');
})();
