/**
 * Honeybadger Error Monitoring Provider
 * @module monitoring/honeybadger
 */

export const name = 'honeybadger';
export const configKey = 'honeybadger';

export function init(config, loadScript) {
    if (!config.key && !config.apiKey) return;

    const apiKey = config.key || config.apiKey;

    loadScript('//js.honeybadger.io/v3.2/honeybadger.min.js')
        .then(() => {
            if (window.Honeybadger) {
                Honeybadger.configure({ apiKey: apiKey });
            }
        });
}
