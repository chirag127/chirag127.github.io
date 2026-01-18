/**
 * BaaS Provider: formsubmit
 * Category: forms
 */

export const name = 'formsubmit';
export const configKey = 'formsubmit';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing forms/formsubmit');

    // Auto-configure forms marked for Formsubmit
    if (config.email) {
        const forms = document.querySelectorAll('form[data-provider="formsubmit"]');
        forms.forEach(form => {
            form.action = `https://formsubmit.co/${config.email}`;
            form.method = 'POST';
        });
    }

    // Expose helper
    window.formsubmit = {
        getEndpoint: () => config.email ? `https://formsubmit.co/${config.email}` : null
    };
}
