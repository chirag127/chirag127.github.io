/**
 * Part 1: Monetization - Text & Contextual Ads
 * ⚠️ LINK HIJACKERS DISABLED - VigLink/Skimlinks modify your links
 * @module config/monetization/ads_text
 */

export const ads_text = {
    // SAFE - Only display contextual ads, don't modify links
    infolinks: { publisherId: '', websiteId: '', enabled: false },  // Enable when needed
    mediaNet: { siteId: '', enabled: false },  // Yahoo/Bing network

    // ⛔ LINK HIJACKERS - PERMANENTLY DISABLED
    // These services automatically convert ALL your links to affiliate links
    // This includes navigation links, social links, and legitimate non-affiliate content
    viglink: { key: '', enabled: false, _warning: 'LINK HIJACKER - Modifies all links' },
    skimlinks: { publisherId: '', enabled: false, _warning: 'LINK HIJACKER - Modifies all links' }
};

export const ads_text_priority = ['infolinks', 'mediaNet'];
// Never add viglink/skimlinks to priority - they hijack links
