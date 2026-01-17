/**
 * Coinbase Commerce Crypto Payments Provider
 * @module ads/coinbase
 */

export const name = 'coinbase';
export const configKey = 'coinbaseCommerce';

export function init(config, loadScript) {
    if (!config.checkoutId || !config.enabled) return;

    // Create Coinbase Commerce button
    const container = document.createElement('div');
    container.id = 'coinbase-container';
    container.innerHTML = `
        <a class="donate-with-crypto" href="https://commerce.coinbase.com/checkout/${config.checkoutId}">
            <span>Donate with Crypto</span>
        </a>
        <script src="https://commerce.coinbase.com/v1/checkout.js?version=201807"></script>
    `;
    document.body.appendChild(container);
}
