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
    // One of the world's largest native ad networks. Known for "You might also like"
    // widgets often seen on news and viral sites.
    //
    // Key Features:
    // - High CPMs for Tier 1 traffic.
    // - Global advertiser coverage.
    //
    // Monetization Model:
    // - CPC (Cost Per Click) & CPM models.
    //
    // Requirements:
    // - Minimum 3,000 unique visitors/day (or ~90k/month).
    // - Clean, family-safe content (no illegal streams/downloads).
    //
    // Payout Details:
    // - Minimum Payout: $100.
    // - Frequency: Net-30.
    // - Methods: PayPal, Payoneer, Tipalti, Wire.
    //
    // Best For:
    // - News magazines, viral blogs, and high-traffic portals.
    //
    mgid: { widgetId: '', enabled: false },

    // ============================================================================
    // ADNOW - Accessible Native Ads
    // ============================================================================
    // Description:
    // A widget-based native ad network that is much easier to join than MGID/Taboola.
    //
    // Key Features:
    // - Fast Approval (often instant/24h).
    // - Weekly Payouts (Major advantage).
    // - Widget customization.
    //
    // Requirements:
    // - No minimum traffic strict requirement (Quality content check).
    // - Accepts newer sites.
    //
    // Payout Details:
    // - Minimum Payout: $20.
    // - Frequency: Net-7 (Weekly).
    // - Methods: PayPal, Wire, PM, Tether (USDT).
    //
    // Best For:
    // - Smaller blogs, niche sites, and publishers wanting weekly pay.
    //
    adnow: { widgetId: '', enabled: false }
};

export const ads_native_priority = ['mgid', 'adnow'];
