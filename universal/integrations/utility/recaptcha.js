/**
 * Google reCAPTCHA v3 Provider
 * @module utility/recaptcha
 */

export const name = 'recaptcha';
export const configKey = 'recaptcha';

export function init(config, loadScript) {
    if (!config.siteKey || !config.enabled) return;

    loadScript(`https://www.google.com/recaptcha/api.js?render=${config.siteKey}`)
        .then(() => {
            window.grecaptcha.ready(function() {
                console.log('✅ reCAPTCHA ready');
            });
        });
}
