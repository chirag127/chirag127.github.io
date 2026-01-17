/**
 * Adsterra Display Ads Provider
 * @module ads/adsterra
 */

export const name = 'adsterra';
export const configKey = 'adsterra';

export function init(config, loadScript) {
    if (!config.enabled) return;

    // Load main script if provided
    if (config.scriptUrl) {
        loadScript(config.scriptUrl, { 'data-cfasync': 'false' });
    }

    // Load zone-specific scripts
    if (config.zones) {
        if (config.zones.banner) {
            loadScript(`//www.topcreativeformat.com/${config.zones.banner}/invoke.js`);
        }
        if (config.zones.native) {
            loadScript(`//pl21973682.profitablegatetocontent.com/${config.zones.native}/invoke.js`);
        }
        if (config.zones.socialBar) {
            loadScript(`//www.highperformanceformat.com/${config.zones.socialBar}/invoke.js`);
        }
    }
}
