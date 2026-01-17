/**
 * Part 1: Monetization - Fiat Donations
 * ENABLED - Non-intrusive, builds community
 * @module config/monetization/donation_fiat
 */

export const donation_fiat = {
    // ALL ENABLED - Non-intrusive, shows you care about community
    buymeacoffee: { username: 'chirag127', enabled: true },  // YOUR USERNAME
    kofi: { username: '', enabled: true },
    paypal: { buttonId: '', enabled: false },
    liberapay: { username: '', enabled: false },
    github_sponsors: { username: 'chirag127', enabled: true }  // GitHub integration
};

export const donation_fiat_priority = ['buymeacoffee', 'kofi', 'github_sponsors'];
