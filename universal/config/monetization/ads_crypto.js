/**
 * Part 1: Monetization - Crypto Advertising
 * Safe crypto ad networks - no link hijacking
 * @module config/monetization/ads_crypto
 */

export const ads_crypto = {
    // SAFE - These are banner ads, not link hijackers
    // Coinzilla
    // Feature: Premium crypto native network
    // Format: Banners, Native
    coinzilla: { zoneId: '04f0bcb8c5793e809c1b6d64b32b5772', format: 'banner', enabled: false },  // YOUR ID - Enable when needed

    // A-ADS
    // Feature: Anonymous, no KYC, daily payouts
    // Format: Clean banners, text ads
    aads: { unitId: '', enabled: false },  // A-ADS - Anonymous, no approval needed

    // Cointraffic
    // Feature: Top tier crypto news sites
    // Format: High impact formats
    cointraffic: { publisherId: '', enabled: false },

    // Bitmedia
    // Feature: Deep targeting for crypto audiences
    // Format: Display & Rich Media
    bitmedia: { zoneId: '', enabled: false },

    // CoinAd
    // Feature: Simple bidding system
    coinad: { publisherId: '', enabled: false },

    // AdShares
    // Feature: Decentralized ad network
    adshares: { publisherId: '', enabled: false }
};

export const ads_crypto_priority = ['coinzilla', 'aads', 'cointraffic', 'bitmedia', 'coinad', 'adshares'];
