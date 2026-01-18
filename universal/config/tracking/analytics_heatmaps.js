/**
 * Part 2: Tracking - Heatmaps & Session Recording
 * BIG TECH PREFERRED: Microsoft Clarity enabled (100% free)
 * @module config/tracking/analytics_heatmaps
 */

export const analytics_heatmaps = {
    // ============================================================================
    // MICROSOFT CLARITY - The King of Free Heatmaps
    // ============================================================================
    // Description:
    // Heatmaps, Scrollmaps, and Session Recordings.
    //
    // Free Limits:
    // - 100% Free Forever.
    // - No traffic limits.
    // - No sampling.
    //
    // Best For:
    // - EVERYONE. There is no better free option.
    //
    clarity: { id: 'v1u8hhnpw2', enabled: true },

    // ============================================================================
    // HOTJAR - The Original (Limited Free Tier)
    // ============================================================================
    // Description:
    // Heatmaps and Recordings + Surveys.
    //
    // Free Limits:
    // - 35 daily sessions (Very low).
    // - Unlimited heatmaps (but limited data within them).
    //
    // Best For:
    // - Very small sites or specific studies.
    //
    hotjar: { siteId: '', enabled: false },

    // ============================================================================
    // SMARTLOOK - Mobile App Focus
    // ============================================================================
    // Description:
    // Session recording for Websites & Mobile Apps.
    //
    // Free Limits:
    // - 3,000 sessions/month.
    //
    smartlook: { projectKey: '', enabled: false }
};

export const analytics_heatmaps_priority = ['clarity', 'hotjar'];
