/**
 * Part 3: Engagement - Rewards & Gamification
 * @module config/engagement/rewards
 */

export const rewards = {
    // ============================================================================
    // GLEAM.IO - Giveaways & Competitions
    // ============================================================================
    // Description:
    // Business growth platform using interactive campaigns.
    //
    // Free Limits (2025):
    // - Unlimited campaigns.
    // - Basic capture of entries.
    // - Limited export and data features.
    //
    gleam: { campaignId: '', enabled: false },

    // ============================================================================
    // VIRALSWEEP
    // ============================================================================
    viralsweep: { apiKey: '', enabled: false }
};

export const rewards_priority = ['gleam'];
