/**
 * Part 2: Tracking - Heatmaps & Session Recording
 * UI/UX FOCUS: Visualizing the user journey
 * @module config/tracking/analytics_heatmaps
 */

export const analytics_heatmaps = {
    // ============================================================================
    // MICROSOFT CLARITY - The Gold Standard for Free Behavior Analysis
    // ============================================================================
    // Description:
    // Visual data tool that reveals where users are clicking and scrolling.
    //
    // Key Features:
    // - Instant Heatmaps: See where users click, scroll, and move their mouse.
    // - Session Recordings: Watch anonymous replays of user visits.
    // - Insights: Identify rage clicks, dead clicks, and excessive scrolling.
    //
    // Free Limits (2025):
    // - **100% Free Forever** (No traffic limits, no data limits).
    // - GDPR & CCPA compliant.
    //
    // Best For:
    // - Every website. Clarity is arguably the best value-for-money (free) tool.
    //
    clarity: { id: 'v1u8hhnpw2', enabled: true },

    // ============================================================================
    // HOTJAR - The Premium Choice (Limited Free Tier)
    // ============================================================================
    // Description:
    // One of the most famous tools for UX research.
    //
    // Free Limits (2025):
    // - **35 Daily Sessions** (Very small for high traffic sites).
    // - Continuous Heatmaps: Unlimited for up to 35 sessions a day.
    // - Basic filtering and surveys.
    //
    // Best For:
    // - Very small projects or testing specific funnel steps.
    //
    hotjar: { siteId: '', enabled: false },

    // ============================================================================
    // LOGROCKET - Developer Focused Replay
    // ============================================================================
    // Description:
    // Combined session replay with error tracking and network monitoring.
    //
    // Free Limits (2025):
    // - **1,000 Sessions / month**.
    // - 30-day data retention.
    //
    // Best For:
    // - Debugging complex web apps where you need to see the console/network logs.
    //
    logrocket: { appId: 'nshsif/github-hub', enabled: true },

    // ============================================================================
    // SMARTLOOK - Cross-Platform Replay
    // ============================================================================
    // Free Limits:
    // - 3,000 sessions/month.
    //
    smartlook: { projectKey: '', enabled: false }
};

export const analytics_heatmaps_priority = ['clarity', 'logrocket', 'hotjar'];
