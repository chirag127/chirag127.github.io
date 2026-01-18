/**
 * Part 1: Monetization - Affiliates
 * @module config/monetization/affiliates
 */

export const affiliates = {
    // Amazon Associates
    // Feature: The world's largest marketplace
    // Rate: 1% - 10% commissions
    amazon: { trackingId: '', marketplace: 'US', enabled: true },

    // Clickbank
    // Feature: Digital products focused
    // Rate: High commissions (up to 75%)
    clickbank: { nickname: '', enabled: true },

    // ShareASale
    // Feature: Diverse merchant network
    shareasale: { affiliateId: '', enabled: true },

    // CJ Affiliate (Commission Junction)
    // Feature: Premium brand partnerships
    cjAffiliate: { websiteId: '', enabled: true },

    // Rakuten Advertising
    // Feature: Global brands
    rakuten: { publisherId: '', enabled: false },

    // Awin
    // Feature: European market leader
    // Cost: $5 signup fee (refundable)
    awin: { publisherId: '', enabled: false }
};

export const affiliates_priority = ['amazon', 'clickbank', 'shareasale', 'cjAffiliate', 'rakuten', 'awin'];
