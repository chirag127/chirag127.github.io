/**
 * Part 1: Monetization - URL Shorteners
 * @module config/monetization/url_shortener
 */

export const url_shortener = {
    // Ouo.io
    // Feature: Clean interface, reliable payouts
    // Rates: Variable CPM based on country
    ouoio: { apiToken: '', enabled: true },

    // ShrinkEarn
    // Feature: High CPM rates claiming
    // Rates: Competitive payout rates
    shrinkEarn: { apiKey: '', enabled: true },

    // Adf.ly (Legacy)
    // Feature: One of the oldest, stable
    // Rates: Lower compared to new entrants
    adfLy: { userId: '', enabled: true },

    // Shorte.st
    // Feature: Smart mining script integration option
    // Rates: Global coverage
    shortest: { apiToken: '', enabled: true },

    // GPLinks
    // Feature: Modern UI, multiple payout options
    // Rates: High CPM for Tier 1 countries
    gplinks: { apiKey: '', enabled: true }
};

export const url_shortener_priority = ['ouoio', 'shrinkEarn', 'adfLy', 'shortest', 'gplinks'];
