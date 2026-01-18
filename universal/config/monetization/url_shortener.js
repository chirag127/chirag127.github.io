/**
 * Part 1: Monetization - URL Shorteners
 * @module config/monetization/url_shortener
 */

export const url_shortener = {
    // ============================================================================
    // OUO.IO - The Reliable Veteran
    // ============================================================================
    // Description:
    // One of the longest-running and most stable URL shorteners in the industry.
    //
    // Key Features:
    // - High Payout Stability: Known for years of on-time payments.
    // - Multi-View Counting: Counts up to 3 views per IP.
    // - Mass Shrinker: Easily shorten many links at once.
    //
    // Monetization Model:
    // - CPM (Cost Per 1000 Views).
    // - Rates: ~$1.50 - $5.00+ (Varies by country).
    //
    // Payout Details:
    // - Minimum Payout: $5 (PayPal, Payeer), $20 (Bitcoin, USDT TRC-20), $50 (Payoneer).
    // - Frequency: 1st and 15th of every month.
    //
    // Best For:
    // - General download links and high-traffic portals where stability is #1.
    //
    ouoio: { apiToken: '', enabled: true },

    // ============================================================================
    // SHRINKME.IO - Top CPM earner (2025)
    // ============================================================================
    // Description:
    // Currently offers some of the highest CPM rates in the market.
    //
    // Key Features:
    // - **Aggressive Rates**: Up to $22 CPM (Greenland), ~$14 (US), ~$3.50 (Worldwide).
    // - Multiple Gateways: Supports UPI/Paytm (India), Cards, and Crypto.
    //
    // Payout Details:
    // - Minimum Payout: $5.
    // - Frequency: Daily (Extremely fast).
    //
    shrinkMe: { apiToken: '', enabled: false },

    // ============================================================================
    // GPLINKS - Professional Analytical Platform
    // ============================================================================
    // Description:
    // Modern UI with advanced tracking and higher-tier CPM for premium publishers.
    //
    // Key Features:
    // - Standard & Premium Plans.
    // - High Tier CPM: Up to $25 for certain premium traffic.
    //
    // Payout Details:
    // - Minimum Payout: $5.
    //
    gplinks: { apiKey: '', enabled: false },

    // ============================================================================
    // AROLINKS - Optimized for India
    // ============================================================================
    // Payout Details:
    // - Minimum Payout: $0.50 (Some methods).
    // - Supports UPI / PhonePe.
    //
    arolinks: { apiToken: '', enabled: false },

    // ============================================================================
    // SHRINKEARN - Long Term Trusted
    // ============================================================================
    shrinkEarn: { apiKey: '', enabled: false }
};

export const url_shortener_priority = ['ouoio', 'shrinkMe', 'gplinks', 'arolinks', 'shrinkEarn'];
