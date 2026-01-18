/**
 * Part 2: Tracking - Performance (RUM) & Vitals
 * SPEED FOCUS: Measuring the Pulse of your site
 * @module config/tracking/tracking_performance
 */

export const tracking_performance = {
    // ============================================================================
    // WEB VITALS (Google Native)
    // ============================================================================
    // Description:
    // Measures the user experience metrics that Google uses for search rankings.
    // LCP (Loading), FID/INP (Interactivity), CLS (Stability).
    //
    // Key Features:
    // - Built-in browser support.
    // - Zero external weight (if using native Observer).
    //
    // Limits:
    // - **100% Free** (Unlimited).
    //
    webVitals: { enabled: true, sendToAnalytics: true },

    // ============================================================================
    // NEW RELIC - Full Stack Observability
    // ============================================================================
    // Description:
    // Advanced performance monitoring for frontend and backend.
    //
    // Free Limits (2025):
    // - **100 GB Data Ingest / month** (Very generous).
    // - 1 Full Platform User.
    // - Unlimited basic users.
    //
    // Best For:
    // - Large-scale monitoring and detailed transaction tracing.
    //
    newRelic: { licenseKey: '', applicationId: '', enabled: false },

    // ============================================================================
    // DATADOG - Infrastructure & RUM
    // ============================================================================
    // Description:
    // Cloud-scale monitoring.
    //
    // ⚠️ FREE LIMITS NOTE:
    // - DataDog's "Free" tier is for Infrastructure only (up to 5 hosts).
    // - **RUM (Real User Monitoring) is NOT free**.
    //
    datadog: { clientToken: '', applicationId: '', enabled: false }
};

export const tracking_performance_priority = ['webVitals', 'newRelic'];
