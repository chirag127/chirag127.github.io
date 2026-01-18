/**
 * Part 2: Tracking - Error Monitoring
 * BIG TECH: Sentry has best free tier
 * @module config/tracking/tracking_bugs
 */

export const tracking_bugs = {
    // SENTRY - Industry standard, 5K events/month free
    // Feature: Full stack monitoring, rigorous performance tracing
    // Free Limit: 5,000 errors/month, 1GB attachments
    sentry: { dsn: 'https://1fb29d2d71eb3c24afd3d9edfb1c6413@o4509296467812352.ingest.us.sentry.io/4509296468533248', enabled: true },

    // ALTERNATIVES - Disabled
    // Rollbar
    // Feature: Real-time error grouping
    // Free Limit: 5,000 events/month
    rollbar: { accessToken: '', enabled: false },

    // Bugsnag
    // Feature: Stability scores for releases
    // Free Limit: 7,500 events/month (Lite)
    bugsnag: { apiKey: '', enabled: false },

    // Honeybadger
    // Feature: Uptime + Error monitoring combined
    // Free Limit: 12,000 errors/month (Solo)
    honeybadger: { apiKey: '', enabled: false },

    // GlitchTip
    // Feature: Open Source Sentry Fork
    // Free Limit: 1,000 events (Hosted) or Self-host free
    glitchtip: { dsn: '', enabled: false }  // Open source Sentry alternative
};

export const tracking_bugs_priority = ['sentry', 'rollbar', 'bugsnag'];
