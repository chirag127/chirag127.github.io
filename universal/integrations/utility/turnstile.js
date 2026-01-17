/**
 * Cloudflare Turnstile Provider
 * @module utility/turnstile
 */

export const name = 'turnstile';
export const configKey = 'turnstile';

export function init(config, loadScript) {
    if (!config.siteKey || !config.enabled) return;

    loadScript('https://challenges.cloudflare.com/turnstile/v0/api.js');
}
