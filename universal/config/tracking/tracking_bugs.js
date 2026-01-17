/**
 * Part 2: Tracking - Error Monitoring
 * BIG TECH: Sentry has best free tier
 * @module config/tracking/tracking_bugs
 */

export const tracking_bugs = {
    // SENTRY - Industry standard, 5K events/month free
    sentry: { dsn: 'https://1fb29d2d71eb3c24afd3d9edfb1c6413@o4509296467812352.ingest.us.sentry.io/4509296468533248', enabled: true },

    // ALTERNATIVES - Disabled
    rollbar: { accessToken: '', enabled: false },
    bugsnag: { apiKey: '', enabled: false },
    honeybadger: { apiKey: '', enabled: false },
    glitchtip: { dsn: '', enabled: false }  // Open source Sentry alternative
};

export const tracking_bugs_priority = ['sentry', 'rollbar', 'bugsnag'];
