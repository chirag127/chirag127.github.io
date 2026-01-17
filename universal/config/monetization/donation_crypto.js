/**
 * Part 1: Monetization - Crypto Donations
 * @module config/monetization/donation_crypto
 */

export const donation_crypto = {
    metamask: { walletAddress: '', enabled: true },
    bitcoin: { walletAddress: '', enabled: true },
    cryptorequest: { pageId: '', enabled: true },
    bitpay: { buttonId: '', enabled: true },
    coinbaseCommerce: { checkoutId: '', enabled: true },
    nowpayments: { apiKey: '', enabled: true }
};

export const donation_crypto_priority = ['metamask', 'bitcoin', 'nowpayments', 'coinbaseCommerce', 'bitpay'];
