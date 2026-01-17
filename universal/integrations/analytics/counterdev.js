/**
 * Counter.dev Analytics Provider
 * @module analytics/counterdev
 */

export const name = 'counterdev';
export const configKey = 'counter_dev';

export function init(config, loadScript) {
    if (!config.id) return;

    const s = document.createElement('script');
    s.src = "https://cdn.counter.dev/script.js";
    s.dataset.id = config.id;
    s.dataset.utcoffset = config.offset || "0";
    document.body.appendChild(s);
}
