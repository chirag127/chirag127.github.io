/**
 * Umami Analytics Provider
 * @module analytics/umami
 */

export const name = 'umami';
export const configKey = 'umami';

export function init(config, loadScript) {
    if (!config.id || !config.host) return;

    const s = document.createElement('script');
    s.async = true;
    s.defer = true;
    s.dataset.websiteId = config.id;
    s.src = config.host.endsWith('.js') ? config.host : `${config.host}/script.js`;
    document.head.appendChild(s);
}
