/**
 * Donation & Tipping Configuration
 * Direct payments from users (Fiat & Crypto)
 *
 * These are NOT ads - users voluntarily support you
 *
 * @module config/ads/donations
 */

export const donationsConfig = {

    // =========================================================================
    // FIAT DONATIONS
    // =========================================================================

    // -------------------------------------------------------------------------
    // BUY ME A COFFEE - Simple donation widget
    // -------------------------------------------------------------------------
    // HOW TO GET: https://www.buymeacoffee.com/
    // 1. Sign up at https://www.buymeacoffee.com/
    // 2. Create your page
    // 3. Get your username for widget
    // PAYOUT: Instant to PayPal/Stripe
    buyMeACoffee: {
        enabled: true,
        username: 'chirag127',  // Your BMC username
        color: '#5F7FFF',
        emoji: '☕',
        message: 'Support this project!'
    },

    // -------------------------------------------------------------------------
    // KO-FI - Similar to BMC, no fees
    // -------------------------------------------------------------------------
    // HOW TO GET: https://ko-fi.com/
    // 1. Sign up and create page
    // 2. Link PayPal or Stripe
    // 3. Get username
    // PAYOUT: Instant, 0% fees
    kofi: {
        enabled: true,
        username: '',  // Your Ko-fi username
        color: '#29abe0'
    },

    // -------------------------------------------------------------------------
    // PAYPAL DONATE - Classic donation button
    // -------------------------------------------------------------------------
    // HOW TO GET: https://www.paypal.com/donate/buttons
    // 1. Go to PayPal Donate Buttons
    // 2. Create donation button
    // 3. Get button ID or email
    // PAYOUT: Instant to PayPal
    paypal: {
        enabled: true,
        email: '',        // Your PayPal email
        buttonId: '',     // Or hosted button ID
        currency: 'USD'
    },

    // -------------------------------------------------------------------------
    // LIBERAPAY - Open source donations
    // -------------------------------------------------------------------------
    // HOW TO GET: https://liberapay.com/
    // 1. Create account
    // 2. Set up receiving
    // PAYOUT: Weekly, via Stripe/PayPal
    liberapay: {
        enabled: false,
        username: ''
    },

    // =========================================================================
    // CRYPTO DONATIONS / WEB3
    // =========================================================================

    // -------------------------------------------------------------------------
    // DIRECT CRYPTO ADDRESSES - Simple wallet display
    // -------------------------------------------------------------------------
    // Just display your wallet addresses for donations
    cryptoAddresses: {
        enabled: true,
        wallets: {
            bitcoin: '',      // Your BTC address
            ethereum: '',     // Your ETH/ERC-20 address
            litecoin: '',
            dogecoin: '',
            solana: '',
            bnb: '',          // BSC address
            polygon: '',      // MATIC address
            usdt_trc20: '',   // Tron USDT
            usdt_erc20: ''    // ETH USDT
        }
    },

    // -------------------------------------------------------------------------
    // COINBASE COMMERCE - Accept many cryptos
    // -------------------------------------------------------------------------
    // HOW TO GET: https://commerce.coinbase.com/
    // 1. Sign up with Coinbase
    // 2. Create checkout/donation button
    // 3. Get checkout ID
    // PAYOUT: Auto to your Coinbase wallet
    coinbaseCommerce: {
        enabled: false,
        checkoutId: ''
    },

    // -------------------------------------------------------------------------
    // NOWPAYMENTS - Accept 100+ cryptocurrencies
    // -------------------------------------------------------------------------
    // HOW TO GET: https://nowpayments.io/
    // 1. Sign up
    // 2. Create donation widget
    // 3. Get API key
    // PAYOUT: Auto-conversion or direct crypto
    nowpayments: {
        enabled: false,
        apiKey: '',
        ipnSecret: ''
    },

    // -------------------------------------------------------------------------
    // GITCOIN - Open source funding
    // -------------------------------------------------------------------------
    // HOW TO GET: https://gitcoin.co/
    // For open source projects, grants and donations
    gitcoin: {
        enabled: false,
        grantUrl: ''
    }
};

// Show donation widgets in this priority
export const donationsPriority = [
    'buyMeACoffee',
    'kofi',
    'paypal',
    'cryptoAddresses',
    'coinbaseCommerce'
];
