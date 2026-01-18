/**
 * Part 1: Monetization - Push Notification Ads
 * ALL DISABLED - These can be intrusive and hurt user trust
 * @module config/monetization/ads_push
 */

export const ads_push = {
    // ⚠️ ALL DISABLED - Push ads are intrusive
    // EvaDav
    // Feature: Push notifications & Natives
    evadav: { siteId: '', enabled: false },

    // RichAds
    // Feature: Performance marketing network
    richads: { publisherId: '', enabled: false },

    // Push.House
    // Feature: High volume push traffic
    pushHouse: { publisherId: '', enabled: false },

    // TacoLoco
    // Feature: Monetize push subscriptions
    tacoloco: { publisherId: '', enabled: false },

    // Zalvis
    // Feature: Direct advertisers
    zalvis: { publisherId: '', enabled: false },

    // Partners.House
    // Feature: RevShare from push subscriptions
    partnersHouse: { publisherId: '', enabled: false }
};

export const ads_push_priority = ['evadav', 'richads', 'pushHouse', 'tacoloco', 'zalvis', 'partnersHouse'];
