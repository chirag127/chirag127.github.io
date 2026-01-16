export function init(config, loadScript) {
  if (!config.code || !config.enabled) return;
  loadScript('//gc.zgo.at/count.js', {'data-goatcounter': `https://${config.code}.goatcounter.com/count`});
}
