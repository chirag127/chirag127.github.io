/**
 * Part 1: Monetization - Pop-Under Networks
 * ALL DISABLED - These are aggressive, hurt SEO, and may trigger AdSense ban
 * @module config/monetization/ads_pop
 */

export const ads_pop = {
    // ============================================================================
    // POP-UNDER ADS - USE WITH CAUTION
    // ============================================================================
    // Description:
    // Ads that open in a new window behind the main browser window.
    //
    // WARNING:
    // - High revenue potential but VERY BAD for User Experience.
    // - Can negatively impact SEO (Google "Intrusive Interstitials" penalty).
    // - Chrome/Firefox often block these by default.
    //
    // Best "Generous Free Tier" Provider:
    // - Adsterra (See ads_display.js).
    //   Adsterra has no minimum traffic, pays well, and is reliable.
    //
    // Configs below are for specific networks if Adsterra is not enough.
    //
    popads: { publisherId: '', enabled: false, _warning: 'AGGRESSIVE FORMAT' },
    popcash: { publisherId: '', enabled: false, _warning: 'AGGRESSIVE FORMAT' },
    clickadu: { siteId: '', enabled: false, _warning: 'AGGRESSIVE FORMAT' }
};

export const ads_pop_priority = [];

export const ads_pop_limits = { maxPopsPerDay: 0, daysBetweenPops: 7 };  // Effectively disabled
