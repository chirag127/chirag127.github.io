/**
 * BaaS Provider: contentful
 * Category: cms
 */

export const name = 'contentful';
export const configKey = 'contentful';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing cms/contentful');

    // Load Contentful CDN SDK
    loadScript('https://cdn.jsdelivr.net/npm/contentful@latest/dist/contentful.browser.min.js', 'contentful-sdk')
        .then(() => {
            if (window.contentful) {
                window.contentfulClient = window.contentful.createClient({
                    space: config.spaceId,
                    accessToken: config.accessToken
                });
                console.log('[BaaS] Contentful client ready as window.contentfulClient');
            }
        });
}
