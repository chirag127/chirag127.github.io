/**
 * GoatCounter Analytics Provider
 * @module analytics/goatcounter
 */

export const name = 'goatcounter';
export const configKey = 'goatcounter';

export function init(config, loadScript) {
    if (!config.code && !config.endpoint) return;

    const s = document.createElement('script');
    s.async = true;
    s.src = '//gc.zgo.at/count.js';
    s.dataset.goatcounter = config.endpoint || `https://${config.code}.goatcounter.com/count`;
    document.body.appendChild(s);
}
