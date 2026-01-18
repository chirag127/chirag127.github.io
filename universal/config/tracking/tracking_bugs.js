/**
 * Part 2: Tracking - Error Monitoring
 * BIG TECH: Sentry has best free tier
 * @module config/tracking/tracking_bugs
 */

export const tracking_bugs = {
    // ============================================================================
    // SENTRY - Industry Standard
    // ============================================================================
    // Description:
    // Full-stack error monitoring and performance tracing.
    //
    // Free Limits:
    // - 5,000 Errors / month.
    // - 10,000 Performance Units / month.
    // - 50 Repays / month.
    //
    // Best For:
    // - Serious production apps.
    //
    sentry: { dsn: 'https://1fb29d2d71eb3c24afd3d9edfb1c6413@o4509296467812352.ingest.us.sentry.io/4509296468533248', enabled: true },

    // ============================================================================
    // GLITCHTIP - Open Source Sentry
    // ============================================================================
    // Description:
    // Sentry-compatible API but open source.
    //
    // Free Limits:
    // - 1,000 Events (Hosted).
    // - UNLIMITED (Self-hosted).
    //
    glitchtip: { dsn: '', enabled: false },

    // ============================================================================
    // ROLLBAR
    // ============================================================================
    // Description:
    // Real-time error grouping.
    //
    // Free Limits:
    // - 5,000 events/month.
    //
    rollbar: { accessToken: '', enabled: false }
};

export const tracking_bugs_priority = ['sentry', 'glitchtip', 'rollbar'];
