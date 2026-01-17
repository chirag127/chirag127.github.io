/**
 * AdMaven Pop-Under Provider
 * @module ads/admaven
 */

export const name = 'admaven';
export const configKey = 'admaven';

export function init(config, loadScript) {
    if (!config.publisherId || !config.enabled) return;

    const lastPop = localStorage.getItem('admaven_last');
    const now = Date.now();
    if (lastPop && (now - parseInt(lastPop)) < 86400000) return;

    loadScript(`//go.onclasrv.com/apu.php?zoneid=${config.publisherId}`);
    localStorage.setItem('admaven_last', now.toString());
}
