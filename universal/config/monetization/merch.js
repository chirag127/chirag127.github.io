/**
 * Part 1: Monetization - Merch / Print on Demand
 * @module config/monetization/merch
 */

export const merch = {
    // Spring (Teespring)
    // Feature: Integrated with YouTube/Twitch
    // Model: Print on Demand (Base cost deducted)
    spring: { storeUrl: '', enabled: false },  // Teespring embed

    // Redbubble
    // Feature: Massive independent marketplace
    // Model: Artist margin on base price
    redbubble: { storeUrl: '', enabled: false },

    // Spreadshop
    // Feature: Customizable storefront embedded
    // Model: Profit margin control
    spreadshop: { shopId: '', enabled: false }
};

export const merch_priority = ['spring', 'redbubble'];
