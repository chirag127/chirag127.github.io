/**
 * Part 1: Monetization - Smart Links
 * ⛔ ALL DISABLED - These hijack ALL clicks and redirect through ad networks
 * @module config/monetization/smart_links
 */

export const smart_links = {
    // ⛔ DANGEROUS - These redirect ALL clicks
    losPollos: { publisherId: '', enabled: false, _warning: 'HIJACKS ALL CLICKS' },
    smartyAds: { publisherId: '', enabled: false, _warning: 'HIJACKS ALL CLICKS' }
};

// NEVER enable these - they hijack legitimate navigation
export const smart_links_priority = [];
