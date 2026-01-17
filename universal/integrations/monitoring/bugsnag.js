/**
 * Bugsnag Error Monitoring Provider
 * @module monitoring/bugsnag
 */

export const name = 'bugsnag';
export const configKey = 'bugsnag';

export function init(config, loadScript) {
    if (!config.key && !config.apiKey) return;

    const apiKey = config.key || config.apiKey;

    loadScript('//d2wy8f7a9ursnm.cloudfront.net/v7/bugsnag.min.js')
        .then(() => {
            if (window.Bugsnag) {
                Bugsnag.start({ apiKey: apiKey });
            }
        });
}
