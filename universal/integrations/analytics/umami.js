export function init(config, loadScript) {
  if (!config.id || !config.enabled) return;
  loadScript(`${config.host}/script.js`, {'data-website-id': config.id});
}
