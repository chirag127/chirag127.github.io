/**
 * Part 1: Monetization - Native Ads
 * Ads that look like content recommendations
 * @module config/monetization/ads_native
 */

export const ads_native = {
    // Native ad networks - all disabled by default
    mgid: { widgetId: '', enabled: false },
    taboola: { publisherId: '', enabled: false },  // Requires traffic
    outbrain: { publisherId: '', enabled: false },  // Strict quality control
    adnow: { widgetId: '', enabled: false }
};

export const ads_native_priority = ['mgid', 'taboola', 'outbrain', 'adnow'];
