/**
 * HilltopAds Provider
 * @module ads/hilltopads
 */

export const name = 'hilltopads';
export const configKey = 'hilltopAds';

export function init(config, loadScript) {
    if (!config.siteId || !config.enabled) return;

    loadScript(`//hta.hilltopads.net/hta/hta.js?id=${config.siteId}`);
}
