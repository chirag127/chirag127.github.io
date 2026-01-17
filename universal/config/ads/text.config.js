/**
 * Text & Contextual Advertising Configuration
 * In-text ads, highlighted keywords, contextual relevance
 *
 * WARNING: VigLink and Skimlinks are DISABLED by default
 * These auto-convert your links to affiliate links (link hijacking)
 * Only enable if you're okay with your links being modified.
 *
 * @module config/ads/text
 */

export const textAdsConfig = {

    // =========================================================================
    // INFOLINKS - In-text bubbles (SAFE)
    // =========================================================================
    // HOW TO GET: https://www.infolinks.com/
    // 1. Sign up at https://www.infolinks.com/
    // 2. Add your website
    // 3. Wait for approval
    // 4. Get publisher ID and website ID
    // PAYOUT: $50 minimum
    // TIP: Safe, non-intrusive in-text ads
    infolinks: {
        enabled: true,
        publisherId: '',
        websiteId: '',
        adTypes: {
            inText: true,    // Keyword highlights
            inFold: false,   // Below fold
            inTag: true,     // Tag cloud
            inFrame: false   // Sticky bar
        }
    },

    // =========================================================================
    // MEDIA.NET - Yahoo/Bing contextual ads (Premium)
    // =========================================================================
    // HOW TO GET: https://www.media.net/
    // 1. Apply at https://www.media.net/signup
    // 2. Requires quality English content
    // 3. Manual review process
    // PAYOUT: $100 minimum
    // TIP: High quality, competitive to AdSense
    mediaNet: {
        enabled: false,
        siteId: '',
        pageId: ''
    },

    // =========================================================================
    // VIGLINK (SOVRN) - Auto affiliate links
    // =========================================================================
    // WARNING: DISABLED - This hijacks your existing links!
    // It automatically converts product mentions to affiliate links.
    // Only enable if you want this behavior.
    // HOW TO GET: https://www.sovrn.com/publishers/commerce/
    // PAYOUT: $25 minimum
    viglink: {
        enabled: false,  // DISABLED - Link hijacking
        publisherId: ''
    },

    // =========================================================================
    // SKIMLINKS - Auto affiliate conversion
    // =========================================================================
    // WARNING: DISABLED - This hijacks your existing links!
    // Similar to VigLink, auto-converts links to affiliate.
    // HOW TO GET: https://skimlinks.com/
    // PAYOUT: $65 minimum
    skimlinks: {
        enabled: false,  // DISABLED - Link hijacking
        publisherId: ''
    }
};

// Safe text ad networks (don't modify links)
export const textAdsPriority = [
    'infolinks',  // Safe in-text
    'mediaNet'    // Premium contextual
];

// Link hijackers - only use if intentional
export const affiliateLinkServices = [
    'viglink',
    'skimlinks'
];
