/**
 * BaaS Provider: emailjs
 * Category: email
 */

export const name = 'emailjs';
export const configKey = 'emailjs';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing email/emailjs');

    loadScript('https://cdn.jsdelivr.net/npm/@emailjs/browser@3/dist/email.min.js', 'emailjs-sdk')
        .then(() => {
            if (window.emailjs) {
                window.emailjs.init(config.publicKey);
                console.log('[BaaS] EmailJS initialized');
            }
        });
}
