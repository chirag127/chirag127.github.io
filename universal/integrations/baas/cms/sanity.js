/**
 * BaaS Provider: sanity
 * Category: cms
 */

export const name = 'sanity';
export const configKey = 'sanity';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing cms/sanity');

    // Load Sanity Client (UMD)
    loadScript('https://unpkg.com/@sanity/client/dist/index.umd.js', 'sanity-sdk')
        .then(() => {
            if (window.SanityClient) {
                window.sanityClient = window.SanityClient({
                    projectId: config.projectId,
                    dataset: config.dataset,
                    useCdn: true,
                    apiVersion: '2023-05-03'
                });
                console.log('[BaaS] Sanity client ready as window.sanityClient');
            }
        });
}
