/**
 * Chat & Communication Configuration
 * Live chat widgets for user support
 *
 * @module config/chat
 */

export const chatConfig = {

    // =========================================================================
    // TAWK.TO - 100% Free, feature-rich
    // =========================================================================
    // HOW TO GET: https://www.tawk.to/
    // 1. Sign up (completely free)
    // 2. Add website
    // 3. Get widget script URL from Administration -> Channels -> Chat Widget
    tawk: {
        src: 'https://embed.tawk.to/6968e3ea8783b31983eb190b/1jf0rkjhp',  // YOUR EXISTING SRC
        enabled: true
    },

    // =========================================================================
    // CRISP - Generous free tier
    // =========================================================================
    // HOW TO GET: https://crisp.chat/
    // 1. Sign up
    // 2. Create website
    // 3. Get website ID from Settings -> Website -> Setup Instructions
    crisp: {
        websiteId: '',
        enabled: false  // Fallback to Tawk
    },

    // =========================================================================
    // TIDIO - Chat + Bots
    // =========================================================================
    // HOW TO GET: https://www.tidio.com/
    // 1. Sign up (free tier)
    // 2. Add website
    // 3. Get public key from Settings -> Installation
    tidio: {
        publicKey: '',
        enabled: false
    },

    // =========================================================================
    // INTERCOM - Premium chat
    // =========================================================================
    // HOW TO GET: https://www.intercom.com/
    // 1. Sign up (paid with trial)
    // 2. Get app ID
    intercom: {
        appId: '',
        enabled: false
    },

    // =========================================================================
    // DRIFT - Conversational marketing
    // =========================================================================
    // HOW TO GET: https://www.drift.com/
    // 1. Sign up (free tier available)
    // 2. Get Drift key
    drift: {
        key: '',
        enabled: false
    },

    // =========================================================================
    // ZENDESK CHAT - Support focused
    // =========================================================================
    // HOW TO GET: https://www.zendesk.com/chat/
    // 1. Sign up
    // 2. Get widget key
    zendesk: {
        key: '',
        enabled: false
    },

    // =========================================================================
    // FRESHCHAT - Modern chat
    // =========================================================================
    // HOW TO GET: https://www.freshworks.com/live-chat-software/
    // 1. Sign up
    // 2. Get token
    freshchat: {
        token: '',
        enabled: false
    }
};

// Only one chat widget at a time
// Use first enabled in priority order
export const chatPriority = [
    'tawk',      // Free, primary
    'crisp',     // Fallback
    'tidio',
    'drift',
    'intercom',
    'zendesk',
    'freshchat'
];
