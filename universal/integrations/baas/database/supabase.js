/**
 * BaaS Provider: supabase
 * Category: database
 */

export const name = 'supabase';
export const configKey = 'supabase';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing database/supabase');

    loadScript('https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2', 'supabase-js')
        .then(() => {
            if (window.supabase) {
                const { createClient } = window.supabase;
                window.supabaseClient = createClient(config.url, config.anonKey);
                console.log('[BaaS] Supabase ready as window.supabaseClient');
            }
        });
}
