/**
 * Beam Analytics Provider
 * @module analytics/beam
 */

export const name = 'beam';
export const configKey = 'beam';

export function init(config, loadScript) {
    if (!config.token) return;

    const s = document.createElement('script');
    s.src = "https://beamanalytics.b-cdn.net/beam.min.js";
    s.dataset.token = config.token;
    s.async = true;
    document.head.appendChild(s);
}
