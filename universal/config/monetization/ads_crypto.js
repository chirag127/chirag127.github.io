/**
 * Part 1: Monetization - Crypto Advertising
 * Safe crypto ad networks - no link hijacking
 * @module config/monetization/ads_crypto
 */

export const ads_crypto = {
    // SAFE - These are banner ads, not link hijackers
    coinzilla: { zoneId: '04f0bcb8c5793e809c1b6d64b32b5772', format: 'banner', enabled: false },  // YOUR ID - Enable when needed
    aads: { unitId: '', enabled: false },  // A-ADS - Anonymous, no approval needed
    cointraffic: { publisherId: '', enabled: false },
    bitmedia: { zoneId: '', enabled: false },
    coinad: { publisherId: '', enabled: false },
    adshares: { publisherId: '', enabled: false }
};

export const ads_crypto_priority = ['coinzilla', 'aads', 'cointraffic', 'bitmedia'];
