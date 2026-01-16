export function init(config, loadScript) {
  if (!config.apiKey || !config.enabled) return;
  loadScript('//js.honeybadger.io/v6.12/honeybadger.min.js');
  window.setTimeout(() => {
      if(window.Honeybadger) {
          window.Honeybadger.configure({
              apiKey: config.apiKey,
              environment: "production"
          });
      }
  }, 2000);
}
