/**
 * Part 2: Tracking - Real-Time Analytics
 * FEEDBACK FOCUS: Watching your site in the moment
 * @module config/tracking/realtime_analytics
 */

export const realtime_analytics = {
    // ============================================================================
    // CLICKY - The "Spy" Tool
    // ============================================================================
    // Description:
    // Real-time analytics that allows you to see individual users in real-time.
    //
    // Key Features:
    // - On-site analytics widget.
    // - Individual visitor "spy" view.
    //
    // Free Limits (2025):
    // - **3,000 Daily Pageviews**.
    // - 1 Website.
    //
    clicky: { siteId: '', enabled: false },

    // ============================================================================
    // GO SQUARED - Real-time Dashboard
    // ============================================================================
    // Description:
    // Professional real-time data visualization.
    //
    // Free Limits:
    // - **1,000 Pageviews / month**.
    //
    goSquared: { siteId: '', enabled: false }
};

export const realtime_analytics_priority = ['clicky', 'goSquared'];
