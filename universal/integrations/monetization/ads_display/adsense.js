/**
 * Google AdSense Provider
 * @module ads/adsense
 */

export const name = 'adsense';
export const configKey = 'adsense';

export function init(config, loadScript) {
    if (!config.id) return;

    // Load AdSense script
    loadScript(`https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${config.id}`, {
        crossorigin: 'anonymous'
    });

    // Enable auto ads if configured
    if (config.autoAds !== false) {
        (window.adsbygoogle = window.adsbygoogle || []).push({
            google_ad_client: config.id,
            enable_page_level_ads: true
        });
    }
}
