/**
 * TacoLoco Push Ads Provider
 * @module ads/tacoloco
 */

export const name = 'tacoloco';
export const configKey = 'tacoloco';

export function init(config, loadScript) {
    if (!config.publisherId || !config.enabled) return;

    loadScript(`//cdn.tacoloco.com/sw/${config.publisherId}.js`);
}
