/**
 * Part 4: Engagement - Notification Bells
 * In-app notification center
 * @module config/engagement/notification_bells
 */

export const notification_bells = {
    // SuprSend
    // Feature: Multi-channel workflow (Email + In-app)
    // Free Limit: 10,000 notifications/month (Generous)
    suprsend: { workspaceKey: '', enabled: true },

    // MagicBell
    // Feature: Retro-fit notification center to any app
    // Free Limit: 1,000 notifications/month
    magicbell: { apiKey: '', userExternalId: '', enabled: false }
};

export const notification_bells_priority = ['suprsend', 'magicbell'];
