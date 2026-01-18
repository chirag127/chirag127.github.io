/**
 * Part 1: Monetization - Offerwalls & Content Locking
 * @module config/monetization/offerwalls
 */

export const offerwalls = {
    // ============================================================================
    // CPALEAD - User Example (Industry Leader)
    // ============================================================================
    // Description:
    // A premier CPA (Cost Per Action) network specializing in content locking.
    //
    // Key Features:
    // - Content Locker: Lock premium content behind an offerwall.
    // - Mobile App Installs, Surveys, and Email Submits.
    // - Daily Payouts available.
    //
    // Requirements:
    // - No traffic minimum.
    // - Instant approval for most countries.
    //
    // Payout Details:
    // - Minimum Payout: $1 (Very low).
    // - Methods: PayPal, Payoneer, Wire, Bitcoin.
    //
    cpalead: {
        publisherId: '264708',
        directLink: 'https://cpalead.com/get-offers.php?id=264708',
        enabled: true
    },

    // ============================================================================
    // OGADS - Mobile Tier 1 King
    // ============================================================================
    // Description:
    // The most trusted network for Mobile Content Locking.
    //
    // Key Features:
    // - High-converting landing pages.
    // - Premium mobile app offers.
    // - Excellent support and dedicated managers.
    //
    // Payout Details:
    // - Minimum Payout: $50.
    // - Frequency: Weekly / Net-7.
    // - Reliability: 5/5 (Consistently pays on time).
    //
    ogads: { publisherId: '', enabled: false },

    // ============================================================================
    // ADWORKMEDIA - Multi-Tool Platform
    // ============================================================================
    // Description:
    // Content lockers, offerwalls, and smart links.
    //
    // ⚠️ WARNING (2025):
    // - Increasing reports of payment delays and "scam" warnings in Recent Reviews.
    // - Use with caution compared to OGAds or CPALead.
    //
    // Payout Details:
    // - Minimum Payout: $35.
    //
    adworkmedia: { publisherId: '', enabled: false }
};

export const offerwalls_priority = ['cpalead', 'ogads', 'adworkmedia'];
