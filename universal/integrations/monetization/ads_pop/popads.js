/**
 * PopAds Pop-Under Provider
 * @module ads/popads
 */

export const name = 'popads';
export const configKey = 'popads';

export function init(config, loadScript) {
    if (!config.publisherId || !config.enabled) return;

    // Check pop frequency limits
    const lastPop = localStorage.getItem('popads_last');
    const now = Date.now();
    const minDelay = (config.frequency || 1) * 86400 * 1000; // Days to ms

    if (lastPop && (now - parseInt(lastPop)) < minDelay) {
        console.log('PopAds: Frequency limit, skipping');
        return;
    }

    // Configure PopAds
    window.popns = window.popns || [];
    window.popns.push({
        siteId: config.publisherId,
        minBid: config.minBid || 0,
        pop498: config.delay || 0
    });

    // Load PopAds script
    loadScript('//c1.popads.net/pop.js');

    // Record pop time
    localStorage.setItem('popads_last', now.toString());
}
