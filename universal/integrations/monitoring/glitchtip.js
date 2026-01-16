export function init(config, loadScript, allConfigs) {
    // GlitchTip uses Sentry SDK.
    // We check if Sentry is also enabled to avoiding double loading, though GlitchTip is compatible.
    if (!config.dsn || !config.enabled) return;

    const sentryEnabled = allConfigs && allConfigs.sentry && allConfigs.sentry.enabled;

    if (!sentryEnabled) {
         loadScript('https://browser.sentry-cdn.com/7.60.0/bundle.min.js', {'crossorigin': 'anonymous'});
    }
    window.setTimeout(() => {
          if(window.Sentry && window.Sentry.init) {
              window.Sentry.init({
                  dsn: config.dsn,
                  tracesSampleRate: 0.01 // GlitchTip specific
              });
          }
    }, 2500);
}
