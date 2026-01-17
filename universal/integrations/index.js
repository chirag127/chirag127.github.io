/**
 * Universal Integrations Master Index
 * Aggregates ALL integration category modules
 * @module integrations
 */

// Import all category providers
import { providers as analyticsProviders, Analytics } from './analytics/index.js';
import { providers as monitoringProviders, Monitoring } from './monitoring/index.js';
import { providers as heatmapsProviders } from './heatmaps/index.js';
import {
    providers as adsProviders,
    Ads,
    displayProviders,
    cryptoProviders,
    popunderProviders,
    pushProviders,
    textProviders,
    donationProviders,
    cryptoTippingProviders,
    displayPriority,
    cryptoPriority,
    popunderPriority,
    pushPriority,
    textPriority,
    donationPriority
} from './ads/index.js';
import { providers as chatProviders, Chat, chatPriority } from './chat/index.js';
import { providers as engagementProviders, shareProviders, commentProviders, sharePriority, commentPriority } from './engagement/index.js';
import { providers as utilityProviders, captchaPriority } from './utility/index.js';

// Export category modules
export {
    analyticsProviders,
    monitoringProviders,
    heatmapsProviders,
    adsProviders,
    chatProviders,
    engagementProviders,
    utilityProviders
};

// Sub-category exports for ads
export {
    displayProviders,
    cryptoProviders,
    popunderProviders,
    pushProviders,
    textProviders,
    donationProviders,
    cryptoTippingProviders,
    displayPriority,
    cryptoPriority,
    popunderPriority,
    pushPriority,
    textPriority,
    donationPriority
};

// Sub-category exports for engagement
export {
    shareProviders,
    commentProviders,
    sharePriority,
    commentPriority
};

// Priority exports
export { chatPriority, captchaPriority };

// Legacy exports for backward compatibility
export { Analytics, Monitoring, Ads, Chat };

// Master providers object
export const allProviders = {
    analytics: analyticsProviders,
    monitoring: monitoringProviders,
    heatmaps: heatmapsProviders,
    ads: adsProviders,
    chat: chatProviders,
    engagement: engagementProviders,
    utility: utilityProviders
};

/**
 * Initialize all providers in a category
 */
export function initCategory(providers, config, loadScript, categoryName = 'Integration') {
    const results = { success: [], failed: [], skipped: [] };
    if (!providers) return results;

    Object.entries(providers).forEach(([key, provider]) => {
        if (!provider || typeof provider.init !== 'function') {
            results.skipped.push(key);
            return;
        }

        const configKey = provider.configKey || key;
        const providerConfig = config[configKey];

        if (providerConfig && providerConfig.enabled) {
            try {
                provider.init(providerConfig, loadScript, config);
                console.log(`✅ ${categoryName}: ${provider.name || key}`);
                results.success.push(key);
            } catch (e) {
                console.error(`❌ ${categoryName} ${key}:`, e);
                results.failed.push(key);
            }
        } else {
            results.skipped.push(key);
        }
    });

    return results;
}

/**
 * Initialize with fallback - try providers in order until one succeeds
 */
export function initWithFallback(priorityList, providers, config, loadScript, categoryName = 'Integration') {
    if (!priorityList || !providers) return { key: null, success: false };

    for (const key of priorityList) {
        const provider = providers[key];
        if (!provider) continue;

        const providerConfig = config[provider.configKey || key];

        if (provider && providerConfig && providerConfig.enabled) {
            try {
                provider.init(providerConfig, loadScript, config);
                console.log(`✅ ${categoryName} (primary): ${provider.name || key}`);
                return { key, success: true };
            } catch (e) {
                console.warn(`⚠️ ${categoryName} ${key} failed, trying next...`);
            }
        }
    }

    console.warn(`❌ ${categoryName}: No providers available`);
    return { key: null, success: false };
}

/**
 * Initialize all integrations with proper fallback patterns
 */
export function initAll(config, loadScript) {
    // Analytics - load ALL enabled
    initCategory(analyticsProviders, config, loadScript, 'Analytics');

    // Heatmaps - load ALL enabled
    initCategory(heatmapsProviders, config, loadScript, 'Heatmaps');

    // Monitoring - load ALL enabled
    initCategory(monitoringProviders, config, loadScript, 'Monitoring');

    // Display Ads - load ALL enabled
    initCategory(displayProviders, config, loadScript, 'Display Ads');

    // Crypto Ads - load ALL enabled
    initCategory(cryptoProviders, config, loadScript, 'Crypto Ads');

    // Pop-under - use ONE at a time
    initWithFallback(popunderPriority, popunderProviders, config, loadScript, 'Pop-Under');

    // Push Ads - load ALL enabled
    initCategory(pushProviders, config, loadScript, 'Push Ads');

    // Text Ads - load ALL enabled
    initCategory(textProviders, config, loadScript, 'Text Ads');

    // Donations - load ALL enabled
    initCategory(donationProviders, config, loadScript, 'Donations');

    // Crypto Tipping - load ALL enabled
    initCategory(cryptoTippingProviders, config, loadScript, 'Crypto Tipping');

    // Chat - use fallback (only one widget)
    initWithFallback(chatPriority, chatProviders, config, loadScript, 'Chat');

    // Social Share - use fallback
    initWithFallback(sharePriority, shareProviders, config, loadScript, 'Social Share');

    // Comments - load ALL enabled
    initCategory(commentProviders, config, loadScript, 'Comments');

    // Utility/Captcha - use fallback
    initWithFallback(captchaPriority, utilityProviders, config, loadScript, 'Captcha');
}
