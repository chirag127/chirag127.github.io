/**
 * ShareThis Social Buttons Provider
 * @module engagement/sharethis
 */

export const name = 'sharethis';
export const configKey = 'shareThis';

export function init(config, loadScript) {
    if (!config.propertyId || !config.enabled) return;

    loadScript(`//platform-api.sharethis.com/js/sharethis.js#property=${config.propertyId}&product=sticky-share-buttons`);
}
