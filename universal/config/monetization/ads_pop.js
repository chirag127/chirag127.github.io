/**
 * Part 1: Monetization - Pop-Under Networks
 * ALL DISABLED - These are aggressive, hurt SEO, and may trigger AdSense ban
 * @module config/monetization/ads_pop
 */

export const ads_pop = {
    // ⚠️ ALL DISABLED - Pop-unders destroy user experience and SEO
    // PopAds
    // Feature: The biggest pop-under network
    popads: { publisherId: '', enabled: false },

    // PopCash
    // Feature: Fast approval, reliable
    popcash: { publisherId: '', enabled: false },

    // Clickadu
    // Feature: Multi-format ad network
    clickadu: { siteId: '', enabled: false },

    // AdMaven
    // Feature: Aggressive monetization
    admaven: { publisherId: '', enabled: false },

    // ExoClick
    // Feature: Adult/Lifestyle friendly
    exoclick: { publisherId: '', zoneId: '', enabled: false },

    // JuicyAds
    // Feature: "Sexy" mainstream allowed
    juicyads: { siteId: '', enabled: false },

    // TrafficForce
    // Feature: High volume traffic
    trafficforce: { publisherId: '', enabled: false }
};

export const ads_pop_limits = { maxPopsPerDay: 0, daysBetweenPops: 7 };  // Effectively disabled
export const ads_pop_priority = ['popads', 'popcash', 'clickadu', 'admaven', 'exoclick', 'juicyads', 'trafficforce'];
