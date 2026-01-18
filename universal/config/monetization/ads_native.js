/**
 * Part 1: Monetization - Native Ads
 * Ads that look like content recommendations
 * @module config/monetization/ads_native
 */

export const ads_native = {
    // Native ad networks - all disabled by default
    // MGID
    // Feature: Native widgets for viral content
    // Requirement: Moderate traffic needed
    mgid: { widgetId: '', enabled: false },

    // Taboola
    // Feature: The biggest native network
    // Requirement: High traffic (500k+ users) often required
    taboola: { publisherId: '', enabled: false },  // Requires traffic

    // Outbrain
    // Feature: High quality placements
    // Requirement: Strict content quality
    outbrain: { publisherId: '', enabled: false },  // Strict quality control

    // AdNow
    // Feature: Widget customization
    // Requirement: Lower barrier to entry
    adnow: { widgetId: '', enabled: false }
};

export const ads_native_priority = ['mgid', 'taboola', 'outbrain', 'adnow'];
