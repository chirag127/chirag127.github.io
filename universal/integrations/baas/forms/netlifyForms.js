/**
 * BaaS Provider: netlifyForms
 * Category: forms
 */

export const name = 'netlifyForms';
export const configKey = 'netlifyForms';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing forms/netlifyForms');

    // Netlify Forms are static - usually handled at build time by parsing HTML.
    // However, for SPA or dynamic forms, we can submit to any helper path or "/" with hidden field.

    // Helper to submit via AJAX
    window.netlifyForms = {
        submit: async (formName, data) => {
            const body = new URLSearchParams(data);
            body.append('form-name', formName);

            const res = await fetch('/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: body.toString()
            });
            return res;
        }
    };
}
