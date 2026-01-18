/**
 * Part 2: Tracking - SEO & Webmasters
 * ALL ENABLED for maximum search engine visibility
 * @module config/tracking/tracking_seo
 */

export const tracking_seo = {
    // ALL MAJOR SEARCH ENGINES ENABLED
    // Google Search Console
    // Feature: Essential for Google indexing
    // Free Limit: Unlimited
    googleSearchConsole: { verificationTag: '', enabled: true },

    // Bing Webmaster Tools
    // Feature: Essential for Bing/Yahoo/DuckDuckGo
    // Free Limit: Unlimited
    bingWebmaster: { verificationTag: '', enabled: true },

    // Yandex Webmaster
    // Feature: Essential for Russia/Eastern Europe
    // Free Limit: Unlimited
    yandexWebmaster: { verificationTag: '', enabled: true },

    // ADDITIONAL VISIBILITY
    // Pinterest
    // Feature: Verification for Rich Pins
    pinterest: { verificationTag: '', enabled: true },  // Image SEO

    // Baidu
    // Feature: Essential for China
    baidu: { verificationTag: '', enabled: false }  // China only
};

export const tracking_seo_priority = ['googleSearchConsole', 'bingWebmaster', 'yandexWebmaster', 'pinterest'];
