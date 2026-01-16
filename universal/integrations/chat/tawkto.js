export function init(config, loadScript) {
  if (!config.src || !config.enabled) return;
  loadScript(config.src, {'crossorigin': '*'});
}
