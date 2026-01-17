/**
 * Coinzilla Crypto Ads Provider
 * @module ads/coinzilla
 */

export const name = 'coinzilla';
export const configKey = 'coinzilla';

export function init(config, loadScript) {
    if (!config.zone) return;

    // Add Coinzilla meta tag
    const meta = document.createElement('meta');
    meta.name = 'coinzilla';
    meta.content = config.zone;
    document.head.appendChild(meta);

    // Load Coinzilla script if needed
    if (config.scriptUrl) {
        loadScript(config.scriptUrl);
    }
}
