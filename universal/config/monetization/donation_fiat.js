/**
 * Part 1: Monetization - Fiat Donations
 * ENABLED - Non-intrusive, builds community
 * @module config/monetization/donation_fiat
 */

export const donation_fiat = {
    // ============================================================================
    // BUY ME A COFFEE - The Creator Favorite
    // ============================================================================
    // Description:
    // A friendly, simple way for fans to support you.
    // Replaces the "Donate" button with something more personal.
    //
    // Key Features:
    // - One-off donations ("coffees").
    // - Memberships (recurring monthly/yearly support).
    // - "Extras" (Sell digital downloads or services).
    // - No account needed for supporters (Guest checkout).
    // - Instant payout options.
    //
    // Fees & Limits:
    // - Platform Fee: 5% flat fee on all income.
    // - Processor Fee: Standard Stripe/PayPal fees (~2.9% + $0.30).
    // - No monthly fee for you.
    //
    // Best For:
    // - Creators, artists, developers, writers.
    // - Casual support without feeling like "begging".
    //
    buymeacoffee: { username: 'chirag127', enabled: true },

    // ============================================================================
    // KO-FI - 0% Fee Donations
    // ============================================================================
    // Description:
    // Similar to BuyMeACoffee but focuses on keeping more of your money.
    // "Gold" plan available but the free version is extremely powerful.
    //
    // Key Features:
    // - 0% Platform Fee on Donations (You keep 100% of the tip!).
    // - Ko-fi Shop (Sell physical/digital items) - 5% fee on free plan.
    // - Commissions (Take custom orders) - 5% fee on free plan.
    // - Memberships (Recurring support) - 5% fee on free plan.
    // - Gallery to showcase work.
    //
    // Fees & Limits:
    // - Donations: 0% Platform Fee (Free Plan).
    // - Shop/Commissions/Memberships: 5% Platform Fee (Free Plan) or 0% (Gold Plan @ $6/mo).
    // - Processor Fee: Standard PayPal/Stripe fees apply.
    //
    // Best For:
    // - Artists and creators wanting maximum donation revenue.
    //
    kofi: { username: '', enabled: true },

    // ============================================================================
    // GITHUB SPONSORS - For Developers
    // ============================================================================
    // Description:
    // The native way to support developers on GitHub.
    //
    // Key Features:
    // - ZERO FEES: GitHub covers all processing fees for individual accounts!
    // - Displays a "Sponsor" button on your repositories.
    // - Tiers and rewards system.
    //
    // Fees & Limits:
    // - 0% Platform Fee.
    // - 0% Processor Fee (GitHub pays this!).
    // - 100% of the money goes to you (Best deal in the industry).
    // - Requires application and approval.
    //
    // Best For:
    // - Open source developers and maintainers.
    //
    github_sponsors: { username: 'chirag127', enabled: true },

    // ============================================================================
    // PAYPAL - The Standard (Fallback)
    // ============================================================================
    // Description:
    // Direct link to pay via PayPal.
    //
    // Fees:
    // - Standard commercial transaction fees (~2.9% + $0.30 for domestic).
    // - International fees are higher.
    //
    paypal: { buttonId: '', enabled: false },

    // ============================================================================
    // LIBERAPAY - Recurrent Open Source Funding
    // ============================================================================
    // Description:
    // A non-profit platform for recurrent donations.
    //
    // Fees:
    // - 0% Platform Fee (Funded by donations to Liberapay itself).
    // - You pay processor fees.
    //
    liberapay: { username: '', enabled: false }
};

export const donation_fiat_priority = ['buymeacoffee', 'kofi', 'github_sponsors'];
