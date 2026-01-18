/**
 * BaaS Provider: strapi
 * Category: cms
 */

export const name = 'strapi';
export const configKey = 'strapi';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing cms/strapi');

    // Strapi is REST/GraphQL based, widely uses fetch.
    // We expose a helper client.
    window.strapiClient = {
        baseUrl: config.apiUrl || 'http://localhost:1337',
        find: async (collection, params = {}) => {
            const url = new URL(`${config.apiUrl}/api/${collection}`);
            Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
            const res = await fetch(url.toString());
            return res.json();
        },
        findOne: async (collection, id) => {
            const res = await fetch(`${config.apiUrl}/api/${collection}/${id}`);
            return res.json();
        }
    };
    console.log('[BaaS] Strapi helper ready as window.strapiClient');
}
