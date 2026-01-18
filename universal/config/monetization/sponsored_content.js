/**
 * Part 1: Monetization - Sponsored Content
 * @module config/monetization/sponsored_content
 */

export const sponsored_content = {
    // ============================================================================
    // PUBLISUITES - Accessible Sponsored Posts
    // ============================================================================
    // Description:
    // A marketplace connecting bloggers with advertisers.
    // Sell sponsored posts, press releases, or social media mentions.
    //
    // Key Features:
    // - You set your own prices.
    // - Accepts blogs with lower traffic as long as content is good.
    // - "Managed Service" (Advertisers buy directly).
    //
    // Requirements:
    // - Original content (No duplicate/spam).
    // - Active blog (updated frequently).
    // - 500+ words per sponsored post required.
    //
    // Payout Details:
    // - Minimum Payout: $5 / €5 (PayPal).
    // - Frequency: On Request (Processed within 10 days).
    //
    // Best For:
    // - Small to Medium bloggers wanting extra income.
    //
    publisuites: { siteId: '', enabled: false },

    // ============================================================================
    // FLYOUT.IO - Premium Blog Monetization
    // ============================================================================
    // Description:
    // Automated sponsored post platform.
    //
    // Key Features:
    // - Automatic placement (sometimes).
    // - Higher payouts per post.
    //
    // Requirements:
    // - **HIGH TRAFFIC BARRIER**: Requires 10,000+ monthly organic visitors.
    // - Must be WordPress blog (No Blogger/Wix).
    // - Verified Google Analytics stats.
    // - Detailed "About", "Contact", "Privacy" pages mandatory.
    //
    // Payout Details:
    // - Instant deposit to Flyout account.
    // - Monthly withdrawals (Net-30ish).
    //
    // Best For:
    // - Established blogs with significant SEO traffic.
    //
    flyout: { publisherId: '', enabled: false }
};

export const sponsored_content_priority = ['publisuites', 'flyout'];
