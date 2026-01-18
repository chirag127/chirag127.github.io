/**
 * BaaS Provider: resend
 * Category: email
 */

export const name = 'resend';
export const configKey = 'resend';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing email/resend');

    // Resend is primarily server-side. Using it client-side requires a proxy to hide the API key.
    // We expose a helper that sends to a proxy endpoint if configured, or warns about key exposure.

    window.resendClient = {
        send: async (payload) => {
            if (config.apiKey && config.apiKey.startsWith('re_')) {
                console.warn('[Security] Resend API Key found in client-side config. Do not expose this in production!');
            }

            // If user has a proxy endpoint
            const endpoint = config.proxyUrl || 'https://api.resend.com/emails';

            const headers = {
                'Content-Type': 'application/json'
            };
            if (config.apiKey) {
                headers['Authorization'] = `Bearer ${config.apiKey}`;
            }

            const res = await fetch(endpoint, {
                method: 'POST',
                headers,
                body: JSON.stringify(payload)
            });
            return res.json();
        }
    };
    console.log('[BaaS] Resend helper ready as window.resendClient');
}
