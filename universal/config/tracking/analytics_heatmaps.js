/**
 * Part 2: Tracking - Heatmaps & Session Recording
 * BIG TECH PREFERRED: Microsoft Clarity enabled (100% free)
 * @module config/tracking/analytics_heatmaps
 */

export const analytics_heatmaps = {
    // BIG TECH - ENABLED (Microsoft, completely free)
    clarity: { id: 'v1u8hhnpw2', enabled: true },

    // ALTERNATIVES - Disabled (pick one if Clarity doesn't meet needs)
    hotjar: { siteId: '', enabled: false },  // Free tier limited
    smartlook: { projectKey: '', enabled: false },
    luckyOrange: { siteId: '', enabled: false },
    inspectlet: { webId: '', enabled: false },
    crazyegg: { accountNumber: '', enabled: false }  // Trial only
};

export const analytics_heatmaps_priority = ['clarity', 'hotjar', 'smartlook'];
