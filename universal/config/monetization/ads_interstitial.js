/**
 * Part 1: Monetization - Interstitial Ads
 * Full-screen ads between pages - use sparingly
 * @module config/monetization/ads_interstitial
 */

export const ads_interstitial = {
    // ============================================================================
    // GOOGLE ADSENSE VIGNETTES
    // ============================================================================
    // Description:
    // Full screen mobile/desktop ads that appear between page loads.
    // Managed automatically by Google for best user experience.
    //
    // Requirements:
    // - Active AdSense account.
    //
    // Best For:
    // - Clean, policy-compliant sites.
    //
    // configured via 'autoAds: true' in ads_display.js

    // ============================================================================
    // ADSTERRA INTERSTITIALS
    // ============================================================================
    // Description:
    // High-CPM full screen ads. Aggressive but highly profitable.
    //
    // Key Features:
    // - Smart frequency capping options.
    // - High payout rates for Pop/Social traffic.
    //
    // Payout Details:
    // - Min: $5 (Paxum), $100 (others).
    // - Net-15.
    //
    adsterra_interstitial: { zoneId: '', enabled: false },

    // ============================================================================
    // INFOLINKS - InScreen
    // ============================================================================
    // Description:
    // "InScreen" intersitial that acts as an "in-between" ad.
    //
    // Key Features:
    // - Intent-based targeting.
    // - Less intrusive than traditional pop-ups.
    //
    // Requirements:
    // - No strict minimum traffic, but approved content required.
    // - 5-10 pages of quality content.
    //
    // Payout Details:
    // - Minimum Payout: $50 (PayPal, Payoneer).
    // - Frequency: Net-45.
    //
    // Best For:
    // - Text-heavy content sites/blogs.
    //
    infolinks_inscreen: { publisherId: '', enabled: false }
};

export const ads_interstitial_priority = ['adsterra_interstitial', 'infolinks_inscreen'];
export const ads_interstitial_frequency = { maxPerSession: 1, secondsBetween: 300 };
