/**
 * Performance Monitoring (RUM) Configuration
 * Real User Monitoring - track actual page load times
 *
 * @module config/performance
 */

export const performanceConfig = {

    // =========================================================================
    // NEW RELIC - Observability platform
    // =========================================================================
    // HOW TO GET: https://newrelic.com/
    // 1. Sign up for free account
    // 2. Create browser application
    // 3. Get license key and app ID
    newRelic: {
        licenseKey: '',
        applicationId: '',
        enabled: false
    },

    // =========================================================================
    // DATADOG RUM - Real User Monitoring
    // =========================================================================
    // HOW TO GET: https://www.datadoghq.com/
    // 1. Sign up (free tier limited)
    // 2. Enable RUM
    // 3. Get client token and app ID
    datadog: {
        clientToken: '',
        applicationId: '',
        enabled: false
    },

    // =========================================================================
    // PINGDOM RUM - Speed testing
    // =========================================================================
    // HOW TO GET: https://www.pingdom.com/
    // 1. Sign up (paid with trial)
    // 2. Create RUM check
    // 3. Get script
    pingdom: {
        siteId: '',
        enabled: false
    },

    // =========================================================================
    // SPEEDCURVE - Performance monitoring
    // =========================================================================
    // HOW TO GET: https://speedcurve.com/
    // Paid, but excellent for performance
    speedcurve: {
        lux_id: '',
        enabled: false
    },

    // =========================================================================
    // REQUESTMETRICS - Simple RUM
    // =========================================================================
    // HOW TO GET: https://requestmetrics.com/
    // 1. Sign up
    // 2. Add site
    // 3. Get token
    requestMetrics: {
        token: '',
        enabled: false
    },

    // =========================================================================
    // WEB VITALS - Google's Core Web Vitals
    // =========================================================================
    // Built-in - no signup needed
    // Just tracks CLS, LCP, FID, etc.
    webVitals: {
        enabled: true,
        sendToAnalytics: true  // Send to GA4 automatically
    }
};

// Performance monitoring priority
export const performancePriority = [
    'webVitals',     // Always - Google's metrics
    'newRelic',
    'datadog',
    'pingdom'
];
