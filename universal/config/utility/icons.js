/**
 * Part 3: Utility - Icons
 * ENABLED - FontAwesome for professional UI
 * @module config/utility/icons
 */

export const icons = {
    // FontAwesome
    // Feature: The web's most popular icon set
    // Free Limit: Free CDN (Basic icons)
    fontAwesome: { kitCode: '', cdnFallback: true, enabled: true },

    // Ionicons
    // Feature: Premium SVG icons for Ionic framework
    // Free Limit: Open Source (Free)
    ionicons: { enabled: false },

    // Material Icons (Google)
    // Feature: Clean, standardized Google look
    // Free Limit: Open Source (Free)
    materialIcons: { enabled: true }  // Google - pairs with Fonts
};

export const icons_priority = ['fontAwesome', 'materialIcons'];
