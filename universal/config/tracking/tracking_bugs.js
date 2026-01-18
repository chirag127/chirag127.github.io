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
        dsn: 'https://45890ca96ce164182a3c74cca6018e3e@o4509333332164608.ingest.de.sentry.io/4509333334458448',
        enabled: true
    },

    // ============================================================================
    // HONEYBADGER - Developer-Friendly Error Tracking
    // ============================================================================
    // Description:
    // Simple, developer-focused error monitoring.
    //
    // Free Limits (2025):
    // - **25,000 Errors/month** on developer plan.
    //
    honeybadger: { apiKey: 'hbp_x8dJHBTim5uTkF7pIZVqj55X4wedmR11iovM', enabled: true },

    // ============================================================================
    // ROLLBAR - Real-time error grouping
    // ============================================================================
    // Free Limits:
    // - 5,000 events/month.
    //
    rollbar: { accessToken: '88062048efd74f7c8e11659187da782b', enabled: true },

    // ============================================================================
    // BUGSNAG - Stability Monitoring
    // ============================================================================
    // Description:
    // Error monitoring with release health tracking.
    //
    // Free Limits (2025):
    // - **7,500 Events/month** on Lite plan.
    //
    bugsnag: { apiKey: '84afb61cb3bf458037f4f15eeab394c4', enabled: true },

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
    glitchtip: { dsn: 'https://fe8b6978187b4ef09020464050d17b06@app.glitchtip.com/19542', enabled: true }
};

export const tracking_bugs_priority = ['sentry', 'honeybadger', 'rollbar', 'bugsnag', 'glitchtip'];
