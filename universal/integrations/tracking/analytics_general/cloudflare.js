/**
 * Cloudflare Web Analytics Provider
 * @module analytics/cloudflare
 */

export const name = 'cloudflare';
export const configKey = 'cloudflare';

export function init(config, loadScript) {
    if (!config.token) return;

    const s = document.createElement('script');
    s.defer = true;
    s.src = 'https://static.cloudflareinsights.com/beacon.min.js';
    s.dataset.cfBeacon = JSON.stringify({ token: config.token });
    document.body.appendChild(s);
}
