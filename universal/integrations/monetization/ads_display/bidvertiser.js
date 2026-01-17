/**
 * BidVertiser Display Ads Provider
 * @module ads/bidvertiser
 */

export const name = 'bidvertiser';
export const configKey = 'bidvertiser';

export function init(config, loadScript) {
    if (!config.publisherId || !config.enabled) return;

    loadScript(`//bdv.bidvertiser.com/BidVertiser.dbm?pid=${config.publisherId}&bid=0`, {
        'data-cfasync': 'false'
    });
}
