/**
 * AdShares Blockchain Ads Provider
 * @module ads/adshares
 */

export const name = 'adshares';
export const configKey = 'adshares';

export function init(config, loadScript) {
    if (!config.publisherId || !config.enabled) return;

    loadScript(`//app.adshares.net/supply/find`, {
        'data-publisher': config.publisherId
    });
}
