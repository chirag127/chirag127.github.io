/**
 * Part 2: Tracking - Attribution
 * Deep linking and attribution tracking
 * @module config/tracking/attribution
 */

export const attribution = {
    // ============================================================================
    // BRANCH.IO
    // ============================================================================
    // Description:
    // Deep linking and attribution for mobile apps.
    //
    // Free Limits:
    // - 10,000 MAUs (Launch Plan).
    // - Deep linking is free.
    //
    branch: { key: '', enabled: false },

    // ============================================================================
    // APPSFLYER
    // ============================================================================
    // Description:
    // Marketing attribution for apps.
    //
    // Free Limits:
    // - 12,000 conversions (Zero Plan).
    //
    appsflyer: { devKey: '', enabled: false }
};

export const attribution_priority = ['branch', 'appsflyer'];
