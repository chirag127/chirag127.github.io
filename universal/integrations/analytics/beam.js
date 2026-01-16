export function init(config, loadScript) {
  if (!config.token || !config.enabled) return;
  loadScript('https://beamanalytics.b-cdn.net/beam.min.js', {'data-token': config.token});
}
