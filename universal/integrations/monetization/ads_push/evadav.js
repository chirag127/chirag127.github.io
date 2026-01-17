/**
 * Evadav Push Notification Ads Provider
 * @module ads/evadav
 */

export const name = 'evadav';
export const configKey = 'evadav';

export function init(config, loadScript) {
    if (!config.enabled || (!config.publisherId && !config.siteId)) return;

    // Evadav push subscription
    const siteId = config.siteId || config.publisherId;

    loadScript(`//oosoa.net/pfe/current/tag.js?z=${siteId}`, {
        'data-cfasync': 'false'
    });
}
