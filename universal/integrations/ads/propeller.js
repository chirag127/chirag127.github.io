/**
 * PropellerAds Provider
 * @module ads/propeller
 */

export const name = 'propeller';
export const configKey = 'propeller';

export function init(config, loadScript) {
    if (!config.zone) return;

    loadScript('https://quge5.com/88/tag.min.js', {
        'data-zone': config.zone,
        'data-cfasync': 'false'
    });
}
