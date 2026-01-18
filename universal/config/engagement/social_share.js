/**
 * Part 4: Engagement - Social Share Buttons
 * ENABLED for maximum social visibility
 * @module config/engagement/social_share
 */

export const social_share = {
    // AddToAny
    // Feature: Lightweight, SVG icons, no account needed
    // Free Limit: 100% FREE (No limits found)
    addtoany: { script: true, enabled: true },

    // ShareThis
    // Feature: Analytics dashboard and sticky bars
    // Free Limit: 100% FREE (Data collection model)
    sharethis: { propertyId: '', enabled: false },

    // AddThis
    // Feature: WAS popular sharing tool
    // Free Limit: TERMINATED / EOL (Service shut down May 2023)
    // WARNING: EOL / SHUT DOWN
    addthis: { pubId: '', enabled: false },

    // Native Web Share
    // Feature: Uses OS-native share sheet for high conversion/privacy
    // Free Limit: 100% FREE
    native: { enabled: true }
};

export const social_share_priority = ['native', 'addtoany', 'sharethis', 'addthis'];
