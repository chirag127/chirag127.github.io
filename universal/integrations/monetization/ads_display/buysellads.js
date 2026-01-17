/**
 * BuySellAds Provider
 * @module ads/buysellads
 */

export const name = 'buysellads';
export const configKey = 'buysellads';

export function init(config, loadScript) {
    if (!config.key) return;

    // Set up BSA config
    window._bsa_queue = window._bsa_queue || [];

    // Load BSA script
    loadScript('//s3.buysellads.com/ac/bsa.js');
}
