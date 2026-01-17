/**
 * Yllix Display Ads Provider
 * @module ads/yllix
 */

export const name = 'yllix';
export const configKey = 'yllix';

export function init(config, loadScript) {
    if (!config.siteId || !config.enabled) return;

    loadScript(`//yllix.com/js/yllix_widget_loader.js`, {
        'data-site': config.siteId
    });
}
