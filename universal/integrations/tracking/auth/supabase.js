/**
 * Supabase Integration
 */
export const supabase = {
    loaded: false,
    client: null,

    init(config) {
        if (!config.enabled || !config.url || !config.anonKey || this.loaded) return;

        const script = document.createElement('script');
        script.src = 'https://unpkg.com/@supabase/supabase-js@2';
        script.onload = () => {
            this.client = window.supabase.createClient(config.url, config.anonKey);
            this.ready = true;
            console.log('[Supabase] Ready');
        };
        document.head.appendChild(script);

        this.loaded = true;
    },

    async signInWithEmail(email, password) {
        if (!this.client) return null;
        return this.client.auth.signInWithPassword({ email, password });
    },

    async signUp(email, password) {
        if (!this.client) return null;
        return this.client.auth.signUp({ email, password });
    },

    async signInWithOAuth(provider) {
        if (!this.client) return null;
        return this.client.auth.signInWithOAuth({ provider });
    },

    async signOut() {
        if (!this.client) return;
        return this.client.auth.signOut();
    },

    getSession() {
        return this.client ? this.client.auth.getSession() : null;
    }
};
