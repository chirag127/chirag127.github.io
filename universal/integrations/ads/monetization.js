export function init(config, loadScript) {
  if (!config.zone || !config.enabled) return;
  loadScript('https://quge5.com/88/tag.min.js', {'data-zone': config.zone, 'data-cfasync': 'false'});
}
