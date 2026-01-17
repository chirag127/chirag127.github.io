/**
 * Part 1: Monetization - Affiliates
 * @module config/monetization/affiliates
 */

export const affiliates = {
    amazon: { trackingId: '', marketplace: 'US', enabled: true },
    clickbank: { nickname: '', enabled: true },
    shareasale: { affiliateId: '', enabled: true },
    cjAffiliate: { websiteId: '', enabled: true },
    rakuten: { publisherId: '', enabled: false },
    awin: { publisherId: '', enabled: false }
};

export const affiliates_priority = ['amazon', 'clickbank', 'shareasale', 'cjAffiliate'];
