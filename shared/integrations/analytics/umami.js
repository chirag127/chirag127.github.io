/**
 * Umami Analytics (Cloud)
 * ID: 18b3773e-e365-458c-be78-d1d8238b4f15
 * Host: https://cloud.umami.is
 */
(function() {
  const UMAMI_ID = '18b3773e-e365-458c-be78-d1d8238b4f15';
  const UMAMI_HOST = 'https://cloud.umami.is';

  const script = document.createElement('script');
  script.defer = true;
  script.src = `${UMAMI_HOST}/script.js`;
  script.setAttribute('data-website-id', UMAMI_ID);
  document.head.appendChild(script);

  console.log('[Analytics] Umami loaded');
})();
