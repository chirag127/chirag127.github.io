/**
 * Adsterra Ads Provider
 * @module ads/adsterra
 */

export const name = 'adsterra';
export const configKey = 'adsterra';

export function init(config, loadScript) {
    if (!config.key && !config.scriptUrl) return;

    if (config.scriptUrl) {
        loadScript(config.scriptUrl, {
            'data-cfasync': 'false'
        });
    } else if (config.key) {
        // Social bar or native ads
        const atOptions = {
            key: config.key,
            format: config.format || 'iframe',
            height: config.height || 250,
            width: config.width || 300,
            params: config.params || {}
        };
        window.atOptions = atOptions;

        loadScript(`//www.topcreativeformat.com/${config.key}/invoke.js`);
    }
}
