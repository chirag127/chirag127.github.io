/**
 * Comprehensive Analytics Configuration
 * All analytics providers with your existing configurations
 *
 * @module config/analytics
 */

export const analyticsConfig = {

    // =========================================================================
    // GOOGLE ANALYTICS 4 - Industry standard
    // =========================================================================
    // HOW TO GET: https://analytics.google.com/
    // 1. Create Google Analytics property
    // 2. Select Web stream
    // 3. Get Measurement ID (G-XXXXXXXXXX)
    ga4: {
        id: 'G-PQ26TN1XJ4',  // YOUR EXISTING ID
        enabled: true
    },

    // =========================================================================
    // YANDEX METRICA - Includes free session replay
    // =========================================================================
    // HOW TO GET: https://metrica.yandex.com/
    // 1. Sign up with Yandex account
    // 2. Add website
    // 3. Get counter ID (number)
    yandex: {
        id: 106273806,  // YOUR EXISTING ID
        enabled: true,
        webvisor: true,
        clickmap: true,
        trackLinks: true,
        accurateTrackBounce: true
    },

    // =========================================================================
    // MICROSOFT CLARITY - Free heatmaps & recordings
    // =========================================================================
    // HOW TO GET: https://clarity.microsoft.com/
    // 1. Sign up with Microsoft account
    // 2. Create project
    // 3. Get project ID
    clarity: {
        id: 'v1u8hhnpw2',  // YOUR EXISTING ID
        enabled: true
    },

    // =========================================================================
    // CLOUDFLARE WEB ANALYTICS - Privacy focused
    // =========================================================================
    // HOW TO GET: https://dash.cloudflare.com/
    // 1. Go to Analytics -> Web Analytics
    // 2. Add site
    // 3. Get beacon token
    cloudflare: {
        token: '333c0705152b4949b3eb0538cd4c2296',  // YOUR EXISTING TOKEN
        enabled: true
    },

    // =========================================================================
    // MIXPANEL - Product analytics
    // =========================================================================
    // HOW TO GET: https://mixpanel.com/
    // 1. Create account
    // 2. Create project
    // 3. Get project token
    mixpanel: {
        token: '8d06e28c86c9b01865d866d0ac4982af',  // YOUR EXISTING TOKEN
        enabled: true
    },

    // =========================================================================
    // AMPLITUDE - Product analytics
    // =========================================================================
    // HOW TO GET: https://amplitude.com/
    // 1. Sign up
    // 2. Create project
    // 3. Get API key
    amplitude: {
        apiKey: 'd1733215e7a8236a73912adf86ac450b',  // YOUR EXISTING KEY
        enabled: true
    },

    // =========================================================================
    // POSTHOG - Open source product analytics
    // =========================================================================
    // HOW TO GET: https://posthog.com/
    // 1. Sign up (cloud or self-host)
    // 2. Create project
    // 3. Get project API key
    posthog: {
        key: 'phc_P9VZ5bjyFoWrIUbecuFTUN2oKavGQYqT3rVSxX8Kqn8',  // YOUR EXISTING KEY
        host: 'https://us.i.posthog.com',
        enabled: true
    },

    // =========================================================================
    // UMAMI - Privacy focused analytics
    // =========================================================================
    // HOW TO GET: https://umami.is/
    // 1. Sign up for cloud or self-host
    // 2. Add website
    // 3. Get website ID
    umami: {
        id: '18b3773e-e365-458c-be78-d1d8238b4f15',  // YOUR EXISTING ID
        host: 'https://cloud.umami.is',
        enabled: true
    },

    // =========================================================================
    // GOATCOUNTER - Simple, privacy friendly
    // =========================================================================
    // HOW TO GET: https://www.goatcounter.com/
    // 1. Sign up (free for personal use)
    // 2. Add site
    // 3. Get code
    goatcounter: {
        code: 'chirag127',  // YOUR EXISTING CODE
        enabled: true
    },

    // =========================================================================
    // HEAP - Auto-capture analytics
    // =========================================================================
    // HOW TO GET: https://heap.io/
    // 1. Sign up
    // 2. Create project
    // 3. Get environment ID
    heap: {
        id: '3491046690',  // YOUR EXISTING ID
        enabled: true
    },

    // =========================================================================
    // LOGROCKET - Session replay + logging
    // =========================================================================
    // HOW TO GET: https://logrocket.com/
    // 1. Sign up
    // 2. Create project
    // 3. Get app ID (org/project format)
    logrocket: {
        id: 'nshsif/github-hub',  // YOUR EXISTING ID
        enabled: true
    },

    // =========================================================================
    // BEAM ANALYTICS - Simple analytics
    // =========================================================================
    // HOW TO GET: https://beamanalytics.io/
    // 1. Sign up
    // 2. Add website
    // 3. Get token
    beam: {
        token: '1148dc4c-933b-4fd2-ba28-a0bb56f78978',  // YOUR EXISTING TOKEN
        enabled: true
    },

    // =========================================================================
    // COUNTER.DEV - Privacy focused
    // =========================================================================
    // HOW TO GET: https://counter.dev/
    // 1. Sign up
    // 2. Get ID
    counter_dev: {
        id: '5c0f4066-d78f-4cd8-a31d-40448c2f2749',  // YOUR EXISTING ID
        enabled: true
    },

    // =========================================================================
    // CRONITOR RUM - Real user monitoring
    // =========================================================================
    // HOW TO GET: https://cronitor.io/
    // 1. Sign up
    // 2. Enable RUM
    // 3. Get client key
    cronitor: {
        key: '205a4c0b70da8fb459aac415c1407b4d',  // YOUR EXISTING KEY
        enabled: true
    },

    // =========================================================================
    // WOOPRA - Customer journey analytics
    // =========================================================================
    // HOW TO GET: https://www.woopra.com/
    // 1. Sign up
    // 2. Add domain
    woopra: {
        domain: '',
        enabled: false
    },

    // =========================================================================
    // STATCOUNTER - Classic free analytics
    // =========================================================================
    // HOW TO GET: https://statcounter.com/
    // 1. Sign up
    // 2. Add project
    // 3. Get project ID and security code
    statcounter: {
        projectId: '',
        securityCode: '',
        enabled: false
    },

    // =========================================================================
    // CLICKY - Real-time analytics
    // =========================================================================
    // HOW TO GET: https://clicky.com/
    // 1. Sign up (free for 1 site)
    // 2. Add site
    // 3. Get site ID
    clicky: {
        siteId: '',
        enabled: false
    },

    // =========================================================================
    // MATOMO CLOUD - Privacy focused
    // =========================================================================
    // HOW TO GET: https://matomo.org/matomo-cloud/
    // 1. Sign up for cloud trial
    // 2. Get URL and site ID
    matomo: {
        url: '',
        siteId: '',
        enabled: false
    },

    // =========================================================================
    // SWETRIX - Open source analytics
    // =========================================================================
    // HOW TO GET: https://swetrix.com/
    // 1. Sign up
    // 2. Create project
    // 3. Get project ID
    swetrix: {
        projectId: '',
        enabled: false
    },

    // =========================================================================
    // PLAUSIBLE - Privacy first
    // =========================================================================
    // HOW TO GET: https://plausible.io/
    // 1. Sign up (paid, has trial)
    // 2. Add domain
    plausible: {
        domain: '',
        enabled: false
    },

    // =========================================================================
    // FATHOM - Simple privacy analytics
    // =========================================================================
    // HOW TO GET: https://usefathom.com/
    // 1. Sign up (paid)
    // 2. Add site
    // 3. Get site ID
    fathom: {
        siteId: '',
        enabled: false
    },

    // =========================================================================
    // SIMPLE ANALYTICS
    // =========================================================================
    // HOW TO GET: https://simpleanalytics.com/
    // Paid, privacy focused
    simpleAnalytics: {
        enabled: false
    }
};

// All analytics run simultaneously for maximum data collection
export const analyticsLoadOrder = [
    'ga4',           // Google first
    'clarity',       // Microsoft heatmaps
    'yandex',        // Yandex with webvisor
    'posthog',       // Product analytics
    'mixpanel',      // Event tracking
    'amplitude',     // User analytics
    'heap',          // Auto-capture
    'logrocket',     // Session replay
    'umami',
    'cloudflare',
    'goatcounter',
    'beam',
    'counter_dev',
    'cronitor'
];
