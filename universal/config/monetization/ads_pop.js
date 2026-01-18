/**
 * Part 1: Monetization - Pop-Under Networks
 * ALL DISABLED - These are aggressive, hurt SEO, and may trigger AdSense ban
 * @module config/monetization/ads_pop
 */

export const ads_pop = {
    // ============================================================================
    // POPADS - The Market Leader
    // ============================================================================
    // Description:
    // Specialized pop-under network running since 2010.
    //
    // Key Features:
    // - Real-time bidding (High CPM).
    // - Bid control (Set minimum CPM).
    // - Instant payments.
    //
    // Requirements:
    // - No minimum traffic.
    // - Accepts almost all sites.
    //
    // Payout Details:
    // - Minimum Payout: $5.
    // - Frequency: Daily / On Request (Instant).
    // - Methods: PayPal, AlertPay, Wire.
    //
    popads: { publisherId: '', enabled: false, _warning: 'AGGRESSIVE FORMAT' },

    // ============================================================================
    // POPCASH - Fast & Simple
    // ============================================================================
    // Description:
    // User-friendly pop-under network with daily payments.
    //
    // Key Features:
    // - Fast approval (often 1 hour).
    // - 24/7 Support.
    //
    // Requirements:
    // - No minimum traffic.
    //
    // Payout Details:
    // - Minimum Payout: $10.
    // - Frequency: Daily (24-48h processing).
    // - Methods: PayPal, Paxum, Skrill, Bitcoin.
    //
    popcash: { publisherId: '', enabled: false, _warning: 'AGGRESSIVE FORMAT' },

    // ============================================================================
    // CLICKADU - Multi-Format Premium
    // ============================================================================
    // Description:
    // Premium ad network offering pops along with video/push.
    //
    // Key Features:
    // - 100% Fill rate.
    // - Clean ads (strong anti-fraud).
    //
    // Requirements:
    // - No strict minimum (5k+ daily recommended).
    //
    // Payout Details:
    // - Minimum Payout: ~$50 (varies by method).
    // - Frequency: Net-7 / Net-30.
    //
    clickadu: { siteId: '', enabled: false, _warning: 'AGGRESSIVE FORMAT' }
};

export const ads_pop_priority = [];
export const ads_pop_limits = { maxPopsPerDay: 0, daysBetweenPops: 7 };  // Effectively disabled
