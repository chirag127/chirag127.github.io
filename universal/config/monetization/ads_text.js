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
    // Scans your page content and hyperlinks specific keywords to relevant ads.
    // Very effective for text-heavy blogs.
    //
    // Key Features:
    // - InText: Double underline links.
    // - InTag: Tag cloud style ads.
    // - InFold: Footer sticky ads.
    //
    // Requirements:
    // - No strict minimum traffic (Content Quality is key).
    // - Must have substantial text content.
    //
    // Payout Details:
    // - Minimum Payout: $50.
    // - Frequency: Net-45.
    // - Methods: PayPal, Payoneer, Wire.
    //
    // Best For:
    // - Blogs with long-form articles.
    //
    infolinks: { publisherId: '', websiteId: '', enabled: false },

    // ============================================================================
    // MEDIA.NET - The Yahoo/Bing Alternative
    // ============================================================================
    // Description:
    // The biggest competitor to AdSense for contextual ads.
    // Powered by the Bing & Yahoo network.
    //
    // Key Features:
    // - Contextual Specialists: Ads are highly relevant to text.
    // - Premium Advertisers: Access to large search budgets.
    //
    // Requirements:
    // - **HIGH TRAFFIC**: Generally looks for 10k+ monthly visitors.
    // - Traffic **MUST** be primarily from US, UK, Canada (Tier 1).
    // - English content only.
    //
    // Payout Details:
    // - Minimum Payout: $100.
    // - Frequency: Net-30.
    // - Methods: PayPal, Wire Transfer.
    //
    // Best For:
    // - Established US-focused blogs in Finance, Tech, or Lifestyle.
    //
    mediaNet: { siteId: '', enabled: false }
};

export const ads_text_priority = ['infolinks', 'mediaNet'];
