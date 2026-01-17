/**
 * Part 4: Engagement - Social Share Buttons
 * ENABLED for maximum social visibility
 * @module config/engagement/social_share
 */

export const social_share = {
    // ENABLE ONE - AddToAny is lightest
    addtoany: { enabled: true },  // Lightweight, no tracking
    sharethis: { propertyId: '', enabled: false },  // Alternative
    addthis: { pubId: '', enabled: false }  // Oracle - heavier
};

export const social_share_priority = ['addtoany'];
