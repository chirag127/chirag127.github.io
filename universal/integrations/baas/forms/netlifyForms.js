/**
 * BaaS Provider: netlifyForms
 * Category: forms
 */

export const name = 'netlifyForms';
export const configKey = 'netlifyForms';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing forms/netlifyForms');

    // Implementation placeholder for netlifyForms
    // const { ...credentials } = config;
}
