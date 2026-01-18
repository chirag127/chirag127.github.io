/**
 * Part 3: Engagement - A/B Testing & Experimentation
 * @module config/engagement/ab_testing
 */

export const ab_testing = {
    // ============================================================================
    // VWO (Visual Website Optimizer) - Professional Choice
    // ============================================================================
    // Description:
    // A comprehensive experimentation platform for small and medium sites.
    //
    // Key Features:
    // - Visual Editor (No-code changes).
    // - Split testing and multivariate testing.
    // - Integrated heatmaps and recordings.
    //
    // Free Tier Limits (2025 - "Starter" Plan):
    // - **50,000 Monthly Tracked Users (MTUs)**.
    // - Unlimited experiments.
    //
    // Best For:
    // - Marketing teams wanting a visual interface.
    //
    vwo: { accountId: '', enabled: false },

    // ============================================================================
    // GROWTHBOOK - The Open Source Powerhouse
    // ============================================================================
    // Description:
    // Fully featured feature flagging and A/B testing platform.
    //
    // Key Features:
    // - Unlimited experiments and traffic.
    // - Bayesian or Frequentist statistics.
    // - Direct connection to your data warehouse.
    //
    // Free Limits (Cloud 2025):
    // - **3 Users**.
    // - 1 Million CDN requests/month.
    // - **Unlimited (Self-hosted)**.
    //
    // Best For:
    // - Developers who want the most control and "unlimited" feel.
    //
    growthbook: { apiKey: '', enabled: false },

    // ============================================================================
    // OPTIMIZELY - Enterprise Experimentation
    // ============================================================================
    // Description:
    // High-end experimentation.
    //
    // ⚠️ FREE LIMITS NOTE:
    // - **Standard A/B testing is NOT free** (Enterprise pricing).
    // - "Rollouts" (Feature Flagging) has a free tier for 1 concurrent experiment.
    //
    optimizely: { sdkKey: '', enabled: false }
};

export const ab_testing_priority = ['growthbook', 'vwo'];
