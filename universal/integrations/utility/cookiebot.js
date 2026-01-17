/**
 * Cookiebot GDPR Consent Provider
 * @module utility/cookiebot
 */

export const name = 'cookiebot';
export const configKey = 'cookiebot';

export function init(config, loadScript) {
    if (!config.domainGroupId || !config.enabled) return;

    loadScript(`https://consent.cookiebot.com/uc.js`, {
        'data-cbid': config.domainGroupId,
        'data-blockingmode': 'auto'
    });
}
