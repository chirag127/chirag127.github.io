/**
 * Part 1: Monetization - Interstitial Ads
 * Full-screen ads between pages - use sparingly
 * @module config/monetization/ads_interstitial
 */

export const ads_interstitial = {
    // All disabled - very aggressive format
    adsterra_interstitial: { zoneId: '', enabled: false },
    monetag_vignette: { zoneId: '', enabled: false },
    infolinks_inscreen: { publisherId: '', enabled: false }
};

export const ads_interstitial_priority = [];  // Empty by default
export const ads_interstitial_frequency = { maxPerSession: 1, secondsBetween: 300 };
