/**
 * Part 2: Tracking - Analytics General
 * VISIBILITY FOCUS: All major analytics enabled for maximum insights
 * @module config/tracking/analytics_general
 */

export const analytics_general = {
    // ============================================================================
    // GOOGLE ANALYTICS 4 (GA4) - The Industry Standard
    // ============================================================================
    // Description:
    // The default analytics solution for the web. Measures traffic and engagement.
    //
    // Free Limits:
    // - Unlimited Hits (Sampling may apply at extremely high scale).
    // - Data retention: 2 or 14 months for custom data (standard).
    // - 100% Free.
    //
    // Best For:
    // - Everyone. It's the baseline.
    //
    ga4: { id: 'G-PQ26TN1XJ4', enabled: true, lazyLoad: false },

    // ============================================================================
    // YANDEX METRICA - The "All-in-One" Wonder
    // ============================================================================
    // Description:
    // Powerful analytics that includes FREE Session Replay and Heatmaps (Webvisor).
    //
    // Free Limits:
    // - Unlimited Data Retention (Reports).
    // - Unlimited Traffic.
    // - Webvisor (Session Replay): Retained for 15 days.
    // - 100% Free.
    //
    // Best For:
    // - Getting Heatmaps/Recordings + Analytics in one free script.
    //
    yandex: { id: 106273806, enabled: true, webvisor: true, clickmap: true },

    // ============================================================================
    // MICROSOFT CLARITY - Heatmaps & Recordings
    // ============================================================================
    // Description:
    // Pure focus on user behavior: Heatmaps and Session Recordings.
    //
    // Free Limits:
    // - 100% Free Forever. No traffic limits. No sampling.
    // - Retention: 30 days for recordings / 1 year for heatmaps.
    //
    // Best For:
    // - Visualizing user behavior (clicks, scrolls, rage clicks).
    //
    clarity: { id: 'v1u8hhnpw2', enabled: true },

    // ============================================================================
    // MIXPANEL - Product Analytics
    // ============================================================================
    // Description:
    // Event-based analytics for deep product usage insights (funnels, retention).
    //
    // Free Limits:
    // - 20 Million Events / month.
    // - Unlimited History.
    // - Core Reports: Funnels, Flows, Retention.
    //
    // Best For:
    // - SaaS, Web Apps, deep user journey analysis.
    //
    mixpanel: { token: '8d06e28c86c9b01865d866d0ac4982af', enabled: true },

    // ============================================================================
    // POSTHOG - The Open Source Suite
    // ============================================================================
    // Description:
    // Product analytics, session recording, feature flags, and A/B testing.
    //
    // Free Limits (Cloud):
    // - 1 Million Events/month (Analytics).
    // - 5,000 Recordings/month.
    // - 1 Million Feature Flag requests/month.
    // - **Requires Credit Card for some overages, but generous free tier**.
    //
    // Best For:
    // - "All in one" product stack (Analytics + Replay + Flags).
    //
    posthog: { key: 'phc_P9VZ5bjyFoWrIUbecuFTUN2oKavGQYqT3rVSxX8Kqn8', host: 'https://us.i.posthog.com', enabled: false },

    // ============================================================================
    // UMAMI - Privacy-Friendly
    // ============================================================================
    // Description:
    // Simple, privacy-focused open-source analytics. No cookies.
    //
    // Free Limits (Cloud):
    // - 100k events/month.
    // - 3 Websites.
    //
    // Best For:
    // - Privacy-conscious sites, EU compliance.
    //
    umami: { id: '18b3773e-e365-458c-be78-d1d8238b4f15', host: 'https://cloud.umami.is', enabled: true },

    // ============================================================================
    // GOATCOUNTER - Simple & Fast
    // ============================================================================
    // Description:
    // User-friendly, lightweight statistics.
    //
    // Free Limits:
    // - 100k pageviews/month.
    // - Unlimited sites.
    //
    goatcounter: { code: 'chirag127', enabled: true },

    // ============================================================================
    // AMPLITUDE - Product Intelligence
    // ============================================================================
    // Description:
    // Digital analytics platform.
    //
    // Free Limits:
    // - 100,000 Monthly Tracked Users (MTUs).
    // - Powerful behavioral cohorts.
    //
    amplitude: { apiKey: 'd1733215e7a8236a73912adf86ac450b', enabled: false },

    // ============================================================================
    // CLOUDFLARE WEB ANALYTICS
    // ============================================================================
    // Description:
    // Privacy-first, lightweight edge analytics.
    //
    // Free Limits:
    // - 100% Free (Unlimited).
    //
    cloudflare: { token: '333c0705152b4949b3eb0538cd4c2296', enabled: true }
};

export const analytics_general_priority = ['ga4', 'yandex', 'clarity', 'mixpanel', 'posthog', 'umami', 'goatcounter', 'cloudflare'];
export const analytics_lazyLoad = true;
