/**
 * Part 2: Tracking - SEO & Webmaster Verifications
 * SEARCH FOCUS: Indexing and Search Engine Presence
 * @module config/tracking/tracking_seo
 */

export const tracking_seo = {
    // ============================================================================
    // GOOGLE SEARCH CONSOLE (GSC)
    // ============================================================================
    // Description:
    // The single most important tool for SEO on Google.
    //
    // Key Features:
    // - Sitemaps submission.
    // - Inspect URLs.
    // - Track search queries and ranking.
    //
    // Limits:
    // - **100% Free**.
    //
    googleSearchConsole: { verificationTag: '', enabled: true },

    // ============================================================================
    // BING WEBMASTER TOOLS
    // ============================================================================
    // Description:
    // Powers search for Bing, Yahoo, and DuckDuckGo.
    //
    // Key Features:
    // - URL submission.
    // - Keyword research.
    //
    // Limits:
    // - **100% Free**.
    //
    bingWebmaster: { verificationTag: '', enabled: true },

    // ============================================================================
    // YANDEX WEBMASTER
    // ============================================================================
    // Description:
    // Dominant search engine in Russia and Turkey.
    //
    // Limits:
    // - **100% Free**.
    //
    yandexWebmaster: { verificationTag: '', enabled: true },

    // ============================================================================
    // PINTEREST VERIFICATION
    // ============================================================================
    // Description:
    // Unlocks "Rich Pins" and analytics for image-heavy content.
    //
    pinterest: { verificationTag: '', enabled: true },

    // ============================================================================
    // AHREFS WEBMASTER TOOLS
    // ============================================================================
    // Description:
    // In-depth backlink analysis and technical SEO audit (uses GSC data).
    //
    ahrefs: { verificationTag: '', enabled: false }
};

export const tracking_seo_priority = ['googleSearchConsole', 'bingWebmaster', 'yandexWebmaster'];
