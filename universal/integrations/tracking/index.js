/**
 * Tracking Integrations Master Index
 * @module integrations/tracking
 */
import { analytics_general } from './analytics_general/index.js';
import { analytics_heatmaps } from './analytics_heatmaps/index.js';
import { tracking_bugs } from './tracking_bugs/index.js';
import { tracking_performance } from './tracking_performance/index.js';
import { tracking_seo } from './tracking_seo/index.js';
import { auth } from './auth/index.js';

export const tracking = {
    analytics_general, analytics_heatmaps, tracking_bugs,
    tracking_performance, tracking_seo, auth
};
