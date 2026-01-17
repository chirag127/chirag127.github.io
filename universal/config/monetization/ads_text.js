/**
 * Part 1: Monetization - Text & Contextual Ads
 * @module config/monetization/ads_text
 */

export const ads_text = {
    infolinks: { publisherId: '', websiteId: '', enabled: true },
    mediaNet: { siteId: '', enabled: true },
    viglink: { key: '', enabled: false },  // DISABLED - Link hijacker
    skimlinks: { publisherId: '', enabled: false }  // DISABLED - Link hijacker
};

export const ads_text_priority = ['infolinks', 'mediaNet'];
