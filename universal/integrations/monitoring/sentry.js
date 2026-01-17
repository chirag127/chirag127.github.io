/**
 * Sentry Error Monitoring Provider
 * @module monitoring/sentry
 */

export const name = 'sentry';
export const configKey = 'sentry';

export function init(config, loadScript) {
    if (!config.dsn) return;

    // Extract project key from DSN for loader script
    const dsnMatch = config.dsn.match(/https:\/\/([^@]+)@/);
    const projectKey = dsnMatch ? dsnMatch[1] : null;

    if (projectKey) {
        loadScript(`https://js.sentry-cdn.com/${projectKey}.min.js`)
            .then(() => {
                if (window.Sentry) {
                    Sentry.init({ dsn: config.dsn });
                }
            });
    } else {
        // Fallback to bundle
        loadScript('https://browser.sentry-cdn.com/7.54.0/bundle.min.js')
            .then(() => {
                if (window.Sentry) {
                    Sentry.init({ dsn: config.dsn });
                }
            });
    }
}
