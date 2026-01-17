/**
 * GlitchTip Error Monitoring Provider (Sentry-compatible)
 * @module monitoring/glitchtip
 */

export const name = 'glitchtip';
export const configKey = 'glitchtip';

export function init(config, loadScript) {
    if (!config.dsn) return;

    // GlitchTip is Sentry-compatible, use Sentry SDK
    loadScript('https://browser.sentry-cdn.com/7.54.0/bundle.min.js')
        .then(() => {
            if (window.Sentry) {
                Sentry.init({ dsn: config.dsn });
            }
        });
}
