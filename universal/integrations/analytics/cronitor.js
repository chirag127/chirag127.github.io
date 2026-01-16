export function init(config, loadScript) {
  if (!config.key || !config.enabled) return;
  loadScript('https://rum.cronitor.io/script.js');
  window.cronitor = window.cronitor || function() { (window.cronitor.q = window.cronitor.q || []).push(arguments); };
  cronitor('config', { clientKey: config.key });
}
