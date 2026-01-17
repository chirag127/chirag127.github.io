/**
 * Heatmaps & Session Recording Configuration
 * Visual analytics to see user behavior
 *
 * @module config/heatmaps
 */

export const heatmapsConfig = {

    // =========================================================================
    // MICROSOFT CLARITY - 100% Free forever
    // =========================================================================
    // Already in analytics.config.js - reference only
    // This is your PRIMARY heatmap solution
    clarity: {
        // Configured in analytics.config.js
        enabled: true
    },

    // =========================================================================
    // HOTJAR - Generous free tier
    // =========================================================================
    // HOW TO GET: https://www.hotjar.com/
    // 1. Sign up (free tier: 35 sessions/day)
    // 2. Create site
    // 3. Get site ID
    hotjar: {
        siteId: '',
        enabled: false
    },

    // =========================================================================
    // SMARTLOOK - Session recording
    // =========================================================================
    // HOW TO GET: https://www.smartlook.com/
    // 1. Sign up (free tier available)
    // 2. Create project
    // 3. Get project key
    smartlook: {
        projectKey: '',
        enabled: false
    },

    // =========================================================================
    // LUCKY ORANGE - Heatmaps + chat
    // =========================================================================
    // HOW TO GET: https://www.luckyorange.com/
    // 1. Sign up (free trial)
    // 2. Get site ID
    luckyOrange: {
        siteId: '',
        enabled: false
    },

    // =========================================================================
    // INSPECTLET - Session recording
    // =========================================================================
    // HOW TO GET: https://www.inspectlet.com/
    // 1. Sign up (free tier: 2,500 sessions/month)
    // 2. Get web ID
    inspectlet: {
        webId: '',
        enabled: false
    },

    // =========================================================================
    // FULLSTORY - Digital experience analytics
    // =========================================================================
    // HOW TO GET: https://www.fullstory.com/
    // 1. Sign up (free tier available)
    // 2. Get org ID
    fullstory: {
        orgId: '',
        enabled: false
    },

    // =========================================================================
    // MOUSEFLOW - Session replay
    // =========================================================================
    // HOW TO GET: https://mouseflow.com/
    // 1. Sign up (free tier: 500 recordings/month)
    // 2. Get website ID
    mouseflow: {
        websiteId: '',
        enabled: false
    }
};

// Priority: Use Clarity as primary (free), others as supplements
export const heatmapsPriority = [
    'clarity',     // Free, always first
    'hotjar',      // Popular
    'smartlook',
    'luckyOrange',
    'inspectlet',
    'fullstory',
    'mouseflow'
];
