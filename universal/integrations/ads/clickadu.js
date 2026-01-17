/**
 * ClickAdu Pop-Under Provider
 * @module ads/clickadu
 */

export const name = 'clickadu';
export const configKey = 'clickadu';

export function init(config, loadScript) {
    if (!config.siteId || !config.enabled) return;

    // Check frequency limits
    const lastPop = localStorage.getItem('clickadu_last');
    const now = Date.now();
    const minDelay = 86400 * 1000; // 24 hours

    if (lastPop && (now - parseInt(lastPop)) < minDelay) {
        return;
    }

    loadScript(`//frolisheddiede.com/tag.js?site=${config.siteId}`);
    localStorage.setItem('clickadu_last', now.toString());
}
