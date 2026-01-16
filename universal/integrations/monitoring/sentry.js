export function init(config, loadScript) {
  if (!config.dsn || !config.enabled) return;
  loadScript('https://browser.sentry-cdn.com/7.60.0/bundle.min.js', {'crossorigin': 'anonymous'});
  window.Sentry = window.Sentry || {};
  window.setTimeout(() => {
      if(window.Sentry && window.Sentry.init) {
          window.Sentry.init({
              dsn: config.dsn,
              sendDefaultPii: true
          });
      }
  }, 2000);
}
