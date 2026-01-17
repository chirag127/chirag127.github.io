/**
 * LiberaPay Open Source Donations Provider
 * @module ads/liberapay
 */

export const name = 'liberapay';
export const configKey = 'liberapay';

export function init(config, loadScript) {
    if (!config.username || !config.enabled) return;

    const container = document.createElement('div');
    container.id = 'liberapay-container';
    container.style.cssText = 'position:fixed;bottom:140px;right:20px;z-index:9999;';
    container.innerHTML = `
        <a href="https://liberapay.com/${config.username}/donate" target="_blank">
            <img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg" style="height:36px;">
        </a>
    `;
    document.body.appendChild(container);
}
