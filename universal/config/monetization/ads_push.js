/**
 * Part 1: Monetization - Push Notification Ads
 * ALL DISABLED - These can be intrusive and hurt user trust
 * @module config/monetization/ads_push
 */

export const ads_push = {
    // ============================================================================
    // EVADAV - Flexible Push Network
    // ============================================================================
    // Description:
    // A rapidly growing ad network focusing on push notifications.
    // Known for accepting traffic from all geos and smaller sites.
    //
    // Key Features:
    // - Flexible: Accepts 100+ daily visitors.
    // - Weekly Payouts (Automatic).
    // - Global Geo coverage.
    //
    // Monetization Model:
    // - CPC (Cost Per Click) & CPM models.
    //
    // Requirements:
    // - Minimal traffic required (100+ visitors).
    // - SSL Certificate (HTTPS) required.
    // - No malware/illegal content.
    //
    // Payout Details:
    // - Minimum Payout: $25 (PayPal, Skrill, Paxum, Bitcoin).
    // - Frequency: Weekly (every Tuesday).
    //
    // Best For:
    // - New sites, streaming sites, or download portals.
    //
    evadav: { siteId: '', enabled: false },

    // ============================================================================
    // RICHADS - Premium Push
    // ============================================================================
    // Description:
    // High-quality push network.
    //
    // Key Features:
    // - Target CPA.
    // - Smart CPC.
    //
    // Payout Details:
    // - Minimum Payout: $10 (Capitalist, Cards).
    // - Frequency: Bi-weekly (Net-15).
    //
    richads: { publisherId: '', enabled: false },

    // ============================================================================
    // PARTNERS.HOUSE (PUSH HOUSE)
    // ============================================================================
    // Description:
    // Monetization arm of Push.House.
    //
    // Payout Details:
    // - Minimum Payout: $50.
    // - Methods: WebMoney, Bitcoin, Capitalist.
    //
    pushHouse: { publisherId: '', enabled: false }
};

export const ads_push_priority = [];
