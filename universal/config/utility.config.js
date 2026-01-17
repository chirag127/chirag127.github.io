/**
 * Utility & Infrastructure Configuration
 * Essential website utilities
 *
 * @module config/utility
 */

export const utilityConfig = {

    // =========================================================================
    // COOKIE CONSENT (CMP)
    // =========================================================================

    // -------------------------------------------------------------------------
    // COOKIEBOT - GDPR compliant
    // -------------------------------------------------------------------------
    // HOW TO GET: https://www.cookiebot.com/
    // 1. Sign up (free for small sites < 100 pages)
    // 2. Add domain
    // 3. Get domain group ID (CBID)
    cookiebot: {
        domainGroupId: '',
        enabled: false
    },

    // -------------------------------------------------------------------------
    // OSANO - Cookie consent
    // -------------------------------------------------------------------------
    // HOW TO GET: https://www.osano.com/
    // 1. Sign up
    // 2. Get script
    osano: {
        scriptUrl: '',
        enabled: false
    },

    // =========================================================================
    // BOT PROTECTION / CAPTCHA
    // =========================================================================

    // -------------------------------------------------------------------------
    // GOOGLE RECAPTCHA v3 - Invisible protection
    // -------------------------------------------------------------------------
    // HOW TO GET: https://www.google.com/recaptcha/admin
    // 1. Sign in with Google
    // 2. Register new site (v3)
    // 3. Get site key and secret key
    recaptcha: {
        siteKey: '',      // Public
        secretKey: '',    // Server-side only, don't expose
        enabled: false
    },

    // -------------------------------------------------------------------------
    // hCAPTCHA - Privacy friendly, pays you!
    // -------------------------------------------------------------------------
    // HOW TO GET: https://www.hcaptcha.com/
    // 1. Sign up
    // 2. Add site
    // 3. Get site key
    // TIP: You earn HMT tokens when users solve captchas
    hcaptcha: {
        siteKey: '',
        enabled: false
    },

    // -------------------------------------------------------------------------
    // CLOUDFLARE TURNSTILE - Privacy friendly alternative
    // -------------------------------------------------------------------------
    // HOW TO GET: https://dash.cloudflare.com/ -> Turnstile
    // 1. Add widget
    // 2. Get site key
    turnstile: {
        siteKey: '',
        enabled: false
    },

    // =========================================================================
    // FONTS
    // =========================================================================

    // -------------------------------------------------------------------------
    // GOOGLE FONTS
    // -------------------------------------------------------------------------
    // HOW TO GET: https://fonts.google.com/
    // 1. Select fonts
    // 2. Copy embed link
    googleFonts: {
        enabled: true,
        families: ['Inter:wght@300;400;500;600;700;800']
    },

    // =========================================================================
    // ICONS
    // =========================================================================

    // -------------------------------------------------------------------------
    // FONT AWESOME
    // -------------------------------------------------------------------------
    // HOW TO GET: https://fontawesome.com/
    // 1. Create kit (free tier)
    // 2. Get kit code
    fontAwesome: {
        kitCode: '',
        enabled: false
    },

    // =========================================================================
    // SEARCH
    // =========================================================================

    // -------------------------------------------------------------------------
    // ALGOLIA - Search as a service
    // -------------------------------------------------------------------------
    // HOW TO GET: https://www.algolia.com/
    // 1. Sign up (free tier)
    // 2. Create index
    // 3. Get app ID and search key
    algolia: {
        appId: '',
        searchKey: '',
        indexName: '',
        enabled: false
    },

    // -------------------------------------------------------------------------
    // GOOGLE PROGRAMMABLE SEARCH
    // -------------------------------------------------------------------------
    // HOW TO GET: https://programmablesearchengine.google.com/
    // 1. Create search engine
    // 2. Get CX ID
    googleSearch: {
        cx: '',
        enabled: false
    },

    // =========================================================================
    // TRANSLATION
    // =========================================================================

    // -------------------------------------------------------------------------
    // GOOGLE TRANSLATE WIDGET
    // -------------------------------------------------------------------------
    // No signup needed
    googleTranslate: {
        enabled: false
    },

    // -------------------------------------------------------------------------
    // WEGLOT - Auto translation
    // -------------------------------------------------------------------------
    // HOW TO GET: https://weglot.com/
    // 1. Sign up (free for 1 language)
    // 2. Get API key
    weglot: {
        apiKey: '',
        enabled: false
    }
};
