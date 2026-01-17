/**
 * Part 3: Communication - Live Chat
 * ENABLED for user support (reputation building)
 * @module config/communication/live_chat
 */

export const live_chat = {
    // TAWK.TO - Completely free, good reputation
    tawkto: {
        source: 'https://embed.tawk.to/YOUR_PROPERTY_ID/default',
        enabled: true
    },
    crisp: { websiteId: '', enabled: false },
    tidio: { publicKey: '', enabled: false },
    drift: { embedId: '', enabled: false },
    intercom: { appId: '', enabled: false }
};

export const live_chat_priority = ['tawkto'];
