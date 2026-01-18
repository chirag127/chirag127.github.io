/**
 * Part 3: Engagement - A/B Testing
 * Test different versions of your site to optimize conversions
 * @module config/engagement/ab_testing
 */

export const ab_testing = {
    // ============================================================================
    // VWO (Visual Website Optimizer) - Comprehensive A/B Testing
    // ============================================================================
    // What it does:
    // - Visual editor for creating test variations (no coding required)
    // - A/B testing, multivariate testing, split URL testing
    // - Heatmaps and session recordings included
    // - Conversion funnel analysis
    // - Targeting and segmentation
    // - Statistical significance calculator
    // - Mobile app testing
    //
    // What it doesn't do:
    // - Free tier limited to low traffic sites
    // - No advanced personalization in free tier
    // - Limited integrations on free tier
    //
    // Free Tier Limits (Free Plan):
    // - Up to 50,000 visitors per month
    // - 1 website
    // - Basic A/B testing
    // - Heatmaps included
    // - 30-day data retention
    // - Community support
    //
    // Best for: Small to medium sites, conversion optimization, UX testing
    // Website: https://vwo.com
    // Note: Good free tier for sites under 50k monthly visitors
    vwo: { accountId: '', enabled: true },

};

export const ab_testing_priority = ['vwo'];

export const ab_testing_priority = ['vwo', 'crazyegg', 'abtasty'];

// Made with Bob
