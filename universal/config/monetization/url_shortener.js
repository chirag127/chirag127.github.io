/**
 * Part 1: Monetization - URL Shorteners
 * @module config/monetization/url_shortener
 */

    // ============================================================================
    // OUO.IO - Reliable & Consistent
    // ============================================================================
    // Description:
    // A long-standing, legitimate URL shortener service.
    // Known for actually paying on time for years.
    //
    // Key Features:
    // - Multi-count: Counts multiple views from the same IP (up to 3).
    // - Clean Interface: User dashboard is simple and effective.
    // - Mass Shrinker tool.
    //
    // Monetization Model:
    // - CPM (Cost Per 1000 Views).
    // - Rates: $1.50 - $5.00+ depending on country (Tier 1 pays highest).
    //
    // Payout Details:
    // - Minimum: $5 (PayPal/Payeer), $50 (Payoneer), $20 (Bitcoin).
    // - Frequency: 1st and 15th of every month (Net-15ish).
    //
    // Best For:
    // - General traffic, download links.
    //
    ouoio: { apiToken: '', enabled: true },

    // ============================================================================
    // SHRINKME.IO - High Payout Rates
    // ============================================================================
    // Description:
    // One of the highest paying URL shorteners currently active.
    //
    // Key Features:
    // - High CPM rates (up to $220/10,000 views for Greenland, ~$3-$10 for others).
    // - Low minimum payout.
    // - Daily payments.
    //
    // Payout Details:
    // - Minimum: $5.
    // - Frequency: Daily.
    // - Methods: PayPal, Bitcoin, Payeer, Skrill, UPI (India), Bank Transfer.
    //
    shrinkMe: { apiToken: '', enabled: false },

    // ============================================================================
    // AROLINKS - High Rates (India/Global)
    // ============================================================================
    // Description:
    // Popular for high CPM rates and trusted reputation.
    //
    // Key Features:
    // - CPM up to $8.
    // - Very low minimum withdrawal which is great for starters.
    //
    // Payout Details:
    // - Minimum: $0.50 (some methods) - $2.00.
    // - Support for UPI, PhonePe (Great for Indian traffic).
    //
    arolinks: { apiToken: '', enabled: false },

    // ============================================================================
    // SHRINKEARN
    // ============================================================================
    // Description:
    // Established in 2018, legit paying network.
    //
    // Key Features:
    // - Competitive rates ($3 - $20 CPM).
    // - Referral program (20%).
    //
    shrinkEarn: { apiKey: '', enabled: false },

    // ============================================================================
    // GPLINKS - Modern & High Performance
    // ============================================================================
    // Description:
    // Modern UI and distinct from the "retro" look of others.
    //
    // Key Features:
    // - High performance and detailed analytics.
    // - Rates: Competitive.
    //
    gplinks: { apiKey: '', enabled: false }
};

export const url_shortener_priority = ['ouoio', 'shrinkMe', 'arolinks', 'shrinkEarn', 'gplinks'];
