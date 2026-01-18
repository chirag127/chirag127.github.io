/**
 * Part 3: Utility - Translation
 * ENABLED - Multi-language for global reach
 * @module config/utility/translation
 */

export const translation = {
    // Google Translate
    // Feature: Simple drop-down widget
    // Free Limit: 100% Free (Legacy Widget)
    googleTranslate: { pageLanguage: 'en', enabled: true },  // Free, easy

    // Weglot
    // Feature: SEO optimized translation (Subdomains)
    // Free Limit: 2,000 translated words, 1 language
    weglot: { apiKey: '', enabled: false }  // Better but paid
};

export const translation_priority = ['googleTranslate'];
