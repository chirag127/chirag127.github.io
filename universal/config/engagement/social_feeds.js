/**
 * Part 4: Engagement - Social Media Feeds
 * Embed Instagram, TikTok, Twitter feeds
 * @module config/engagement/social_feeds
 */

export const social_feeds = {
    elfsight: { appId: '', enabled: true },  // Multi-platform widgets
    juicer: { feedId: '', enabled: false },
    curator: { feedId: '', enabled: false }
};

export const social_feeds_priority = ['elfsight', 'juicer', 'curator'];
