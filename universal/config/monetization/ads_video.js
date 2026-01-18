/**
 * Part 1: Monetization - Video Ads
 * Pre-roll and outstream video ads
 * @module config/monetization/ads_video
 */

export const ads_video = {
    // ============================================================================
    // VIDOOMY - Premium Video Slider
    // ============================================================================
    // Description:
    // High-impact sliding video ads for premium publishers.
    //
    // Requirements:
    // - **VERY HIGH**: 3 Million+ pageviews/month often cited.
    // - 500+ Original articles.
    // - Top-level domains only.
    //
    // Best For:
    // - Large media houses and viral news sites.
    //
    vidoomy: { publisherId: '', enabled: false },

    // ============================================================================
    // PRIMIS - Video Discovery
    // ============================================================================
    // Description:
    // A video player that recommends content to users and runs ads.
    //
    // Requirements:
    // - ~200,000 monthly pageviews.
    // - High engagement metrics.
    //
    // Payout Details:
    // - Minimum Payout: $50.
    // - Frequency: Net-15.
    //
    primis: { widgetId: '', enabled: false },

    // ============================================================================
    // ADPLAYER.PRO - Outstream Technology
    // ============================================================================
    // Description:
    // Professional video player with built-in monetization.
    //
    // Requirements:
    // - Variable, generally strictly for established sites.
    //
    // Payout Details:
    // - Minimum Payout: $100.
    // - Frequency: Net-30.
    //
    adplayerPro: { publisherId: '', enabled: false }
};

export const ads_video_priority = ['vidoomy', 'primis', 'adplayerPro'];
