/**
 * Part 1: Monetization - Text & Contextual Ads
 * ⚠️ LINK HIJACKERS DISABLED - VigLink/Skimlinks modify your links
 * @module config/monetization/ads_text
 */

export const ads_text = {
    // SAFE - Only display contextual ads, don't modify links
    // Infolinks
    // Feature: In-Fold, In-Text ads
    // Requirement: 1000 pageviews/month
    infolinks: { publisherId: '', websiteId: '', enabled: false },  // Enable when needed

    // Media.net
    // Feature: Yahoo/Bing contextual ads (AdSense alternative)
    // Requirement: High traffic from US/UK/CA
    mediaNet: { siteId: '', enabled: false },  // Yahoo/Bing network

    // ⛔ LINK HIJACKERS - PERMANENTLY DISABLED
    // These services automatically convert ALL your links to affiliate links
    // This includes navigation links, social links, and legitimate non-affiliate content
    viglink: { key: '', enabled: false, _warning: 'LINK HIJACKER - Modifies all links' },
    skimlinks: { publisherId: '', enabled: false, _warning: 'LINK HIJACKER - Modifies all links' }
};

export const ads_text_priority = ['infolinks', 'mediaNet'];
// Never add viglink/skimlinks to priority - they hijack links
