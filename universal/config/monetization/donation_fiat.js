/**
 * Part 1: Monetization - Fiat Donations
 * ENABLED - Non-intrusive, builds community
 * @module config/monetization/donation_fiat
 */

export const donation_fiat = {
    // ALL ENABLED - Non-intrusive, shows you care about community
    // BuyMeACoffee
    // Feature: Friendly, social donation widget
    // Fees: 5% transaction fee (Free Standard)
    buymeacoffee: { username: 'chirag127', enabled: true },  // YOUR USERNAME

    // Ko-fi
    // Feature: 0% fee on donations (Direct to PayPal/Stripe)
    // Free Limit: Free Gold features with Monthly Subs
    kofi: { username: '', enabled: true },

    // PayPal
    // Feature: The global standard
    // Fees: Standard transaction fees applied
    paypal: { buttonId: '', enabled: false },

    // Liberapay
    // Feature: Recurrent donations, Open Source funded
    // Fees: 0% platform fee coverage model
    liberapay: { username: '', enabled: false },

    // GitHub Sponsors
    // Feature: Zero fees for individuals!
    // Free Limit: Best for dev projects
    github_sponsors: { username: 'chirag127', enabled: true }  // GitHub integration
};

export const donation_fiat_priority = ['buymeacoffee', 'kofi', 'github_sponsors'];
