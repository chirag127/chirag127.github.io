/**
 * LogRocket Session Replay
 * App ID: nshsif/github-hub
 */
(function() {
  const LOGROCKET_APP = 'nshsif/github-hub';

  const script = document.createElement('script');
  script.src = 'https://cdn.logr-in.com/LogRocket.min.js';
  script.crossOrigin = 'anonymous';
  script.onload = function() {
    window.LogRocket && window.LogRocket.init(LOGROCKET_APP);
    console.log('[Analytics] LogRocket loaded');
  };
  document.head.appendChild(script);
})();
