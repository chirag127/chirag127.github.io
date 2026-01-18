/**
 * Part 4: Engagement - Social Media Feeds
 * Embed Instagram, TikTok, Twitter feeds
 * @module config/engagement/social_feeds
 */

export const social_feeds = {
    // Curator
    // Feature: Clean, masonry grid layouts
    // Free Limit: 3 sources, 2,000 views/month (Branded)
    curator: { feedId: '', enabled: true },

    // Juicer
    // Feature: Aggregates multiple social sources into one feed
    // Free Limit: 1 source feed, 24 hour updates (Branded)
    juicer: { feedId: '', enabled: false },

    // Elfsight
    // Feature: Beautiful, highly customizable widgets for everything
    // Free Limit: 1 widget, 200 views/month (Very restrictive)
    elfsight: { appId: '', enabled: false }
};

export const social_feeds_priority = ['curator', 'juicer', 'elfsight'];
