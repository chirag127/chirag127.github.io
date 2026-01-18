/* UNIVERSAL CONFIGURATION
   Hosted at: /universal/config.js
   Defines the SITE_CONFIG global object.

   NOTE: This file contains ONLY the runtime configuration values.
   The modular configuration structure is in /universal/config/ directory.
   For A/B testing config, see: /universal/config/engagement/ab_testing.js
*/

window.SITE_CONFIG = {
    // --- ANALYTICS STACK ---
    ga4: { id: 'G-PQ26TN1XJ4', enabled: true },
    yandex: { id: 106273806, enabled: true, webvisor: true, clickmap: true, trackLinks: true, accurateTrackBounce: true },
    clarity: { id: 'v1u8hhnpw2', enabled: true },
    cloudflare: { token: '333c0705152b4949b3eb0538cd4c2296', enabled: true },
    mixpanel: { token: '8d06e28c86c9b01865d866d0ac4982af', enabled: true },
    amplitude: { apiKey: 'd1733215e7a8236a73912adf86ac450b', enabled: true },
    posthog: { key: 'phc_P9VZ5bjyFoWrIUbecuFTUN2oKavGQYqT3rVSxX8Kqn8', host: 'https://us.i.posthog.com', enabled: true },
    umami: { id: '18b3773e-e365-458c-be78-d1d8238b4f15', host: 'https://cloud.umami.is', enabled: true },
    goatcounter: { code: 'chirag127', enabled: true },
    heap: { id: '3491046690', enabled: true },
    logrocket: { id: 'nshsif/github-hub', enabled: true },
    beam: { token: '1148dc4c-933b-4fd2-ba28-a0bb56f78978', enabled: true },
    counter_dev: { id: '5c0f4066-d78f-4cd8-a31d-40448c2f2749', enabled: true },
    cronitor: { key: '205a4c0b70da8fb459aac415c1407b4d', enabled: true },

    // --- MONETIZATION (Ads) ---
    propeller: { zone: '202358', enabled: true },
    adsense: { id: '', enabled: false },

    // --- CHAT ---
    tawk: { src: 'https://embed.tawk.to/6968e3ea8783b31983eb190b/1jf0rkjhp', enabled: true },

    // --- ERROR TRACKING ---
    sentry: { dsn: 'https://45890ca96ce164182a3c74cca6018e3e@o4509333332164608.ingest.de.sentry.io/4509333334458448', enabled: true },
    honeybadger: { apiKey: 'hbp_x8dJHBTim5uTkF7pIZVqj55X4wedmR11iovM', enabled: true },
    rollbar: { accessToken: '88062048efd74f7c8e11659187da782b', enabled: true },
    bugsnag: { apiKey: '84afb61cb3bf458037f4f15eeab394c4', enabled: true },
    glitchtip: { dsn: 'https://fe8b6978187b4ef09020464050d17b06@app.glitchtip.com/19542', enabled: true },

    // --- AUTHENTICATION ---
    auth0: { domain: '', clientId: '' },
    clerk: { publishableKey: '' },
    supabase: { url: '', anonKey: '' }
};
