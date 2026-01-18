/**
 * Part 1: Monetization - Interstitial Ads
 * Full-screen ads between pages - use sparingly
 * @module config/monetization/ads_interstitial
 */

export const ads_interstitial = {
    // All disabled - very aggressive format
    // Adsterra Interstitial
    // Feature: High CPM, frequency capped
    // Aggression: High
    adsterra_interstitial: { zoneId: '', enabled: false },

    // Monetag Vignette
    // Feature: Google-compliant interstitial styling
    // Aggression: Medium
    monetag_vignette: { zoneId: '', enabled: false },

    // Infolinks
    // Feature: "InScreen" ads between page views
    // Aggression: Low
    infolinks_inscreen: { publisherId: '', enabled: false }
};

export const ads_interstitial_priority = ['infolinks_inscreen', 'monetag_vignette', 'adsterra_interstitial'];  // Ordered by least aggressive
export const ads_interstitial_frequency = { maxPerSession: 1, secondsBetween: 300 };
