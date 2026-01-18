/**
 * Part 1: Monetization - Text & Contextual Ads
 * ⚠️ LINK HIJACKERS DISABLED - VigLink/Skimlinks modify your links
 * @module config/monetization/ads_text
 */

export const ads_text = {
    // ============================================================================
    // INFOLINKS - Contextual Text Ads
    // ============================================================================
    // Description:
    // Turn keywords in your text into ad links.
    //
    // Requirements:
    // - ~1000 Pageviews/month normally required.
    // - Content must be text-heavy.
    //
    // Payout:
    // - Min $50 (PayPal).
    //
    infolinks: { publisherId: '', websiteId: '', enabled: false },

    // ============================================================================
    // MEDIA.NET - The Yahoo/Bing Alternative
    // ============================================================================
    // Description:
    // High quality contextual ads.
    //
    // Requirements:
    // - High Traffic (Major portion from US/UK/Canada).
    // - English content only.
    //
    mediaNet: { siteId: '', enabled: false }

    // Removed: VigLink / Skimlinks (Link Hijackers) per user instruction to prioritize UX.
};

export const ads_text_priority = ['infolinks', 'mediaNet'];
