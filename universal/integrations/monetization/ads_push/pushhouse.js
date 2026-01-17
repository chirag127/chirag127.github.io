/**
 * Push.House Push Ads Provider
 * @module ads/pushhouse
 */

export const name = 'pushhouse';
export const configKey = 'pushHouse';

export function init(config, loadScript) {
    if (!config.publisherId || !config.enabled) return;

    loadScript(`//push.house/sw/${config.publisherId}.js`);
}
