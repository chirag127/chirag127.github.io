/**
 * Clerk Integration
 */
export const clerk = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.publishableKey || this.loaded) return;

        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/@clerk/clerk-js@4/dist/clerk.browser.js';
        script.crossOrigin = 'anonymous';
        script.dataset.clerkPublishableKey = config.publishableKey;
        script.onload = async () => {
            await window.Clerk.load();
            this.ready = true;
            console.log('[Clerk] Ready');
        };
        document.head.appendChild(script);

        this.loaded = true;
    },

    mountSignIn(containerId) {
        const container = document.getElementById(containerId);
        if (!container || !window.Clerk) return;
        window.Clerk.mountSignIn(container);
    },

    mountSignUp(containerId) {
        const container = document.getElementById(containerId);
        if (!container || !window.Clerk) return;
        window.Clerk.mountSignUp(container);
    },

    async signOut() {
        if (!window.Clerk) return;
        return window.Clerk.signOut();
    },

    getUser() {
        return window.Clerk ? window.Clerk.user : null;
    }
};
