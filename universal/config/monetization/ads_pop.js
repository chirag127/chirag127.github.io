/**
 * Part 1: Monetization - Pop-Under Networks (disabled by default - AdSense risk)
 * @module config/monetization/ads_pop
 */

export const ads_pop = {
    popads: { publisherId: '', enabled: false },
    popcash: { publisherId: '', enabled: false },
    clickadu: { siteId: '', enabled: false },
    admaven: { publisherId: '', enabled: false },
    exoclick: { publisherId: '', zoneId: '', enabled: false },
    juicyads: { siteId: '', enabled: false },
    trafficforce: { publisherId: '', enabled: false }
};

export const ads_pop_limits = { maxPopsPerDay: 1, daysBetweenPops: 1 };
export const ads_pop_priority = ['popads', 'popcash', 'clickadu', 'admaven'];
