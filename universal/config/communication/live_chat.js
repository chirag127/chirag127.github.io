/**
 * Part 3: Communication - Live Chat
 * ENABLED for user support (reputation building)
 * @module config/communication/live_chat
 */

export const live_chat = {
    // TAWK.TO - Completely free, good reputation
    // Feature: Unlimited agents, real-time monitoring
    // Free Limit: 100% Free always
    tawkto: {
        source: 'https://embed.tawk.to/YOUR_PROPERTY_ID/default',
        enabled: true
    },

    // Crisp
    // Feature: Lightweight, modern UI
    // Free Limit: 2 seats, unlimited history (Basic)
    crisp: { websiteId: '', enabled: false },

    // Tidio
    // Feature: Chatbots + Live Chat combo
    // Free Limit: 50 conversations/month
    tidio: { publicKey: '', enabled: false },

    // Drift
    // Feature: B2B focused, rigorous playbooks
    // Free Limit: Very limited/Paid mainly
    drift: { embedId: '', enabled: false },

    // Intercom
    // Feature: Full enterprise customer engagement platform
    // Free Limit: No free tier (Trial only)
    intercom: { appId: '', enabled: false }
};

export const live_chat_priority = ['tawkto'];
