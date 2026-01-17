/**
 * RichAds Push Ads Provider
 * @module ads/richads
 */

export const name = 'richads';
export const configKey = 'richads';

export function init(config, loadScript) {
    if (!config.publisherId || !config.enabled) return;

    loadScript(`//richinfo.co/richpartners/push/js/r498.js?pubid=${config.publisherId}`);
}
