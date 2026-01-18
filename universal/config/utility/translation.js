/**
 * Part 3: Utility - Translation
 * ENABLED - Multi-language for global reach
 * @module config/utility/translation
 */

export const translation = {
    // ============================================================================
    // GOOGLE TRANSLATE - Simple Widget
    // ============================================================================
    // Description:
    // Simple drop-down widget to translate the page.
    //
    // Limits:
    // - 100% Free (Legacy Widget).
    //
    googleTranslate: { pageLanguage: 'en', enabled: true },

    // ============================================================================
    // WEGLOT - SEO Optimized
    // ============================================================================
    // Description:
    // Creates translated versions of your site (subdomains) for SEO.
    //
    // Free Limits:
    // - 2,000 translated words.
    // - 1 translated language.
    //
    weglot: { apiKey: '', enabled: false }
};

export const translation_priority = ['googleTranslate', 'weglot'];
