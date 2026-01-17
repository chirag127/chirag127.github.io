/**
 * Part 2: Tracking - Index
 * @module config/tracking
 */

import { analytics_general, analytics_general_priority } from './analytics_general.js';
import { analytics_heatmaps, analytics_heatmaps_priority } from './analytics_heatmaps.js';
import { tracking_bugs, tracking_bugs_priority } from './tracking_bugs.js';
import { tracking_performance, tracking_seo, tracking_performance_priority, tracking_seo_priority } from './tracking_performance.js';
import { auth, auth_priority } from './auth.js';

export const tracking = {
    ...analytics_general, ...analytics_heatmaps, ...tracking_bugs,
    ...tracking_performance, ...tracking_seo, ...auth
};

export const tracking_priorities = {
    analytics_general: analytics_general_priority, analytics_heatmaps: analytics_heatmaps_priority,
    tracking_bugs: tracking_bugs_priority, tracking_performance: tracking_performance_priority,
    tracking_seo: tracking_seo_priority, auth: auth_priority
};

export { analytics_general, analytics_heatmaps, tracking_bugs, tracking_performance, tracking_seo, auth };
