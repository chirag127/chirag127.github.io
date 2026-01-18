/**
 * UNIVERSAL INTEGRATIONS MASTER INDEX
 * @module integrations
 */
import { monetization } from './monetization/index.js';
import { tracking } from './tracking/index.js';
import { engagement } from './engagement/index.js';
import { communication } from './communication/index.js';
import { utility } from './utility/index.js';
import { baas } from './baas/index.js';

export const INTEGRATIONS = {
    monetization, tracking, engagement, communication, utility, baas
};

// Helper to load external scripts dynamically
function loadScript(src, id) {
    return new Promise((resolve, reject) => {
        if (document.getElementById(id || src)) return resolve();
        const s = document.createElement('script');
        s.src = src;
        s.id = id || src;
        s.async = true;
        s.onload = resolve;
        s.onerror = reject;
        document.head.appendChild(s);
    });
}

// Start function to initialize integrations based on config
export function initIntegrations(config) {
    console.log('[Universal] Initializing integrations...', config);

    // Iterate over each stack (monetization, tracking, etc.)
    Object.keys(INTEGRATIONS).forEach(stackKey => {
        const stack = INTEGRATIONS[stackKey];
        const stackConfig = config[stackKey] || {};

        // Iterate over modules within key (e.g. baas -> cms, database)
        Object.keys(stack).forEach(moduleKey => {
            const module = stack[moduleKey];

            // Handle nested structure (like baas.cms) vs flat structure (like utility)
            // If the module object has 'index.js' exports of sub-providers, we iterate them.
            // We identify providers by checking if they have an 'init' function or 'configKey'.

            Object.values(module).forEach(provider => {
                if (provider && typeof provider.init === 'function' && provider.configKey) {
                    // It's a provider!
                    // Find its config.
                    // Example: config.baas.cms.contentful
                    // Stack: baas, Module: cms, Provider: contentful
                    // But config structure is config.baas.cms = { contentful: ... }
                    // OR config.engagement.social_share = { addThis: ... }

                    // We need to find the correct config object.
                    // Try to find it in the stack config under the module key.
                    const moduleConfig = stackConfig[moduleKey]; // e.g. config.baas.cms

                    if (moduleConfig && moduleConfig[provider.configKey]) {
                        const providerConfig = moduleConfig[provider.configKey];
                        try {
                            provider.init(providerConfig, loadScript);
                        } catch (err) {
                            console.error(`[Universal] Failed to init ${provider.name}`, err);
                        }
                    }
                } else if (typeof provider === 'object') {
                    // Recursion for deeper nesting if needed, or simple flattened loop above covers it
                    // The structure seems to be: INTEGRATIONS.baas.cms = { contentful: mod, ... }
                    // So module is the object containing providers.
                    // The loop `Object.values(module)` gets the provider module directly.
                }
            });
        });
    });
}

export { monetization, tracking, engagement, communication, utility, baas };
