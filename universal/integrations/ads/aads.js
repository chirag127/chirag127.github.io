/**
 * A-ADS (Anonymous Ads) Provider
 * Bitcoin ad network - no approval needed
 * @module ads/aads
 */

export const name = 'aads';
export const configKey = 'aads';

export function init(config, loadScript) {
    if (!config.unitId || !config.enabled) return;

    // A-ADS uses iframe embed
    const container = document.createElement('div');
    container.id = 'aads-container';
    container.innerHTML = `
        <iframe
            data-aa="${config.unitId}"
            src="//acceptable.a-ads.com/${config.unitId}?size=${config.size || '728x90'}"
            style="border:0; padding:0; width:${(config.size || '728x90').split('x')[0]}px; height:${(config.size || '728x90').split('x')[1]}px; overflow:hidden; background-color:transparent;">
        </iframe>
    `;

    // Insert after header or at top of main content
    const target = document.querySelector('main') || document.body;
    target.insertBefore(container, target.firstChild);
}
