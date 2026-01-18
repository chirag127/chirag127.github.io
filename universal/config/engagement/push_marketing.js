/**
 * Part 3: Engagement - Push Marketing (Direct to Browser)
 * @module config/engagement/push_marketing
 */

export const push_marketing = {
    // ============================================================================
    // ONESIGNAL - The Industry Leader
    // ============================================================================
    // Description:
    // The most used push notification service for mobile and web.
    //
    // Free Tier Limits (2025):
    // - **10,000 Subscriptions**.
    // - Unlimited Web Push.
    // - OneSignal Branding on some notifications.
    //
    onesignal: { appId: '', enabled: false },

    // ============================================================================
    // WEB PUSH SDK (Native)
    // ============================================================================
    // Description:
    // Use the native Browser Push API.
    // Requires a service worker and VAPID keys.
    // **100% Free**.
    //
    web_push_native: { enabled: false }
};

export const push_marketing_priority = ['onesignal', 'web_push_native'];
