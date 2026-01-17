/**
 * Analytics Configuration
 * Public keys for analytics providers
 * @module config/analytics
 */

export const analyticsConfig = {
    ga4: {
        id: 'G-PQ26TN1XJ4',
        enabled: true
    },
    yandex: {
        id: 106273806,
        enabled: true,
        webvisor: true,
        clickmap: true,
        trackLinks: true,
        accurateTrackBounce: true
    },
    clarity: {
        id: 'v1u8hhnpw2',
        enabled: true
    },
    cloudflare: {
        token: '333c0705152b4949b3eb0538cd4c2296',
        enabled: true
    },
    mixpanel: {
        token: '8d06e28c86c9b01865d866d0ac4982af',
        enabled: true
    },
    amplitude: {
        apiKey: 'd1733215e7a8236a73912adf86ac450b',
        enabled: true
    },
    posthog: {
        key: 'phc_P9VZ5bjyFoWrIUbecuFTUN2oKavGQYqT3rVSxX8Kqn8',
        host: 'https://us.i.posthog.com',
        enabled: true
    },
    umami: {
        id: '18b3773e-e365-458c-be78-d1d8238b4f15',
        host: 'https://cloud.umami.is',
        enabled: true
    },
    goatcounter: {
        code: 'chirag127',
        enabled: true
    },
    heap: {
        id: '3491046690',
        enabled: true
    },
    logrocket: {
        id: 'nshsif/github-hub',
        enabled: true
    },
    beam: {
        token: '1148dc4c-933b-4fd2-ba28-a0bb56f78978',
        enabled: true
    },
    counter_dev: {
        id: '5c0f4066-d78f-4cd8-a31d-40448c2f2749',
        enabled: true
    },
    cronitor: {
        key: '205a4c0b70da8fb459aac415c1407b4d',
        enabled: true
    }
};
