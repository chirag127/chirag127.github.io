/**
 * Part 2: Tracking - SEO & Webmasters
 * ALL ENABLED for maximum search engine visibility
 * @module config/tracking/tracking_seo
 */

export const tracking_seo = {
    // ALL MAJOR SEARCH ENGINES ENABLED
    googleSearchConsole: { verificationTag: '', enabled: true },
    bingWebmaster: { verificationTag: '', enabled: true },
    yandexWebmaster: { verificationTag: '', enabled: true },

    // ADDITIONAL VISIBILITY
    pinterest: { verificationTag: '', enabled: true },  // Image SEO
    baidu: { verificationTag: '', enabled: false }  // China only
};

export const tracking_seo_priority = ['googleSearchConsole', 'bingWebmaster', 'yandexWebmaster', 'pinterest'];
