/**
 * Part 2: Tracking - Index
 * @module config/tracking
 */

import { analytics_general, analytics_general_priority } from './analytics_general.js';
import { analytics_heatmaps, analytics_heatmaps_priority } from './analytics_heatmaps.js';
import { tracking_bugs, tracking_bugs_priority } from './tracking_bugs.js';
import { tracking_performance, tracking_performance_priority } from './tracking_performance.js';
import { tracking_seo, tracking_seo_priority } from './tracking_seo.js';
import { auth, auth_priority } from './auth.js';
import { attribution, attribution_priority } from './attribution.js';
import { realtime_analytics, realtime_analytics_priority } from './realtime_analytics.js';

export const tracking = {
    ...analytics_general, ...analytics_heatmaps, ...tracking_bugs,
    ...tracking_performance, ...tracking_seo, ...auth, ...attribution, ...realtime_analytics
};

export const tracking_priorities = {
    analytics_general: analytics_general_priority, analytics_heatmaps: analytics_heatmaps_priority,
    tracking_bugs: tracking_bugs_priority, tracking_performance: tracking_performance_priority,
    tracking_seo: tracking_seo_priority, auth: auth_priority,
    attribution: attribution_priority, realtime_analytics: realtime_analytics_priority
};

export { analytics_general, analytics_heatmaps, tracking_bugs, tracking_performance, tracking_seo, auth, attribution, realtime_analytics };
