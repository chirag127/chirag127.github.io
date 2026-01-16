/**
 * Counter.dev Analytics
 * ID: 5c0f4066-d78f-4cd8-a31d-40448c2f2749
 */
(function() {
  const COUNTER_ID = '5c0f4066-d78f-4cd8-a31d-40448c2f2749';

  const script = document.createElement('script');
  script.src = 'https://cdn.counter.dev/script.js';
  script.setAttribute('data-id', COUNTER_ID);
  script.setAttribute('data-utcoffset', '6');
  document.head.appendChild(script);

  console.log('[Monitoring] Counter.dev loaded');
})();
