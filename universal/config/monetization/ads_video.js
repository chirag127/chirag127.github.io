/**
 * Part 1: Monetization - Video Ads
 * Pre-roll and outstream video ads
 * @module config/monetization/ads_video
 */

export const ads_video = {
    // Video ad networks - all disabled
    // Vidoomy
    // Feature: Slider video formats
    // Requirement: 300,000 pageviews/month
    vidoomy: { publisherId: '', enabled: false },

    // Primis
    // Feature: Discover video player
    // Requirement: High engagement metrics
    primis: { widgetId: '', enabled: false },

    // AdPlayer.Pro
    // Feature: Outstream video player technology
    adplayerPro: { publisherId: '', enabled: false }
};

export const ads_video_priority = ['vidoomy', 'primis', 'adplayerPro'];
