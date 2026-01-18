/**
 * Part 4: Engagement - Push Marketing (User Updates)
 * ENABLED for returning visitors
 * @module config/engagement/push_marketing
 */

export const push_marketing = {
    // ONESIGNAL - Best free tier, great for engagement
    // Feature: Unlimited subscribers, segmentation
    // Free Limit: Unlimited web subscribers (Max 10k per send)
    onesignal: { appId: '', enabled: true },  // Enable when you have appId

    // PushEngage
    // Feature: Cart abandonment campaigns
    // Free Limit: 200 subscribers, 30 campaigns
    pushengage: { siteId: '', enabled: false }
};

export const push_marketing_priority = ['onesignal', 'pushengage'];
