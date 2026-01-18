/**
 * BaaS Provider: googleForms
 * Category: forms
 */

export const name = 'googleForms';
export const configKey = 'googleForms';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing forms/googleForms');

    // Implementation placeholder for googleForms
    // const { ...credentials } = config;
}
