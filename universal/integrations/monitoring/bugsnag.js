export function init(config, loadScript) {
  if (!config.apiKey || !config.enabled) return;
  loadScript('//d2wy8f7a9ursnm.cloudfront.net/v8/bugsnag.min.js');
  window.setTimeout(() => {
      if(window.Bugsnag) {
          window.Bugsnag.start({ apiKey: config.apiKey });
      }
  }, 2000);
}
