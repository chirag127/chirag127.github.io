/**
 * BaaS Provider: surrealdb
 * Category: database
 */

export const name = 'surrealdb';
export const configKey = 'surrealdb';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing database/surrealdb');

    // SurrealDB is often accessed via simple fetch or WebSocket
    // Providing a lightweight fetch wrapper
    window.surrealDb = {
        endpoint: config.endpoint,
        query: async (sql) => {
            if (!config.endpoint) return console.error('SurrealDB endpoint not configured');

            const res = await fetch(`${config.endpoint}/sql`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': `Basic ${btoa(config.user + ':' + config.pass)}` // Example auth if needed
                },
                body: sql
            });
            return res.json();
        }
    };
    console.log('[BaaS] SurrealDB helper ready as window.surrealDb');
}
