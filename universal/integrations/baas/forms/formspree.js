/**
 * BaaS Provider: formspree
 * Category: forms
 */

export const name = 'formspree';
export const configKey = 'formspree';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing forms/formspree');

    // Auto-configure forms marked for Formspree
    if (config.formId) {
        const forms = document.querySelectorAll('form[data-provider="formspree"]');
        forms.forEach(form => {
            form.action = `https://formspree.io/f/${config.formId}`;
            form.method = 'POST';
        });
    }

    // Expose helper
    window.formspree = {
        submit: async (data) => {
             if (!config.formId) return console.error('[BaaS] Formspree formId missing');
             const res = await fetch(`https://formspree.io/f/${config.formId}`, {
                 method: 'POST',
                 headers: { 'Content-Type': 'application/json' },
                 body: JSON.stringify(data)
             });
             return res.json();
        }
    };
}
