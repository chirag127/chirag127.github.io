/**
 * Part 3: Utility - Fonts
 * ENABLED - Google Fonts for professional look
 * @module config/utility/fonts
 */

export const fonts = {
    googleFonts: {
        families: ['Inter:wght@400;500;600;700', 'JetBrains+Mono:wght@400;500'],
        enabled: true,
        display: 'swap'  // Performance: font-display: swap
    },
    adobeFonts: { projectId: '', enabled: false }
};

export const fonts_priority = ['googleFonts'];
