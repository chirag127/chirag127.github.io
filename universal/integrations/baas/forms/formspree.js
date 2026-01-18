/**
 * BaaS Provider: formspree
 * Category: forms
 */

export const name = 'formspree';
export const configKey = 'formspree';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing forms/formspree');

    // Implementation placeholder for formspree
    // const { ...credentials } = config;
}
