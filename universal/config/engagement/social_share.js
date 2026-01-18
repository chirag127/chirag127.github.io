/**
 * Part 4: Engagement - Social Share Buttons
 * ENABLED for maximum social visibility
 * @module config/engagement/social_share
 */

export const social_share = {
    // AddThis (Oracle) - Legacy
    // Feature: Comprehensive analytics & tools
    // Free Limit: Free (End of Life - use caution)
    addthis: { profileId: '', enabled: false },

    // AddToAny
    // Feature: Lightweight, no tracking, vector icons
    // Free Limit: 100% Free
    addtoany: { enabled: true },

    // ShareThis
    // Feature: Sticky bars, inline, image sharing
    // Free Limit: Free (Data collection model)
    sharethis: { propertyId: '', enabled: false }
};

export const social_share_priority = ['addtoany'];
