/**
 * Amplitude Analytics Provider
 * @module analytics/amplitude
 */

export const name = 'amplitude';
export const configKey = 'amplitude';

export function init(config, loadScript) {
    if (!config.key && !config.apiKey) return;

    const apiKey = config.key || config.apiKey;

    loadScript('https://cdn.amplitude.com/libs/amplitude-8.17.0-min.gz.js')
        .then(() => {
            if (window.amplitude) {
                window.amplitude.getInstance().init(apiKey);
            }
        });
}
