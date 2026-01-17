/**
 * LogRocket Session Replay Provider
 * @module analytics/logrocket
 */

export const name = 'logrocket';
export const configKey = 'logrocket';

export function init(config, loadScript) {
    if (!config.id) return;

    loadScript('https://cdn.lr-in.com/LogRocket.min.js')
        .then(() => {
            if (window.LogRocket) {
                window.LogRocket.init(config.id);
            }
        });
}
