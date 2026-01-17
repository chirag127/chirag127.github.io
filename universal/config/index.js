/**
 * Master Configuration Index
 * 6 STACKS: Monetization, Tracking, Engagement, Communication, Utility, BaaS
 * @module config
 */

// Import all stacks
import { monetization, monetization_priorities } from './monetization/index.js';
import { tracking, tracking_priorities } from './tracking/index.js';
import { engagement, engagement_priorities } from './engagement/index.js';
import { communication, communication_priorities } from './communication/index.js';
import { utility, utility_priorities } from './utility/index.js';
import { baas, baas_priorities } from './baas/index.js';

// Global site configuration
export const SITE_CONFIG = {
    monetization,
    tracking,
    engagement,
    communication,
    utility,
    baas
};

// All priorities for waterfall/fallback logic
export const priorities = {
    monetization: monetization_priorities,
    tracking: tracking_priorities,
    engagement: engagement_priorities,
    communication: communication_priorities,
    utility: utility_priorities,
    baas: baas_priorities
};

// Performance settings
export const performance = {
    lazyLoadIntegrations: true,  // Defer non-critical scripts
    lazyLoadThreshold: 2000,     // ms after DOMContentLoaded
    maxScriptsPerSecond: 2,      // Rate limit script loading
    priorityScripts: ['ga4', 'clarity'],  // Load these first
    deferScripts: ['mixpanel', 'amplitude', 'posthog'],  // Load after page ready
    blockWhenSlow: ['ads_display', 'ads_native']  // Skip on slow connections
};

// Export individual stacks
export { monetization, tracking, engagement, communication, utility, baas };
