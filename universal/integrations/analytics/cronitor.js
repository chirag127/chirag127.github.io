/**
 * Cronitor RUM Provider
 * @module analytics/cronitor
 */

export const name = 'cronitor';
export const configKey = 'cronitor';

export function init(config, loadScript) {
    if (!config.key && !config.id) return;

    const clientKey = config.key || config.id;

    window.cronitor = window.cronitor || function() {
        (window.cronitor.q = window.cronitor.q || []).push(arguments);
    };
    cronitor('config', { clientKey: clientKey });

    const s = document.createElement('script');
    s.src = "https://rum.cronitor.io/script.js";
    s.async = true;
    document.body.appendChild(s);
}
