/**
 * Part 2: Tracking - Heatmaps & Session Recording
 * BIG TECH PREFERRED: Microsoft Clarity enabled (100% free)
 * @module config/tracking/analytics_heatmaps
 */

export const analytics_heatmaps = {
    // BIG TECH - ENABLED (Microsoft, completely free)
    clarity: { id: 'v1u8hhnpw2', enabled: true },

    // ALTERNATIVES - Disabled (pick one if Clarity doesn't meet needs)
    // ALTERNATIVES - Disabled (pick one if Clarity doesn't meet needs)
    // Hotjar
    // Feature: The original heatmap tool
    // Free Limit: 35 daily sessions
    hotjar: { siteId: '', enabled: false },  // Free tier limited

    // Smartlook
    // Feature: Mobile app recording support
    // Free Limit: 3,000 sessions/month
    smartlook: { projectKey: '', enabled: false },

    // Lucky Orange
    // Feature: Chat + Heatmaps
    // Free Limit: 7 day trial (Paid)
    luckyOrange: { siteId: '', enabled: false },

    // Inspectlet
    // Feature: Eye tracking heatmaps
    // Free Limit: 2,500 sessions/month
    inspectlet: { webId: '', enabled: false },

    // CrazyEgg
    // Feature: Snapshot testing
    // Free Limit: 30 day trial
    crazyegg: { accountNumber: '', enabled: false }  // Trial only
};

export const analytics_heatmaps_priority = ['clarity', 'hotjar', 'smartlook', 'luckyOrange', 'inspectlet', 'crazyegg'];
