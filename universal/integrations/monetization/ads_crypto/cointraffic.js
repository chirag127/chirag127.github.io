/**
 * Cointraffic Crypto Ads Provider
 * @module ads/cointraffic
 */

export const name = 'cointraffic';
export const configKey = 'cointraffic';

export function init(config, loadScript) {
    if (!config.publisherId || !config.enabled) return;

    loadScript(`//cointraffic.io/widgets/${config.publisherId}.js`);
}
