/**
 * Part 1: Monetization - Fiat Donations
 * ENABLED - Highly recommended as first monetization step.
 * @module config/monetization/donation_fiat
 */

export const donation_fiat = {
    // ============================================================================
    // KO-FI - The Best for Small Creators (2025 Favorite)
    // ============================================================================
    // Description:
    // The most creator-friendly tipping platform.
    //
    // Key Features:
    // - **0% Platform Fee on Tips**: You keep 100% of one-time donations.
    // - Instant Payouts: Money goes directly to PayPal/Stripe immediately.
    // - No Minimum Payout: Access your money from $1.
    // - Digital Shop (5% fee on free tier, 0% on Gold).
    //
    // Fees (2025):
    // - One-time Tips: 0%.
    // - Memberships/Shop: 5% (Free plan).
    // - Processor Fee: Standard Stripe/PayPal (~2.9% + $0.30).
    //
    // Best For:
    // - MAXIMUM revenue from tips. Best alternative to BuyMeACoffee.
    //
    kofi: { username: '', enabled: true },

    // ============================================================================
    // BUY ME A COFFEE - The Polish & Simplicity Leader
    // ============================================================================
    // Description:
    // Elegant, simple UI that users love.
    //
    // Key Features:
    // - Single-page checkout.
    // - "Extras" for selling simple digital products.
    //
    // Fees (2025):
    // - **Flat 5% Fee** on everything (Donations, Memberships, Extras).
    // - Processor Fee: Standard Stripe/PayPal.
    //
    // Payout Details:
    // - Minimum Payout: $10.
    // - Frequency: Weekly (or instant review for first $20).
    //
    // Best For:
    // - Users who want the highest "support conversion" due to trusted branding.
    //
    buymeacoffee: { username: 'chirag127', enabled: true },

    // ============================================================================
    // GITHUB SPONSORS - Best for Open Source
    // ============================================================================
    // Description:
    // Native GitHub integration.
    //
    // Fees:
    // - **0% Platform Fee**.
    // - **0% Processing Fee** (GitHub pays it!).
    // - 100% of the support reaches you.
    //
    github_sponsors: { username: 'chirag127', enabled: true },

    // ============================================================================
    // LIBERAPAY - Non-Profit Model
    // ============================================================================
    // Description:
    // Peer-to-peer recurrent funding. No platform fees.
    //
    liberapay: { username: '', enabled: false },

    // ============================================================================
    // PAYPAL - Direct Fallback
    // ============================================================================
    paypal: { buttonId: '', enabled: false }
};

export const donation_fiat_priority = ['kofi', 'buymeacoffee', 'github_sponsors'];
