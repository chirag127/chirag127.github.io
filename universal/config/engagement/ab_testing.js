/**
 * Part 3: Engagement - A/B Testing & Experimentation
 * @module config/engagement/ab_testing
 *
 * This module provides configuration for A/B testing providers and
 * the polymorph multi-armed bandit optimization system.
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
    // GROWTHBOOK - The Open Source Powerhouse (RECOMMENDED)
    // ============================================================================
    // Description:
    // Fully featured feature flagging and A/B testing platform.
    // We use this for client-side multi-armed bandit optimization of polymorphs.
    //
    // Key Features:
    // - Unlimited experiments and traffic.
    // - Bayesian or Frequentist statistics.
    // - Multi-armed bandit with Thompson Sampling.
    // - Direct connection to your data warehouse.
    //
    // Free Limits (Cloud 2025):
    // - **3 Users**.
    // - 1 Million CDN requests/month.
    // - **Unlimited (Self-hosted)**.
    //
    // Best For:
    // - Developers who want the most control and "unlimited" feel.
    // - Static sites needing client-side experimentation.
    //
    // Implementation:
    // - Uses localStorage for persistence (no backend required).
    // - Tracks impressions and conversions per variant.
    // - Thompson Sampling auto-optimizes to show best variants more often.
    //
    growthbook: {
        enabled: true,
        // Your specific API key
        apiKey: 'sdk-BamkgvyjaSFKa0m6',
        clientKey: 'sdk-BamkgvyjaSFKa0m6',
        apiHost: 'https://cdn.growthbook.io',
        // Client-side polymorph A/B testing (no API key required)
        clientSideEnabled: true,
        // Enhanced tracking integration
        trackingIntegration: {
            ga4: true,
            gtm: true,
            clarity: true,
            mixpanel: true,
            amplitude: true,
            posthog: true,
            heap: true
        },
        // Auto-optimization settings
        enableDevMode: true,
        enableAutoOptimization: true,
        plugins: ['autoAttributesPlugin', 'thirdPartyTrackingPlugin']
    },

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

// ============================================================================
// POLYMORPHS A/B TESTING CONFIGURATION
// ============================================================================
// Description:
// Configuration for the polymorph multi-armed bandit system.
// Variants are auto-discovered from the /polymorphs/ directory.
//
// How it works:
// 1. On page load, scans polymorphs folder for available variants
// 2. Uses Thompson Sampling to select best-performing variant
// 3. Tracks conversions on tool card clicks
// 4. Automatically optimizes traffic towards winners
//
// Free & Open Source:
// - 100% client-side, no external API calls
// - Uses localStorage for all data persistence
// - No tracking limits or costs
//
export const polymorphs_ab = {
    enabled: true,

    // Use multi-armed bandit (Thompson Sampling) for auto-optimization
    // If false, uses simple random weighted selection
    enableBandit: true,

    // Number of impressions before switching from exploration to exploitation
    // During exploration phase, variants are selected randomly
    explorationThreshold: 50,

    // What action counts as a "conversion"
    // Options: 'tool_click', 'time_on_page', 'scroll_depth'
    conversionEvent: 'tool_click',

    // Polymorphs folder path (relative to site root)
    polymorphsPath: '/polymorphs/',

    // Control variant settings
    control: {
        id: 'control',
        slug: null,  // null means stay on index.html
        weight: 1
    },

    // Storage keys (localStorage)
    storageKeys: {
        visitorId: 'gb_visitor_id',
        experimentData: 'gb_polymorph_ab',
        manualOverride: 'gb_polymorph_override'
    },

    // Experiment identifier
    experimentId: 'polymorph_ab_v1'
};

export const ab_testing_priority = ['growthbook', 'vwo'];
