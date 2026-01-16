export function init(config, loadScript) {
  if (!config.id || !config.enabled) return;
  loadScript('https://cdn.logr-in.com/LogRocket.min.js');
  window.setTimeout(() => { if(window.LogRocket) window.LogRocket.init(config.id); }, 2000);
}
