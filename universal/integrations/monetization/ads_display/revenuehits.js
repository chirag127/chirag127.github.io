/**
 * RevenueHits CPA Ads Provider
 * @module ads/revenuehits
 */

export const name = 'revenuehits';
export const configKey = 'revenueHits';

export function init(config, loadScript) {
    if (!config.publisherId || !config.enabled) return;

    loadScript(`//ads.revenuehits.com/ppc.js?pid=${config.publisherId}`);
}
