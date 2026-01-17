/**
 * CoinAd Simple Crypto Ads Provider
 * @module ads/coinad
 */

export const name = 'coinad';
export const configKey = 'coinad';

export function init(config, loadScript) {
    if (!config.publisherId || !config.enabled) return;

    loadScript(`//coinad.com/ads/${config.publisherId}.js`);
}
