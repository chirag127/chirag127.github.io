/**
 * AdCash Display Ads Provider
 * @module ads/adcash
 */

export const name = 'adcash';
export const configKey = 'adcash';

export function init(config, loadScript) {
    if (!config.zoneId || !config.enabled) return;

    loadScript(`//asacdn.com/script/atg.js`, {
        'data-zone': config.zoneId
    });
}
