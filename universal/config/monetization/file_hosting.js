/**
 * Part 1: Monetization - File Hosting (PPD)
 * Pay Per Download
 * @module config/monetization/file_hosting
 */

export const file_hosting = {
    // ============================================================================
    // UPLOAD-4EVER - Low Threshold Leader
    // ============================================================================
    // Description:
    // Monetize your file downloads with high rates.
    //
    // Key Features:
    // - Rates: Up to $7 per 1000 downloads for Tier 1 traffic.
    // - Referral: 10% commission.
    //
    // Payout Details:
    // - **Minimum Payout: $1** (Extremely accessible).
    // - Methods: PayPal, Payeer, Bitcoin, Skrill, Neteller.
    //
    upload4ever: { apiKey: '', enabled: false },

    // ============================================================================
    // UP-FILES - High Reliability
    // ============================================================================
    // Description:
    // Professional file storage with monetization.
    //
    // Payout Details:
    // - Minimum Payout: $5.
    // - Rates: Competitive global rates.
    //
    upfiles: { apiKey: '', enabled: false }
};

export const file_hosting_priority = ['upload4ever', 'upfiles'];
