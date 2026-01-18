/**
 * Part 1: Monetization - File Hosting (PPD)
 * Pay Per Download - disabled by default
 * @module config/monetization/file_hosting
 */

    // ============================================================================
    // UPLOAD-4EVER - Pay Per Download (PPD)
    // ============================================================================
    // Description:
    // A reliable file hosting service that pays you when people download your files.
    //
    // Key Features:
    // - Payout Rates: Tiered system.
    //   - Tier 1 (US/Canada): Up to $7.00 per 1000 downloads.
    //   - Tier 2/3: ~$3.00 - $4.00 per 1000 downloads.
    // - Storage: Generous free storage limits.
    // - Payment Methods: Huge variety (PayPal, Payeer, WebMoney, Crypto, Skrill).
    //
    // Payout Details:
    // - Minimum: $1 (Very low barrier).
    //
    // Best For:
    // - Sharing software, e-books, resource packs, mods.
    //
    upload4ever: { apiKey: '', enabled: false },

    // ============================================================================
    // UP-FILES
    // ============================================================================
    // Description:
    // Another popular PPD host.
    //
    // Key Features:
    // - Competitive rates.
    //
    upfiles: { apiKey: '', enabled: false }
};

export const file_hosting_priority = ['upload4ever', 'upfiles'];
