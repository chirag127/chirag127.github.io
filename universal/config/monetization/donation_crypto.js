/**
 * Part 1: Monetization - Crypto Donations
 * Direct, fee-minimal support
 * @module config/monetization/donation_crypto
 */

export const donation_crypto = {
    // ============================================================================
    // METAMASK / WEB3 - One-Click Support
    // ============================================================================
    // Description:
    // Allow users to send crypto directly from their browser extension.
    //
    // Key Features:
    // - Direct "Connect Wallet" flow.
    // - No middleman.
    //
    // Fees:
    // - 0% Platform Fee.
    // - User pays Network (Gas) fees.
    //
    metamask: { walletAddress: '', enabled: true },

    // ============================================================================
    // BITCOIN / STATIC ADDRESS
    // ============================================================================
    // Description:
    // Simply display your public address for manual transfers.
    //
    // Fees:
    // - 0% Platform Fee.
    // - User pays Network fees.
    //
    bitcoin: { walletAddress: '', enabled: true },

    // ============================================================================
    // NOWPAYMENTS - Professional Crypto Gate
    // ============================================================================
    // Description:
    // Accept 150+ cryptocurrencies with automatic conversion.
    //
    // Key Features:
    // - Massive list of supported coins.
    // - Donation widgets and buttons.
    // - API for custom integrations.
    //
    // Fees:
    // - Transaction Fee: ~0.5%.
    //
    // Payout Details:
    // - Instant payout to your wallet once minimum is met.
    //
    nowpayments: { apiKey: '', enabled: true },

    // ============================================================================
    // COINBASE COMMERCE - Merchant Grade
    // ============================================================================
    // Description:
    // Managed payment portal by Coinbase.
    //
    // Fees:
    // - 1% Transaction fee.
    //
    coinbaseCommerce: { checkoutId: '', enabled: true },

    // ============================================================================
    // BITPAY - Enterprise Payments
    // ============================================================================
    // Fees:
    // - 1% - 2% depending on volume.
    //
    bitpay: { buttonId: '', enabled: true }
};

export const donation_crypto_priority = ['metamask', 'bitcoin', 'nowpayments', 'coinbaseCommerce', 'bitpay'];
