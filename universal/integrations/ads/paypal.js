/**
 * PayPal Donate Button Provider
 * @module ads/paypal
 */

export const name = 'paypal';
export const configKey = 'paypal';

export function init(config, loadScript) {
    if ((!config.email && !config.buttonId) || !config.enabled) return;

    // Create donate button container
    const container = document.createElement('div');
    container.id = 'paypal-donate-container';
    container.style.cssText = 'position:fixed;bottom:80px;right:20px;z-index:9999;';

    if (config.buttonId) {
        // Hosted button
        container.innerHTML = `
            <form action="https://www.paypal.com/donate" method="post" target="_top">
                <input type="hidden" name="hosted_button_id" value="${config.buttonId}" />
                <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" border="0" name="submit" title="Donate with PayPal" alt="Donate with PayPal button" />
            </form>
        `;
    } else if (config.email) {
        // Email-based
        container.innerHTML = `
            <form action="https://www.paypal.com/donate" method="post" target="_top">
                <input type="hidden" name="business" value="${config.email}" />
                <input type="hidden" name="currency_code" value="${config.currency || 'USD'}" />
                <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" border="0" name="submit" alt="Donate" />
            </form>
        `;
    }

    document.body.appendChild(container);
}
