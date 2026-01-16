export function init(config, loadScript) {
  if (!config.token || !config.enabled) return;
  loadScript('https://static.cloudflareinsights.com/beacon.min.js', {'data-cf-beacon': `{"token": "${config.token}"}`});
}
