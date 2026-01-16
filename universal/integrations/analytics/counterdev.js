export function init(config, loadScript) {
  if (!config.id || !config.enabled) return;
  loadScript('https://cdn.counter.dev/script.js', {'data-id': config.id, 'data-utcoffset': '6'});
}
