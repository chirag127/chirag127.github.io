/**
 * Part 3: Engagement - A/B Testing
 * @module config/engagement/ab_testing
 */
export const ab_testing = {
    // VWO (Visual Website Optimizer)
    // Feature: Visual editor, heatmaps included
    // Free Limit: Free plan for < 50k visitors/month
    vwo: { accountId: '', enabled: true },

    // CrazyEgg
    // Feature: Simple A/B testing
    // Free Limit: 30 day trial
    crazyegg: { accountNumber: '', enabled: true },

    // AB Tasty
    // Feature: AI-driven experimentation
    // Free Limit: Enterprise only
    abtasty: { accountId: '', enabled: false }
};

export const ab_testing_priority = ['vwo', 'crazyegg', 'abtasty'];
