/**
 * APEX UNIVERSAL INTEGRATIONS MASTER INDEX v3.0
 * Following APEX TECHNICAL AUTHORITY principles:
 * - Client-Side Only Architecture
 * - Modular Integration System
 * - Performance Optimized
 * - Battery-Aware
 * - Accessibility Compliant
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

// APEX Script Loader with Enhanced Error Handling
function loadScript(src, id, options = {}) {
    return new Promise((resolve, reject) => {
        // Check if already loaded
        if (document.getElementById(id || src)) {
            console.debug(`[APEX] Script already loaded: ${src}`);
            return resolve();
        }

        const script = document.createElement('script');
        script.src = src;
        script.id = id || src;
        script.async = options.async !== false;
        script.defer = options.defer || false;

        // Add integrity if provided
        if (options.integrity) {
            script.integrity = options.integrity;
            script.crossOrigin = 'anonymous';
        }

        // Performance monitoring
        const startTime = performance.now();

        script.onload = () => {
            const loadTime = performance.now() - startTime;
            console.debug(`[APEX] Script loaded: ${src} (${loadTime.toFixed(2)}ms)`);
            resolve();
        };

        script.onerror = (error) => {
            console.warn(`[APEX] Script failed to load: ${src}`, error);
            reject(error);
        };

        // Timeout handling
        const timeout = options.timeout || 10000;
        const timeoutId = setTimeout(() => {
            console.warn(`[APEX] Script timeout: ${src}`);
            reject(new Error(`Script timeout: ${src}`));
        }, timeout);

        script.onload = () => {
            clearTimeout(timeoutId);
            const loadTime = performance.now() - startTime;
            console.debug(`[APEX] Script loaded: ${src} (${loadTime.toFixed(2)}ms)`);
            resolve();
        };

        document.head.appendChild(script);
    });
}

// APEX Integration Initializer with Performance Optimization
export function initIntegrations(config) {
    console.log('[APEX] Initializing integrations with performance optimization...', config);

    // Battery API Support
    const battery = navigator.battery || navigator.getBattery?.();
    let lowBattery = false;

    if (battery) {
        battery.then?.(b => {
            lowBattery = b.level < 0.2 && !b.charging;
            if (lowBattery) {
                console.log('[APEX] Low battery detected, reducing features');
            }
        });
    }

    // Network API Support
    const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    const slowConnection = connection?.effectiveType === 'slow-2g' || connection?.effectiveType === '2g';

    if (slowConnection) {
        console.log('[APEX] Slow connection detected, optimizing loading');
    }

    // Enhanced Idle Callback with Fallback
    const runWhenIdle = (task, options = {}) => {
        const timeout = options.timeout || 2000;
        const priority = options.priority || 'normal';

        if ('requestIdleCallback' in window && !lowBattery) {
            requestIdleCallback(() => {
                try {
                    task();
                } catch (error) {
                    console.error('[APEX] Task error:', error);
                }
            }, { timeout });
        } else {
            // Fallback for browsers without requestIdleCallback or low battery
            const delay = priority === 'high' ? 1 : (priority === 'low' ? 5000 : 1000);
            setTimeout(() => {
                try {
                    task();
                } catch (error) {
                    console.error('[APEX] Task error:', error);
                }
            }, delay);
        }
    };

    // Performance monitoring
    const performanceMetrics = {
        startTime: performance.now(),
        scriptsLoaded: 0,
        scriptsFailed: 0,
        totalLoadTime: 0
    };

    // Process each integration stack
    Object.keys(INTEGRATIONS).forEach((stackKey, stackIndex) => {
        const stack = INTEGRATIONS[stackKey];
        const stackConfig = config[stackKey] || {};

        // Stagger stacks for better performance
        const stackDelay = stackIndex * 150; // 150ms between stacks

        setTimeout(() => {
            console.debug(`[APEX] Processing stack: ${stackKey}`);

            Object.keys(stack).forEach(moduleKey => {
                const module = stack[moduleKey];

                Object.values(module).forEach(provider => {
                    if (provider && typeof provider.init === 'function' && provider.configKey) {
                        const moduleConfig = stackConfig[moduleKey];
                        if (moduleConfig && moduleConfig[provider.configKey]) {
                            const providerConfig = moduleConfig[provider.configKey];

                            // Enhanced configuration checks
                            const isEnabled = providerConfig.enabled === true;
                            const shouldLazyLoad = providerConfig.lazyLoad !== false;
                            const priority = providerConfig.priority || 'normal';
                            const skipOnSlowConnection = providerConfig.skipOnSlowConnection && slowConnection;
                            const skipOnLowBattery = providerConfig.skipOnLowBattery && lowBattery;

                            if (!isEnabled || skipOnSlowConnection || skipOnLowBattery) {
                                if (skipOnSlowConnection) {
                                    console.debug(`[APEX] Skipping ${provider.name} due to slow connection`);
                                }
                                if (skipOnLowBattery) {
                                    console.debug(`[APEX] Skipping ${provider.name} due to low battery`);
                                }
                                return;
                            }

                            const initProvider = async () => {
                                try {
                                    const startTime = performance.now();
                                    console.debug(`[APEX] Initializing: ${provider.name} (${priority} priority)`);

                                    await provider.init(providerConfig, loadScript);

                                    const loadTime = performance.now() - startTime;
                                    performanceMetrics.scriptsLoaded++;
                                    performanceMetrics.totalLoadTime += loadTime;

                                    console.debug(`[APEX] ✓ ${provider.name} initialized (${loadTime.toFixed(2)}ms)`);
                                } catch (error) {
                                    performanceMetrics.scriptsFailed++;
                                    console.warn(`[APEX] ✗ Failed to initialize ${provider.name}:`, error);
                                }
                            };

                            if (shouldLazyLoad && priority !== 'critical') {
                                runWhenIdle(initProvider, {
                                    priority: priority,
                                    timeout: priority === 'high' ? 1000 : 3000
                                });
                            } else {
                                // Critical scripts load immediately
                                initProvider();
                            }
                        }
                    }
                });
            });
        }, stackDelay);
    });

    // Performance reporting
    setTimeout(() => {
        const totalTime = performance.now() - performanceMetrics.startTime;
        console.log(`[APEX] Integration initialization complete:`, {
            totalTime: `${totalTime.toFixed(2)}ms`,
            scriptsLoaded: performanceMetrics.scriptsLoaded,
            scriptsFailed: performanceMetrics.scriptsFailed,
            averageLoadTime: performanceMetrics.scriptsLoaded > 0
                ? `${(performanceMetrics.totalLoadTime / performanceMetrics.scriptsLoaded).toFixed(2)}ms`
                : '0ms'
        });
    }, 5000);
}

export { monetization, tracking, engagement, communication, utility, baas };
