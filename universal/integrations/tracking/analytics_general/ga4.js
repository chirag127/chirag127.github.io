/**
 * Google Analytics 4 Provider
 * @module analytics/ga4
 */

export const name = 'ga4';
export const configKey = 'ga4';

export function init(config, loadScript) {
    if (!config.id) return;

    loadScript(`https://www.googletagmanager.com/gtag/js?id=${config.id}`)
        .then(() => {
            window.dataLayer = window.dataLayer || [];
            function gtag() { dataLayer.push(arguments); }
            window.gtag = gtag;
            gtag('js', new Date());
            gtag('config', config.id);
        });
}
