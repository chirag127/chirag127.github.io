/**
 * Part 4: Engagement - Social Media Feeds
 * Embed Instagram, TikTok, Twitter feeds
 * @module config/engagement/social_feeds
 */

export const social_feeds = {
    // Elfsight
    // Feature: Beautiful, highly customizable widgets for everything
    // Free Limit: 1 widget per app, 200 views/month (Very restrictive)
    elfsight: { appId: '', enabled: true },  // Multi-platform widgets

    // Juicer
    // Feature: Aggregates multiple social sources into one feed
    // Free Limit: 1 feed, 2 source accounts (Branded)
    juicer: { feedId: '', enabled: false },

    // Curator
    // Feature: Clean, masonry grid layouts
    // Free Limit: 3 sources, 2000 views/month (Branded)
    curator: { feedId: '', enabled: false }
};

export const social_feeds_priority = ['elfsight', 'juicer', 'curator'];
