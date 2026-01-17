/**
 * NowPayments Crypto Gateway Provider
 * @module ads/nowpayments
 */

export const name = 'nowpayments';
export const configKey = 'nowpayments';

export function init(config, loadScript) {
    if (!config.apiKey || !config.enabled) return;

    // Create crypto donate button
    const container = document.createElement('div');
    container.id = 'nowpayments-container';
    container.style.cssText = 'position:fixed;bottom:200px;right:20px;z-index:9999;';
    container.innerHTML = `
        <a href="https://nowpayments.io/donation?api_key=${config.apiKey}" target="_blank" style="background:#00c26f;color:white;padding:10px 20px;border-radius:8px;text-decoration:none;display:flex;align-items:center;gap:8px;font-family:sans-serif;font-size:14px;">
            <span>💰</span> Donate Crypto
        </a>
    `;
    document.body.appendChild(container);
}
