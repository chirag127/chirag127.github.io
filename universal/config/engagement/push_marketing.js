/**
 * Part 4: Engagement - Push Marketing (User Updates)
 * ENABLED for returning visitors
 * @module config/engagement/push_marketing
 */

export const push_marketing = {
    // ONESIGNAL - Best free tier, great for engagement
    onesignal: { appId: '', enabled: true },  // Enable when you have appId
    pushengage: { siteId: '', enabled: false },
    wonderpush: { webKey: '', enabled: false }
};

export const push_marketing_priority = ['onesignal'];
