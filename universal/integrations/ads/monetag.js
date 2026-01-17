/**
 * Monetag (PropellerAds AI) Provider
 * @module ads/monetag
 */

export const name = 'monetag';
export const configKey = 'monetag';

export function init(config, loadScript) {
    if (!config.zone || !config.enabled) return;

    // Monetag uses multiple script sources
    loadScript('https://alwingulla.com/88/tag.min.js', {
        'data-zone': config.zone,
        'data-cfasync': 'false'
    });

    // Anti-adblock if enabled
    if (config.antiAdblock) {
        loadScript('https://thubanoa.com/1?z=' + config.zone);
    }
}
