/**
 * Part 1: Monetization - Push Notification Ads
 * ALL DISABLED - These can be intrusive and hurt user trust
 * @module config/monetization/ads_push
 */

export const ads_push = {
    // ============================================================================
    // WEB PUSH ADS
    // ============================================================================
    // Description:
    // Asks user to subscribe to notifications, then sends ads later.
    //
    // Best "Generous Free Tier" Provider:
    // - Adsterra (See ads_display.js).
    //
    // Specialized Push Networks (Use only if Adsterra is insufficient):
    //
    evadav: { siteId: '', enabled: false },
    richads: { publisherId: '', enabled: false },
    pushHouse: { publisherId: '', enabled: false }
};

export const ads_push_priority = [];
