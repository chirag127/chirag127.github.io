/**
 * Tracking Integrations Master Index
 * @module integrations/tracking
 */
import { analytics_general } from './analytics_general/index.js';
import { analytics_heatmaps } from './analytics_heatmaps/index.js';
import { auth } from './auth/index.js';
import { tracking_bugs } from './tracking_bugs/index.js';
import { tracking_performance } from './tracking_performance/index.js';
import { tracking_seo } from './tracking_seo/index.js';
import * as auto_track from './auto-track.js';

export const tracking = {
    analytics_general,
    analytics_heatmaps,
    auth,
    tracking_bugs,
    tracking_performance,
    tracking_seo,
    auto_track
};
