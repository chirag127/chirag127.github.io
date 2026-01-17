/**
 * hCaptcha Provider (Earns tokens!)
 * @module utility/hcaptcha
 */

export const name = 'hcaptcha';
export const configKey = 'hcaptcha';

export function init(config, loadScript) {
    if (!config.siteKey || !config.enabled) return;

    loadScript('https://js.hcaptcha.com/1/api.js');
}
