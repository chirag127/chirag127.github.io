/**
 * Error & Bug Tracking Configuration
 * Detect JavaScript errors and crashes
 *
 * @module config/monitoring
 */

export const monitoringConfig = {

    // =========================================================================
    // SENTRY - Industry standard
    // =========================================================================
    // HOW TO GET: https://sentry.io/
    // 1. Sign up (free tier: 5K errors/month)
    // 2. Create project (JavaScript)
    // 3. Get DSN from project settings
    sentry: {
        dsn: 'https://45890ca96ce164182a3c74cca6018e3e@o4509333332164608.ingest.de.sentry.io/4509333334458448',  // YOUR EXISTING DSN
        enabled: true
    },

    // =========================================================================
    // HONEYBADGER - Error monitoring
    // =========================================================================
    // HOW TO GET: https://www.honeybadger.io/
    // 1. Sign up (free trial)
    // 2. Create project
    // 3. Get API key from project settings
    honeybadger: {
        apiKey: 'hbp_x8dJHBTim5uTkF7pIZVqj55X4wedmR11iovM',  // YOUR EXISTING KEY
        enabled: true
    },

    // =========================================================================
    // ROLLBAR - Real-time error tracking
    // =========================================================================
    // HOW TO GET: https://rollbar.com/
    // 1. Sign up (free tier: 5K events/month)
    // 2. Create project
    // 3. Get access token
    rollbar: {
        accessToken: '88062048efd74f7c8e11659187da782b',  // YOUR EXISTING TOKEN
        enabled: true
    },

    // =========================================================================
    // BUGSNAG - Stability monitoring
    // =========================================================================
    // HOW TO GET: https://www.bugsnag.com/
    // 1. Sign up (free tier: 7,500 events/month)
    // 2. Create project
    // 3. Get API key
    bugsnag: {
        apiKey: '84afb61cb3bf458037f4f15eeab394c4',  // YOUR EXISTING KEY
        enabled: true
    },

    // =========================================================================
    // GLITCHTIP - Open source Sentry alternative
    // =========================================================================
    // HOW TO GET: https://glitchtip.com/
    // 1. Sign up for cloud or self-host
    // 2. Create project
    // 3. Get DSN
    glitchtip: {
        dsn: 'https://fe8b6978187b4ef09020464050d17b06@app.glitchtip.com/19542',  // YOUR EXISTING DSN
        enabled: true
    },

    // =========================================================================
    // RAYGUN - Crash reporting
    // =========================================================================
    // HOW TO GET: https://raygun.com/
    // 1. Sign up (free trial)
    // 2. Create application
    // 3. Get API key
    raygun: {
        apiKey: '',
        enabled: false
    },

    // =========================================================================
    // AIRBRAKE - Error monitoring
    // =========================================================================
    // HOW TO GET: https://airbrake.io/
    // 1. Sign up
    // 2. Create project
    // 3. Get project ID and key
    airbrake: {
        projectId: '',
        projectKey: '',
        enabled: false
    }
};

// Use all enabled error trackers for redundancy
export const monitoringLoadOrder = [
    'sentry',       // Primary
    'bugsnag',      // Secondary
    'rollbar',      // Tertiary
    'honeybadger',
    'glitchtip'
];
