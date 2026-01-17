/**
 * TrafficForce Pop-Under Provider
 * @module ads/trafficforce
 */

export const name = 'trafficforce';
export const configKey = 'trafficforce';

export function init(config, loadScript) {
    if (!config.publisherId || !config.enabled) return;

    const lastPop = localStorage.getItem('trafficforce_last');
    const now = Date.now();
    if (lastPop && (now - parseInt(lastPop)) < 86400000) return;

    loadScript(`//a.trafficforce.com/tag.js?id=${config.publisherId}`);
    localStorage.setItem('trafficforce_last', now.toString());
}
