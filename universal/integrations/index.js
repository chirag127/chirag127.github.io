/**
 * Universal Integrations Master Index
 * Aggregates all integration category modules
 * @module integrations
 */

// Import all category providers
import { providers as analyticsProviders, Analytics } from './analytics/index.js';
import { providers as monitoringProviders, Monitoring } from './monitoring/index.js';
import { providers as adsProviders, Ads } from './ads/index.js';
import { providers as chatProviders, Chat } from './chat/index.js';

// Export category modules
export {
    analyticsProviders,
    monitoringProviders,
    adsProviders,
    chatProviders
};

// Legacy exports for backward compatibility
export { Analytics, Monitoring, Ads, Chat };

// Master providers object for dynamic iteration
export const allProviders = {
    analytics: analyticsProviders,
    monitoring: monitoringProviders,
    ads: adsProviders,
    chat: chatProviders
};

/**
 * Initialize all providers in a category
 * @param {Object} providers - Provider modules object
 * @param {Object} config - Site configuration
 * @param {Function} loadScript - Script loader function
 * @param {string} categoryName - Name for logging
 */
export function initCategory(providers, config, loadScript, categoryName = 'Integration') {
    Object.entries(providers).forEach(([key, provider]) => {
        const configKey = provider.configKey || key;
        const providerConfig = config[configKey];

        if (providerConfig && providerConfig.enabled) {
            try {
                provider.init(providerConfig, loadScript, config);
                console.log(`✅ Loaded ${categoryName}: ${provider.name || key}`);
            } catch (e) {
                console.error(`❌ Failed to init ${categoryName} ${key}:`, e);
            }
        }
    });
}

/**
 * Initialize all integrations
 * @param {Object} config - Site configuration
 * @param {Function} loadScript - Script loader function
 */
export function initAll(config, loadScript) {
    initCategory(analyticsProviders, config, loadScript, 'Analytics');
    initCategory(monitoringProviders, config, loadScript, 'Monitoring');
    initCategory(adsProviders, config, loadScript, 'Ads');
    initCategory(chatProviders, config, loadScript, 'Chat');
}
