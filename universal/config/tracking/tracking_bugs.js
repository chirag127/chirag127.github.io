/**
 * Part 2: Tracking - Error Monitoring & Bug Tracking
 * RELIABILITY FOCUS: Catching crashes before users report them
 * @module config/tracking/tracking_bugs
 */

export const tracking_bugs = {
    // ============================================================================
    // SENTRY - The Industry Leader
    // ============================================================================
    // Description:
    // Full-stack error monitoring that provides deep context for every crash.
    //
    // Key Features:
    // - Stack traces with source maps.
    // - Performance monitoring and vitals.
    // - Session Replay (Error-focused).
    //
    // Free Limits (2025 - "Developer" Plan):
    // - **5,000 Errors / month**.
    // - **10,000 Performance Units / month**.
    // - **50 Session Replays / month**.
    // - 1 User.
    //
    // Best For:
    // - Professional apps needing production-grade monitoring.
    //
    sentry: {
        dsn: 'https://1fb29d2d71eb3c24afd3d9edfb1c6413@o4509296467812352.ingest.us.sentry.io/4509296468533248',
        enabled: true
    },

    // ============================================================================
    // GLITCHTIP - Open Source & Sentry Compatible
    // ============================================================================
    // Description:
    // An open-source alternative that implements the Sentry API.
    //
    // Free Limits (Hosted):
    // - **1,000 Events / month**.
    // - **Unlimited (if self-hosted)**.
    //
    glitchtip: { dsn: '', enabled: false },

    // ============================================================================
    // ROLLBAR - Real-time error grouping
    // ============================================================================
    // Free Limits:
    // - 5,000 events/month.
    //
    rollbar: { accessToken: '', enabled: false }
};

export const tracking_bugs_priority = ['sentry', 'glitchtip', 'rollbar'];
