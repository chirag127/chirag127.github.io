/**
 * Part 2: Tracking - Heatmaps & Recording
 * @module config/tracking/analytics_heatmaps
 */

export const analytics_heatmaps = {
    clarity: { id: 'v1u8hhnpw2', enabled: true },  // YOUR ID (also in analytics_general)
    hotjar: { siteId: '', enabled: true },
    smartlook: { projectKey: '', enabled: true },
    luckyOrange: { siteId: '', enabled: false },
    inspectlet: { webId: '', enabled: true }
};

export const analytics_heatmaps_priority = ['clarity', 'hotjar', 'smartlook', 'inspectlet'];
