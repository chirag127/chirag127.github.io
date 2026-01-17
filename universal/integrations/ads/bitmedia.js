/**
 * Bitmedia Bitcoin Ads Provider
 * @module ads/bitmedia
 */

export const name = 'bitmedia';
export const configKey = 'bitmedia';

export function init(config, loadScript) {
    if ((!config.publisherId && !config.zoneId) || !config.enabled) return;

    const id = config.zoneId || config.publisherId;
    loadScript(`//bitmedia.io/tags/${id}.js`);
}
