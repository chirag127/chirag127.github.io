/**
 * GrowthBook Official SDK Client
 * Handles initialization of the official SDK for visual experiments.
 * @module integrations/engagement/ab_testing/growthbook_client
 */

import { runVisualExperiments } from './experiments.js';

export const name = 'growthbook_client';
export const configKey = 'growthbook'; // Uses the same config key

export async function init(config, loadScript) {
    if (!config.enabled || !config.clientKey) return;

    console.log('[APEX GrowthBook] Initializing Official SDK...');

    // Load the official auto-loading script
    // This script automatically creates window.growthbook
    await loadScript('https://cdn.jsdelivr.net/npm/@growthbook/growthbook/dist/bundles/auto.min.js', 'growthbook-sdk');

    const waitForGrowthBook = () => {
        return new Promise((resolve) => {
            if (window.growthbook) {
                resolve(window.growthbook);
            } else {
                let retries = 0;
                const checkInterval = setInterval(() => {
                    retries++;
                    if (window.growthbook) {
                        clearInterval(checkInterval);
                        resolve(window.growthbook);
                    } else if (retries > 50) { // 5 seconds timeout
                        clearInterval(checkInterval);
                        console.warn('[APEX GrowthBook] SDK timeout');
                        resolve(null);
                    }
                }, 100);
            }
        });
    };

    const gb = await waitForGrowthBook();

    if (gb) {
        gb.init({
            apiHost: config.apiHost || "https://cdn.growthbook.io",
            clientKey: config.clientKey,
            enableDevMode: config.enableDevMode || false,
            trackingCallback: (experiment, result) => {
                console.log('[APEX GrowthBook] View', experiment.key, result.variationId);
                // Dispatch event for analytics
                if (window.gtag) {
                    window.gtag('event', 'ab_test_view', {
                         experiment_id: experiment.key,
                         variant_id: result.variationId
                    });
                }
            }
        }).then(() => {
            console.log('[APEX GrowthBook] SDK Ready');

            // Set user attributes
            const attrs = {
                id: localStorage.getItem('gb_visitor_id') || 'gen_' + Math.random().toString(36).substr(2, 9),
                url: window.location.pathname,
                userAgent: navigator.userAgent,
                device: /Mobile/.test(navigator.userAgent) ? 'mobile' : 'desktop'
            };

            gb.setAttributes(attrs);

            // Run visual experiments
            runVisualExperiments(gb);
        });
    }
}
