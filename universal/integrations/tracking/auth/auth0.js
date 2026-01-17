/**
 * Auth0 Integration
 */
export const auth0 = {
    loaded: false,
    client: null,

    init(config) {
        if (!config.enabled || !config.domain || !config.clientId || this.loaded) return;

        const script = document.createElement('script');
        script.src = 'https://cdn.auth0.com/js/auth0-spa-js/2.0/auth0-spa-js.production.js';
        script.onload = async () => {
            this.client = await window.auth0.createAuth0Client({
                domain: config.domain,
                clientId: config.clientId,
                authorizationParams: {
                    redirect_uri: window.location.origin
                }
            });
            this.ready = true;
            console.log('[Auth0] Ready');
        };
        document.head.appendChild(script);

        this.loaded = true;
    },

    async login() {
        if (!this.client) return;
        return this.client.loginWithRedirect();
    },

    async logout() {
        if (!this.client) return;
        return this.client.logout({ logoutParams: { returnTo: window.location.origin } });
    },

    async getUser() {
        if (!this.client) return null;
        return this.client.getUser();
    },

    async isAuthenticated() {
        if (!this.client) return false;
        return this.client.isAuthenticated();
    }
};
