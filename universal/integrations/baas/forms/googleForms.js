/**
 * BaaS Provider: googleForms
 * Category: forms
 */

export const name = 'googleForms';
export const configKey = 'googleForms';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing forms/googleForms');

    // Google Forms are typically embedded via iframe.
    // Helper to inject iframe into a container
    window.googleForms = {
        embed: (containerId, formUrl) => {
            const container = document.getElementById(containerId);
            if (!container) return console.warn('[BaaS] Google Forms container not found:', containerId);

            const iframe = document.createElement('iframe');
            iframe.src = formUrl;
            iframe.width = "100%";
            iframe.height = "100%";
            iframe.frameBorder = "0";
            iframe.marginHeight = "0";
            iframe.marginWidth = "0";
            iframe.textContent = "Loading...";

            container.innerHTML = '';
            container.appendChild(iframe);
        }
    };
}
