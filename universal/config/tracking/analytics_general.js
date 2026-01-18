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
    // The world's most used web analytics platform. Focuses on event-based data.
    //
    // Key Features:
    // - User journey tracking across devices.
    // - Predictive metrics (churn, revenue).
    // - Standard integration for nearly all ad platforms.
    //
    // Free Limits (2025):
    // - **100% Free** for standard use.
    // - Data retention: 2 months (default) or 14 months (expandable in settings).
    //
    // Best For:
    // - Baseline tracking, baseline for ad conversion measurement.
    //
    ga4: { id: 'G-PQ26TN1XJ4', enabled: true, lazyLoad: false },

    // ============================================================================
    // YANDEX METRICA - The "Everything Included" Powerhouse
    // ============================================================================
    // Description:
    // Comprehensive analytics suite that offers premium features for free.
    //
    // Key Features:
    // - **FREE Session Replay (Webvisor)**: Watch users interact with your site.
    // - **FREE Heatmaps**: Visual click, scroll, and link maps.
    // - Form analytics and detailed demographics.
    //
    // Free Limits:
    // - **100% Free** (Unlimited traffic, unlimited reports).
    // - Webvisor recordings retained for 15 days.
    //
    // Best For:
    // - Getting professional session recordings and heatmaps without a monthly bill.
    //
    yandex: { id: 106273806, enabled: true, webvisor: true, clickmap: true },

    // ============================================================================
    // MICROSOFT CLARITY - Dedicated Behavior Insight
    // ============================================================================
    // Description:
    // Focused entirely on user experience and behavior through visuals.
    //
    // Key Features:
    // - Heatmaps (Click, Scroll, Area).
    // - High-fidelity Session Recordings.
    // - "Rage Click" and "Dead Click" detection.
    //
    // Free Limits:
    // - **100% Free Forever** (No traffic limits, no sampling).
    // - Data retention: 30 days for recordings, 1 year for heatmaps.
    //
    // Best For:
    // - Visualizing exactly where users get frustrated or stuck.
    //
    clarity: { id: 'v1u8hhnpw2', enabled: true },

    // ============================================================================
    // MIXPANEL - Advanced Product Analytics
    // ============================================================================
    // Description:
    // Event-based tracking to understand product usage and user retention.
    //
    // Free Limits (2025):
    // - **20 Million Events per month** (Very generous).
    // - Unlimited historical data.
    // - Core reports (Funnels, Flows, Retention).
    //
    mixpanel: { token: '8d06e28c86c9b01865d866d0ac4982af', enabled: true },

    // ============================================================================
    // POSTHOG - The Developer's Favorite (Analytics + Replay + Flags)
    // ============================================================================
    // Description:
    // An all-in-one product suite for developers.
    //
    // Key Features:
    // - Product Analytics + Session Recordings.
    // - Feature Flags & A/B Testing.
    // - Survey engine.
    //
    // Free Limits (2025):
    // - **1 Million Events / month**.
    // - **5,000 Session Recordings / month**.
    // - **Requires Credit Card** for overflow (use spend caps to stay free).
    //
    posthog: { key: 'phc_P9VZ5bjyFoWrIUbecuFTUN2oKavGQYqT3rVSxX8Kqn8', host: 'https://us.i.posthog.com', enabled: false },

    // ============================================================================
    // UMAMI - Privacy-First & Simple
    // ============================================================================
    // Description:
    // Clean, lightweight, and GDPR-compliant. No cookies, no tracking.
    //
    // Free Limits (Cloud 2025):
    // - **10,000 Events / month** (Basic Free plan).
    // - 3 Websites.
    // - *Note*: Previous 100k limits were reduced for new accounts.
    //
    umami: { id: '18b3773e-e365-458c-be78-d1d8238b4f15', host: 'https://cloud.umami.is', enabled: true },

    // ============================================================================
    // GOATCOUNTER - The Lightweight Alternative
    // ============================================================================
    // Description:
    // Simple, no-nonsense analytics for people who hate bloat.
    //
    // Free Limits:
    // - **100,000 Pageviews / month**.
    // - Unlimited sites for personal use.
    //
    goatcounter: { code: 'chirag127', enabled: true },

    // ============================================================================
    // CLOUDFLARE WEB ANALYTICS
    // ============================================================================
    // Description:
    // Privacy-first analytics at the network edge.
    //
    // Free Limits:
    // - **Totally Free** (Unlimited traffic).
    //
    cloudflare: { token: '333c0705152b4949b3eb0538cd4c2296', enabled: true }
};

export const analytics_general_priority = ['ga4', 'yandex', 'clarity', 'mixpanel', 'umami', 'goatcounter', 'cloudflare'];
export const analytics_lazyLoad = true;
