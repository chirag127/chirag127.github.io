/**
 * Part 1: Monetization - Interstitial Ads
 * Full-screen ads between pages - use sparingly
 * @module config/monetization/ads_interstitial
 */

export const ads_interstitial = {
    // ============================================================================
    // INTERSTITIALS / VIGNETTES
    // ============================================================================
    // Description:
    // Full screen ads that appear between page loads.
    //
    // Best Provider (Generous & Compliant):
    // - Google AdSense (Vignette Ads): Automatically handles frequency capping and UX.
    //   Enable "Auto Ads" in ads_display.js for this.
    //
    // Alternatives:
    //
    adsterra_interstitial: { zoneId: '', enabled: false }, // High CPM, typically safe.
    infolinks_inscreen: { publisherId: '', enabled: false } // "InScreen" format.
};

export const ads_interstitial_priority = ['adsterra_interstitial', 'infolinks_inscreen'];


export const ads_interstitial_frequency = { maxPerSession: 1, secondsBetween: 300 };
