/**
 * Part 1: Monetization - Crypto Donations
 * @module config/monetization/donation_crypto
 */

export const donation_crypto = {
    // Metamask
    // Feature: Direct wallet connection (Web3)
    // Fee: Gas fees only
    metamask: { walletAddress: '', enabled: true },

    // Bitcoin
    // Feature: Direct address display
    // Fee: Network fees
    bitcoin: { walletAddress: '', enabled: true },

    // CryptoRequest
    // Feature: Payment links
    cryptorequest: { pageId: '', enabled: true },

    // BitPay
    // Feature: Payment processor (Merchant)
    // Fee: ~1% + Network Cost
    bitpay: { buttonId: '', enabled: true },

    // Coinbase Commerce
    // Feature: Managed billing & invoices
    // Fee: 1% transaction fee
    coinbaseCommerce: { checkoutId: '', enabled: true },

    // NOWPayments
    // Feature: Accepts 150+ coins
    // Fee: 0.5% transaction fee
    nowpayments: { apiKey: '', enabled: true }
};

export const donation_crypto_priority = ['metamask', 'bitcoin', 'nowpayments', 'coinbaseCommerce', 'bitpay'];
