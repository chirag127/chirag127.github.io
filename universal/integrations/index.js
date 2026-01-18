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

    // Helper to run tasks when browser is idle to prevent UI blocking
    const runWhenIdle = (task) => {
        if ('requestIdleCallback' in window) {
            requestIdleCallback(() => task(), { timeout: 2000 });
        } else {
            setTimeout(task, 1);
        }
    };

    // Iterate over each stack (monetization, tracking, etc.)
    Object.keys(INTEGRATIONS).forEach((stackKey, stackIndex) => {
        const stack = INTEGRATIONS[stackKey];
        const stackConfig = config[stackKey] || {};

        // Stagger stacks slightly
        setTimeout(() => {
            Object.keys(stack).forEach(moduleKey => {
                const module = stack[moduleKey];

                Object.values(module).forEach(provider => {
                    if (provider && typeof provider.init === 'function' && provider.configKey) {
                        const moduleConfig = stackConfig[moduleKey];
                        if (moduleConfig && moduleConfig[provider.configKey]) {
                            const providerConfig = moduleConfig[provider.configKey];

                            // Check for lazyLoad config - enabled by default for everything unless specified
                            const shouldLazyLoad = providerConfig.lazyLoad !== false;
                            const isEnabled = providerConfig.enabled === true;

                            if (isEnabled) {
                                if (shouldLazyLoad) {
                                    runWhenIdle(() => {
                                        try {
                                            console.debug(`[Universal] Lazy init: ${provider.name}`);
                                            provider.init(providerConfig, loadScript);
                                        } catch (err) {
                                            console.warn(`[Universal] Failed to lazy init ${provider.name}`, err);
                                        }
                                    });
                                } else {
                                    try {
                                        console.debug(`[Universal] Urgent init: ${provider.name}`);
                                        provider.init(providerConfig, loadScript);
                                    } catch (err) {
                                        console.warn(`[Universal] Failed to init ${provider.name}`, err);
                                    }
                                }
                            }
                        }
                    }
                });
            });
        }, stackIndex * 100); // 100ms delay between stacks
    });
}

export { monetization, tracking, engagement, communication, utility, baas };
