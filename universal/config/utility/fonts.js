/**
 * Part 3: Utility - Fonts
 * ENABLED - Google Fonts for professional look
 * @module config/utility/fonts
 */

export const fonts = {
    // Google Fonts
    // Feature: Extensive free library
    // Performance: Fast CDN delivery
    googleFonts: {
        families: ['Inter:wght@400;500;600;700', 'JetBrains+Mono:wght@400;500'],
        enabled: true,
        display: 'swap'  // Performance: font-display: swap
    },

    // Adobe Fonts (Typekit)
    // Feature: Premium typefaces
    // Limit: Creative Cloud subscription required
    adobeFonts: { projectId: '', enabled: false }
};

export const fonts_priority = ['googleFonts', 'adobeFonts'];
