/**
 * AddToAny Social Sharing Provider
 * @module engagement/addtoany
 */

export const name = 'addtoany';
export const configKey = 'addToAny';

export function init(config, loadScript) {
    if (!config.enabled) return;

    // Create floating share buttons
    const container = document.createElement('div');
    container.className = 'a2a_kit a2a_kit_size_32 a2a_floating_style a2a_vertical_style';
    container.style.cssText = 'right:0;top:150px;';
    container.innerHTML = `
        <a class="a2a_button_facebook"></a>
        <a class="a2a_button_twitter"></a>
        <a class="a2a_button_whatsapp"></a>
        <a class="a2a_button_linkedin"></a>
        <a class="a2a_button_reddit"></a>
    `;
    document.body.appendChild(container);

    loadScript('https://static.addtoany.com/menu/page.js');
}
