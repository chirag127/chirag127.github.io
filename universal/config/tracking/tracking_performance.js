/**
 * Part 2: Tracking - Performance (RUM) & SEO
 * @module config/tracking/tracking_performance
 */

export const tracking_performance = {
    // ============================================================================
    // WEB VITALS (Google)
    // ============================================================================
    // Description:
    // Captures Core Web Vitals (LCP, FID, CLS) using the standard browser API.
    // Data can be sent to GA4 or custom endpoints.
    //
    // Limits:
    // - 100% Free (Native API).
    //
    webVitals: { enabled: true, sendToAnalytics: true },

    // ============================================================================
    // NEW RELIC
    // ============================================================================
    // Description:
    // Full stack observability.
    //
    // Free Limits:
    // - 100 GB Data Ingest / month (Generous).
    // - 1 Full Platform User.
    //
    newRelic: { licenseKey: '', applicationId: '', enabled: false },

    // ============================================================================
    // DATADOG
    // ============================================================================
    // Description:
    // Infrastructure monitoring.
    //
    // Free Limits:
    // - "Free" tier is very limited ( Infrastructure only, up to 5 hosts).
    // - RUM (Real User Monitoring) is paid.
    //
    datadog: { clientToken: '', applicationId: '', enabled: false }
};

export const tracking_performance_priority = ['webVitals', 'newRelic'];
