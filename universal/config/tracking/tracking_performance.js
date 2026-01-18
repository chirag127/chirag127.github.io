/**
 * Part 2: Tracking - Performance (RUM) & SEO
 * @module config/tracking/tracking_performance
 */

export const tracking_performance = {
    // New Relic
    // Feature: Full stack observability
    // Free Limit: 100GB/month (Generous)
    newRelic: { licenseKey: '', applicationId: '', enabled: false },

    // Datadog
    // Feature: Infrastructure monitoring
    // Free Limit: Limited free tier
    datadog: { clientToken: '', applicationId: '', enabled: false },

    // Pingdom
    // Feature: Uptime monitoring
    // Free Limit: 14 day trial
    pingdom: { siteId: '', enabled: false },

    // Web Vitals
    // Feature: Chrome native performance metrics
    // Free Limit: Unlimited (Browser API)
    webVitals: { enabled: true, sendToAnalytics: true }
};

export const tracking_performance_priority = ['webVitals', 'newRelic', 'datadog', 'pingdom'];
