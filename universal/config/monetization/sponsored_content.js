/**
 * Part 1: Monetization - Sponsored Content
 * @module config/monetization/sponsored_content
 */

export const sponsored_content = {
    // ============================================================================
    // PUBLISUITES - Quality Focused Marketplace
    // ============================================================================
    // Description:
    // Connects bloggers with advertisers for sponsored posts and press releases.
    //
    // Requirements:
    // - **Quality Over Quantity**: No strict traffic minimum, but content must be original and high quality.
    // - Must have an active blog section.
    // - No link farms.
    //
    // Payout Details:
    // - Minimum Payout: $5.
    // - Frequency: On demand (10-day process).
    //
    publisuites: { siteId: '', enabled: false },

    // ============================================================================
    // FLYOUT.IO - High Traffic Automated Platform
    // ============================================================================
    // Description:
    // High-end marketplace for established blogs.
    //
    // Requirements (Strict):
    // - **10,000+ Monthly Visitors** (Verified via GA).
    // - 100+ High-quality original articles.
    // - WordPress blogs preferred.
    //
    flyout: { publisherId: '', enabled: false }
};

export const sponsored_content_priority = ['publisuites', 'flyout'];
