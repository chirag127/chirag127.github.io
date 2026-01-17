/**
 * Part 2: Tracking - Analytics General
 * VISIBILITY FOCUS: All major analytics enabled for maximum insights
 * @module config/tracking/analytics_general
 */

export const analytics_general = {
    // BIG TECH - ALL ENABLED (Free, unlimited)
    ga4: { id: 'G-PQ26TN1XJ4', enabled: true, lazyLoad: false },  // Google - Primary
    yandex: { id: 106273806, enabled: true, webvisor: true, clickmap: true },  // Session replay
    clarity: { id: 'v1u8hhnpw2', enabled: true },  // Microsoft heatmaps

    // PRODUCT ANALYTICS - Enable one for deep insights
    mixpanel: { token: '8d06e28c86c9b01865d866d0ac4982af', enabled: true },  // User journeys
    amplitude: { apiKey: 'd1733215e7a8236a73912adf86ac450b', enabled: false },  // Alternative
    posthog: { key: 'phc_P9VZ5bjyFoWrIUbecuFTUN2oKavGQYqT3rVSxX8Kqn8', host: 'https://us.i.posthog.com', enabled: false },

    // PRIVACY-FOCUSED - Enable for EU visibility
    umami: { id: '18b3773e-e365-458c-be78-d1d8238b4f15', host: 'https://cloud.umami.is', enabled: true },
    goatcounter: { code: 'chirag127', enabled: true },  // Simple, fast
    counter_dev: { id: '5c0f4066-d78f-4cd8-a31d-40448c2f2749', enabled: true },

    // ADDITIONAL
    heap: { id: '3491046690', enabled: false },  // Auto-capture (heavy)
    logrocket: { id: 'nshsif/github-hub', enabled: false },  // Session replay (heavy)
    cloudflare: { token: '333c0705152b4949b3eb0538cd4c2296', enabled: true },  // Web analytics
    beam: { token: '1148dc4c-933b-4fd2-ba28-a0bb56f78978', enabled: false },
    cronitor: { key: '205a4c0b70da8fb459aac415c1407b4d', enabled: false },
    matomo: { url: '', siteId: '', enabled: false },
    clicky: { siteId: '', enabled: false }
};

export const analytics_general_priority = ['ga4', 'yandex', 'clarity', 'umami', 'goatcounter', 'mixpanel', 'cloudflare'];
export const analytics_lazyLoad = true;
