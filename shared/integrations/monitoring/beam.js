/**
 * Beam Analytics
 * Token: 1148dc4c-933b-4fd2-ba28-a0bb56f78978
 */
(function() {
  const BEAM_TOKEN = '1148dc4c-933b-4fd2-ba28-a0bb56f78978';

  const script = document.createElement('script');
  script.async = true;
  script.src = 'https://beamanalytics.b-cdn.net/beam.min.js';
  script.setAttribute('data-token', BEAM_TOKEN);
  document.head.appendChild(script);

  console.log('[Monitoring] Beam Analytics loaded');
})();
