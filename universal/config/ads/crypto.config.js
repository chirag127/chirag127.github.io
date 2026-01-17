/**
 * Crypto Advertising Configuration
 * Bitcoin/Ethereum/Crypto-specific ad networks
 * Best for tech-savvy audiences. Pays in cryptocurrency.
 *
 * @module config/ads/crypto
 */

export const cryptoAdsConfig = {

    // =========================================================================
    // COINZILLA - Premium crypto/finance ads
    // =========================================================================
    // HOW TO GET: https://coinzilla.com/
    // 1. Sign up at https://publishers.coinzilla.com/
    // 2. Submit your crypto/finance related website
    // 3. Wait for manual approval (usually 24-48 hours)
    // 4. Get zone ID from dashboard
    // PAYOUT: $50 minimum via Bitcoin/Bank
    // TIP: Your content should be crypto/finance related for approval
    coinzilla: {
        enabled: true,
        zone: '04f0bcb8c5793e809c1b6d64b32b5772',  // Your existing zone
        format: 'banner'  // banner, native, or popup
    },

    // =========================================================================
    // COINTRAFFIC - Top tier crypto ads
    // =========================================================================
    // HOW TO GET: https://cointraffic.io/
    // 1. Apply at https://cointraffic.io/en/advertiser/
    // 2. They review your site manually
    // 3. Requires decent crypto traffic
    // PAYOUT: Monthly, NET30
    cointraffic: {
        enabled: false,
        publisherId: '',
        format: 'banner'
    },

    // =========================================================================
    // BITMEDIA - Bitcoin advertising network
    // =========================================================================
    // HOW TO GET: https://bitmedia.io/
    // 1. Sign up at https://bitmedia.io/publishers
    // 2. Add website and verify ownership
    // 3. Wait for approval
    // 4. Create ad zones
    // PAYOUT: 0.001 BTC minimum
    bitmedia: {
        enabled: false,
        publisherId: '',
        zoneId: ''
    },

    // =========================================================================
    // COINAD - Simple text/banner crypto ads
    // =========================================================================
    // HOW TO GET: https://coinad.com/
    // 1. Quick signup
    // 2. Add your Bitcoin address
    // 3. Get embed code
    // PAYOUT: Direct to Bitcoin wallet
    coinad: {
        enabled: false,
        publisherId: ''
    },

    // =========================================================================
    // ADSHARES - Blockchain-based ad network
    // =========================================================================
    // HOW TO GET: https://adshares.net/
    // 1. Create account at https://app.adshares.net/
    // 2. Register as publisher
    // 3. Add your website
    // PAYOUT: ADS tokens (can convert to other crypto)
    adshares: {
        enabled: false,
        publisherId: ''
    },

    // =========================================================================
    // DOT AUDIENCES - Web3 focused
    // =========================================================================
    // HOW TO GET: https://dotaudiences.com/
    // 1. Apply for publisher program
    // 2. Must have Web3/NFT related content
    // PAYOUT: Various crypto options
    dotAudiences: {
        enabled: false,
        publisherId: ''
    },

    // =========================================================================
    // AMBIRE ADEX - Decentralized ad exchange
    // =========================================================================
    // HOW TO GET: https://www.adex.network/
    // 1. Sign up at AdEx Platform
    // 2. Register as publisher
    // 3. Connect wallet for payments
    // PAYOUT: ADX tokens or DAI
    adex: {
        enabled: false,
        publisherAddr: ''  // Ethereum address
    }
};

// Fallback order for crypto ads
export const cryptoAdsPriority = [
    'coinzilla',     // Premium, already enabled
    'bitmedia',      // Good rates
    'cointraffic',   // High quality
    'coinad',        // Simple
    'adshares',      // Blockchain native
    'dotAudiences',
    'adex'
];
