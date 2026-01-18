/**
 * APEX MASTER CONFIGURATION INDEX v3.0
 * Following APEX TECHNICAL AUTHORITY principles:
 * - Client-Side Only Architecture
 * - Modular Integration System
 * - Zero-Defect, High-Velocity, Future-Proof
 * - AI-Native, Neuro-Inclusive, Ethical-First
 *
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

// APEX Global Site Configuration
export const SITE_CONFIG = {
    // Core Stacks
    monetization,
    tracking,
    engagement,
    communication,
    utility,
    baas,

    // APEX Metadata
    version: '3.0',
    architecture: 'APEX_CLIENT_SIDE_ONLY',
    lastUpdated: new Date().toISOString(),

    // Performance Configuration
    performance: {
        lazyLoadIntegrations: true,
        lazyLoadThreshold: 1500,
        maxScriptsPerSecond: 3,
        priorityScripts: ['ga4', 'clarity', 'coinzilla'],
        deferScripts: ['mixpanel', 'amplitude', 'posthog', 'heap'],
        blockWhenSlow: ['ads_display', 'ads_native'],
        enableServiceWorker: true,
        enableCaching: true
    },

    // Security Configuration
    security: {
        enableCSP: true,
        sanitizeInputs: true,
        validateOrigins: true,
        enableSRI: true
    },

    // Accessibility Configuration
    accessibility: {
        enableAriaLabels: true,
        enableKeyboardNav: true,
        enableScreenReader: true,
        enableHighContrast: true,
        enableReducedMotion: true
    }
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

// APEX Performance Settings (Enhanced)
export const performance = {
    // Loading Strategy
    lazyLoadIntegrations: true,
    lazyLoadThreshold: 1500,
    maxScriptsPerSecond: 3,

    // Priority Management
    priorityScripts: ['ga4', 'clarity', 'coinzilla'],
    deferScripts: ['mixpanel', 'amplitude', 'posthog', 'heap'],
    blockWhenSlow: ['ads_display', 'ads_native'],

    // Caching Strategy
    enableServiceWorker: true,
    cacheStrategy: 'stale-while-revalidate',
    cacheDuration: 86400000, // 24 hours

    // Battery Optimization
    enableBatteryAPI: true,
    reduceFeaturesOnLowBattery: true,

    // Network Optimization
    enableNetworkAPI: true,
    adaptToConnectionSpeed: true,

    // Memory Management
    enableMemoryAPI: true,
    cleanupUnusedResources: true
};

// APEX Security Configuration
export const security = {
    // Content Security Policy
    csp: {
        'default-src': ["'self'"],
        'script-src': ["'self'", "'unsafe-inline'", "https://www.googletagmanager.com", "https://www.google-analytics.com"],
        'style-src': ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
        'font-src': ["'self'", "https://fonts.gstatic.com"],
        'img-src': ["'self'", "data:", "https:"],
        'connect-src': ["'self'", "https://api.github.com", "https://www.google-analytics.com"]
    },

    // Input Sanitization
    sanitization: {
        enableDOMPurify: true,
        allowedTags: ['b', 'i', 'em', 'strong', 'a'],
        allowedAttributes: ['href', 'title']
    },

    // Origin Validation
    allowedOrigins: [
        'https://chirag127.github.io',
        'https://localhost:3000',
        'https://127.0.0.1:3000'
    ]
};

// Export individual stacks
export { monetization, tracking, engagement, communication, utility, baas };
