/**
 * PopCash Pop-Under Provider
 * @module ads/popcash
 */

export const name = 'popcash';
export const configKey = 'popcash';

export function init(config, loadScript) {
    if (!config.publisherId || !config.enabled) return;

    // Check frequency limits
    const lastPop = localStorage.getItem('popcash_last');
    const now = Date.now();
    const minDelay = (config.frequency || 1) * 86400 * 1000;

    if (lastPop && (now - parseInt(lastPop)) < minDelay) {
        console.log('PopCash: Frequency limit, skipping');
        return;
    }

    // PopCash configuration
    window.popcash_config = {
        siteId: config.publisherId,
        frequency: config.frequency || 1
    };

    // Load PopCash
    loadScript('//cdn.popcash.net/show.js');

    localStorage.setItem('popcash_last', now.toString());
}
