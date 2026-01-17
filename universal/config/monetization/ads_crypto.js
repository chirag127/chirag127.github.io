/**
 * Part 1: Monetization - Crypto Advertising
 * @module config/monetization/ads_crypto
 */

export const ads_crypto = {
    coinzilla: { zoneId: '04f0bcb8c5793e809c1b6d64b32b5772', format: 'banner', enabled: true },  // YOUR ID
    cointraffic: { publisherId: '', enabled: true },
    bitmedia: { zoneId: '', enabled: true },
    coinad: { publisherId: '', enabled: true },
    adshares: { publisherId: '', enabled: true },
    dragonX: { publisherId: '', enabled: false },
    dotAudiences: { publisherId: '', enabled: false },
    ambireAdex: { publisherId: '', enabled: false }
};

export const ads_crypto_priority = ['coinzilla', 'cointraffic', 'bitmedia', 'coinad', 'adshares'];
