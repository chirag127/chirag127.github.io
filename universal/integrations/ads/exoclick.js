/**
 * ExoClick Pop-Under Provider
 * @module ads/exoclick
 */

export const name = 'exoclick';
export const configKey = 'exoclick';

export function init(config, loadScript) {
    if (!config.publisherId || !config.enabled) return;

    const lastPop = localStorage.getItem('exoclick_last');
    const now = Date.now();
    if (lastPop && (now - parseInt(lastPop)) < 86400000) return;

    loadScript(`//a.exoclick.com/tag.js?pid=${config.publisherId}&z=${config.zoneId || ''}`);
    localStorage.setItem('exoclick_last', now.toString());
}
