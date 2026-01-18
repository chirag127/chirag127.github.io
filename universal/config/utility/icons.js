/**
 * Part 3: Utility - Icons
 * ENABLED - FontAwesome for professional UI
 * @module config/utility/icons
 */

export const icons = {
    // ============================================================================
    // FONTAWESOME - The Standard
    // ============================================================================
    // Description:
    // The web's most popular icon set.
    //
    // Free Limits:
    // - Free CDN usage (Basic Free icons).
    // - Thousands of icons available.
    //
    fontAwesome: { kitCode: '', cdnFallback: true, enabled: true },

    // ============================================================================
    // GOOGLE MATERIAL ICONS
    // ============================================================================
    // Description:
    // Clean, standardized Google look.
    //
    // Limits:
    // - 100% Free (Open Source).
    //
    materialIcons: { enabled: true },

    // ============================================================================
    // IONICONS
    // ============================================================================
    // Description:
    // Premium SVG icons for Ionic framework.
    //
    // Limits:
    // - 100% Free (MIT).
    //
    ionicons: { enabled: false }
};

export const icons_priority = ['fontAwesome', 'materialIcons', 'ionicons'];
