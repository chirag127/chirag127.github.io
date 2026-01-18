/**
 * Part 2: Tracking - SEO & Webmasters
 * ALL ENABLED for maximum search engine visibility
 * @module config/tracking/tracking_seo
 */

export const tracking_seo = {
    // ============================================================================
    // GOOGLE SEARCH CONSOLE
    // ============================================================================
    // Description:
    // The most critical SEO tool. Monitor indexing, performance, and issues on Google.
    //
    // Limits:
    // - 100% Free.
    //
    googleSearchConsole: { verificationTag: '', enabled: true },

    // ============================================================================
    // BING WEBMASTER TOOLS
    // ============================================================================
    // Description:
    // Essential for Bing, Yahoo, and DuckDuckGo visibility.
    //
    // Limits:
    // - 100% Free.
    //
    bingWebmaster: { verificationTag: '', enabled: true },

    // ============================================================================
    // YANDEX WEBMASTER
    // ============================================================================
    // Description:
    // Essential for Russia, Turkey, and Eastern Europe traffic.
    //
    // Limits:
    // - 100% Free.
    //
    yandexWebmaster: { verificationTag: '', enabled: true },

    // ============================================================================
    // PINTEREST VERIFICATION
    // ============================================================================
    // Description:
    // Verifies website for Pinterest "Rich Pins" (Image SEO).
    //
    pinterest: { verificationTag: '', enabled: true },

    // ============================================================================
    // BAIDU
    // ============================================================================
    // Description:
    // Essential for China.
    //
    baidu: { verificationTag: '', enabled: false }
};

export const tracking_seo_priority = ['googleSearchConsole', 'bingWebmaster', 'yandexWebmaster', 'pinterest'];
