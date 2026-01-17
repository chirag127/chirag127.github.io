/**
 * Universal Configuration Index
 * Aggregates all configuration modules into a single SITE_CONFIG object
 * @module config
 */

import { analyticsConfig } from './analytics.config.js';
import { monitoringConfig } from './monitoring.config.js';
import { adsConfig } from './ads.config.js';
import { chatConfig } from './chat.config.js';
import { authConfig } from './auth.config.js';

// Merge all configs into the global SITE_CONFIG
export const SITE_CONFIG = {
    // Analytics
    ...analyticsConfig,

    // Monitoring
    ...monitoringConfig,

    // Ads
    ...adsConfig,

    // Chat
    ...chatConfig,

    // Auth
    ...authConfig
};

// Also export individual configs for selective imports
export {
    analyticsConfig,
    monitoringConfig,
    adsConfig,
    chatConfig,
    authConfig
};

// Set global for backward compatibility
if (typeof window !== 'undefined') {
    window.SITE_CONFIG = SITE_CONFIG;
}
