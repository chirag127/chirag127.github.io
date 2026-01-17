/**
 * Universal Configuration Master Index
 * Aggregates ALL configuration modules into a single SITE_CONFIG object
 *
 * ARCHITECTURE:
 * - Each category has its own config file
 * - All configs are merged here
 * - Fallback patterns are defined per category
 * - Missing configs = service disabled (no crashes)
 *
 * @module config
 */

// ============================================================================
// IMPORT ALL CONFIG MODULES
// ============================================================================

// Analytics & Tracking
import { analyticsConfig } from './analytics.config.js';
import { heatmapsConfig } from './heatmaps.config.js';
import { monitoringConfig } from './monitoring.config.js';
import { performanceConfig } from './performance.config.js';
import { seoConfig } from './seo.config.js';

// Monetization
import { displayAdsConfig, displayAdsPriority } from './ads/display.config.js';
import { cryptoAdsConfig, cryptoAdsPriority } from './ads/crypto.config.js';
import { popunderAdsConfig, popunderAdsPriority, popunderLimits } from './ads/popunder.config.js';
import { pushAdsConfig, pushAdsPriority } from './ads/push.config.js';
import { textAdsConfig, textAdsPriority } from './ads/text.config.js';
import { donationsConfig, donationsPriority } from './ads/donations.config.js';
import { affiliatesConfig } from './ads/affiliates.config.js';

// Engagement
import { engagementConfig, shareButtonsPriority, commentsPriority } from './engagement.config.js';

// Communication
import { chatConfig, chatPriority } from './chat.config.js';

// Infrastructure
import { utilityConfig } from './utility.config.js';
import { authConfig, authPriority } from './auth.config.js';

// ============================================================================
// BUILD MASTER CONFIG
// ============================================================================

export const SITE_CONFIG = {
    // ----- Analytics -----
    ...analyticsConfig,

    // ----- Heatmaps -----
    ...heatmapsConfig,

    // ----- Monitoring -----
    ...monitoringConfig,

    // ----- Performance -----
    ...performanceConfig,

    // ----- SEO -----
    seo: seoConfig,

    // ----- Display Ads -----
    ...displayAdsConfig,

    // ----- Crypto Ads -----
    ...cryptoAdsConfig,

    // ----- Pop-Under Ads -----
    ...popunderAdsConfig,
    popunderLimits,

    // ----- Push Ads -----
    ...pushAdsConfig,

    // ----- Text Ads -----
    ...textAdsConfig,

    // ----- Donations -----
    ...donationsConfig,

    // ----- Affiliates -----
    ...affiliatesConfig,

    // ----- Engagement -----
    ...engagementConfig,

    // ----- Chat -----
    ...chatConfig,

    // ----- Utility -----
    ...utilityConfig,

    // ----- Auth -----
    ...authConfig
};

// ============================================================================
// EXPORT PRIORITY ARRAYS (for fallback logic)
// ============================================================================

export const priorities = {
    displayAds: displayAdsPriority,
    cryptoAds: cryptoAdsPriority,
    popunderAds: popunderAdsPriority,
    pushAds: pushAdsPriority,
    textAds: textAdsPriority,
    donations: donationsPriority,
    shareButtons: shareButtonsPriority,
    comments: commentsPriority,
    chat: chatPriority,
    auth: authPriority
};

// ============================================================================
// EXPORT INDIVIDUAL CONFIGS (for selective imports)
// ============================================================================

export {
    analyticsConfig,
    heatmapsConfig,
    monitoringConfig,
    performanceConfig,
    seoConfig,
    displayAdsConfig,
    cryptoAdsConfig,
    popunderAdsConfig,
    pushAdsConfig,
    textAdsConfig,
    donationsConfig,
    affiliatesConfig,
    engagementConfig,
    chatConfig,
    utilityConfig,
    authConfig
};

// ============================================================================
// SET GLOBAL FOR BACKWARD COMPATIBILITY
// ============================================================================

if (typeof window !== 'undefined') {
    window.SITE_CONFIG = SITE_CONFIG;
    window.CONFIG_PRIORITIES = priorities;
}

// ============================================================================
// HELPER: Get first enabled service from priority list
// ============================================================================

export function getFirstEnabled(priorityList, config = SITE_CONFIG) {
    for (const key of priorityList) {
        const service = config[key];
        if (service && service.enabled) {
            return { key, config: service };
        }
    }
    return null;
}

// ============================================================================
// HELPER: Get all enabled services from a category
// ============================================================================

export function getAllEnabled(priorityList, config = SITE_CONFIG) {
    return priorityList
        .filter(key => config[key] && config[key].enabled)
        .map(key => ({ key, config: config[key] }));
}
