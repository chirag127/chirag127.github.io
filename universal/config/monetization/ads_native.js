/**
 * Part 1: Monetization - Native Ads
 * Ads that look like content recommendations
 * @module config/monetization/ads_native
 */

export const ads_native = {
    // ============================================================================
    // MGID - Viral Content Widgets
    // ============================================================================
    // Description:
    // "You might also like" widgets often seen on news sites.
    //
    // Requirements:
    // - Moderate traffic required (~3,000 unique visitors/day often cited).
    // - Family-safe content (usually).
    //
    // Payout:
    // - NET-30.
    // - Min payout: $100.
    //
    mgid: { widgetId: '', enabled: false },

    // ============================================================================
    // TABOOLA - The Giant (High Barrier)
    // ============================================================================
    // Description:
    // World's largest discovery platform.
    //
    // Requirements:
    // - **EXTREME TRAFFIC BARRIER**: Typically 500,000+ monthly pageviews.
    // - NOT for new websites.
    //
    taboola: { publisherId: '', enabled: false },

    // ============================================================================
    // OUTBRAIN - Premium Native (High Barrier)
    // ============================================================================
    // Description:
    // High quality native ads for premium publishers.
    //
    // Requirements:
    // - **EXTREME TRAFFIC BARRIER**: Typically 1M+ monthly pageviews.
    //
    outbrain: { publisherId: '', enabled: false },

    // ============================================================================
    // ADNOW - Lower Barrier
    // ============================================================================
    // Description:
    // Widget based native ads.
    //
    // Requirements:
    // - Lower than Taboola/Outbrain, but still prefers active sites.
    //
    adnow: { widgetId: '', enabled: false }
};

export const ads_native_priority = ['mgid', 'adnow']; // Taboola/Outbrain removed from default priority due to limits
