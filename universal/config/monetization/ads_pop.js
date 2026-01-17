/**
 * Part 1: Monetization - Pop-Under Networks
 * ALL DISABLED - These are aggressive, hurt SEO, and may trigger AdSense ban
 * @module config/monetization/ads_pop
 */

export const ads_pop = {
    // ⚠️ ALL DISABLED - Pop-unders destroy user experience and SEO
    popads: { publisherId: '', enabled: false },
    popcash: { publisherId: '', enabled: false },
    clickadu: { siteId: '', enabled: false },
    admaven: { publisherId: '', enabled: false },
    exoclick: { publisherId: '', zoneId: '', enabled: false },
    juicyads: { siteId: '', enabled: false },
    trafficforce: { publisherId: '', enabled: false }
};

export const ads_pop_limits = { maxPopsPerDay: 0, daysBetweenPops: 7 };  // Effectively disabled
export const ads_pop_priority = [];  // Empty - nothing enabled
