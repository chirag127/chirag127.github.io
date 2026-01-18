/**
 * Part 3: Engagement - User Reviews & Social Proof
 * @module config/engagement/reviews
 */

export const reviews = {
    // ============================================================================
    // TRUSTPILOT - High Trust Badge
    // ============================================================================
    // Description:
    // The most recognized independent review platform.
    //
    // Free Limits (2025):
    // - 50 Review invitations per month.
    // - Basic profile and trust box.
    //
    trustpilot: { businessId: '', enabled: false },

    // ============================================================================
    // G2 - Software Focus
    // ============================================================================
    // Free Limits:
    // - Basic profile listing.
    //
    g2: { productId: '', enabled: false },

    // ============================================================================
    // CROWDSOURCE - Native Review System
    // ============================================================================
    // Description:
    // Internal simple rating system for the tool.
    // **100% Free**.
    //
    native_reviews: { enabled: true }
};

export const reviews_priority = ['native_reviews', 'trustpilot'];
