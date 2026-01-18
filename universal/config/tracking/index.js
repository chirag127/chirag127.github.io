import * as analytics_general from './analytics_general.js';
import * as analytics_heatmaps from './analytics_heatmaps.js';
import * as attribution from './attribution.js';
import * as auth from './auth.js';
import * as realtime_analytics from './realtime_analytics.js';
import * as tracking_bugs from './tracking_bugs.js';
import * as tracking_performance from './tracking_performance.js';
import * as tracking_seo from './tracking_seo.js';

export const tracking = {
    analytics_general, analytics_heatmaps, attribution, auth,
    realtime_analytics, tracking_bugs, tracking_performance, tracking_seo
};

export {
    analytics_general, analytics_heatmaps, attribution, auth,
    realtime_analytics, tracking_bugs, tracking_performance, tracking_seo
};

/**
 * GLOBAL TRACKING PRIORITIES
 * Defines the initialization order for analytics scripts to minimize impact.
 */
export const tracking_priorities = {
    // CRITICAL - Load Immediately
    critical: ['tracking_seo', 'analytics_general'],

    // VISUAL - Load after first paint
    visual: ['analytics_heatmaps'],

    // SYSTEMS - Load when idle or background
    systems: ['tracking_bugs', 'tracking_performance', 'attribution', 'auth', 'realtime_analytics']
};
