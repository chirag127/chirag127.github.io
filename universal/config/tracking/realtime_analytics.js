/**
 * Part 2: Tracking - Real-Time Analytics
 * @module config/tracking/realtime_analytics
 */

export const realtime_analytics = {
    // Clicky
    // Feature: Real-time spy view
    // Free Limit: 3,000 daily pageviews
    clicky: { siteId: '', enabled: false },

    // LiveSession
    // Feature: High fidelity session replay
    // Free Limit: 1,000 sessions/month
    livesession: { trackId: '', enabled: false }
};

export const realtime_analytics_priority = ['clicky'];
