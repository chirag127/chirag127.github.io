/**
 * Part 3: Engagement - Notification Bells & Widgets
 * @module config/engagement/notification_bells
 */

export const notification_bells = {
    // ============================================================================
    // MAGIC BELL - Real-time Notifications
    // ============================================================================
    // Description:
    // A notification inbox for your website.
    //
    // Free Tier Limits:
    // - **10,000 Monthly Active Users**.
    // - Real-time push, email, and mobile notifications.
    //
    magicbell: { apiKey: '', enabled: false },

    // ============================================================================
    // NOVU - Open Source Infrastructure
    // ============================================================================
    // Description:
    // Notification engine that connects to multiple providers.
    //
    novu: { apiKey: '', enabled: false }
};

export const notification_bells_priority = ['magicbell', 'novu'];
