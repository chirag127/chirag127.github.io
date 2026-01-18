/**
 * BaaS Provider: web3forms
 * Category: forms
 */

export const name = 'web3forms';
export const configKey = 'web3forms';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing forms/web3forms');

    // Helper to submit JSON
    window.web3forms = {
        submit: async (data) => {
            if (!config.accessKey) return console.error('[BaaS] Web3Forms accessKey missing');

            const payload = { ...data, access_key: config.accessKey };
            const res = await fetch('https://api.web3forms.com/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            return res.json();
        }
    };
}
