/**
 * Cloudflare Turnstile Integration
 */
export const turnstile = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.siteKey || this.loaded) return;

        const script = document.createElement('script');
        script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js';
        script.async = true;
        script.defer = true;
        document.head.appendChild(script);

        this.siteKey = config.siteKey;
        this.loaded = true;
        console.log('[Turnstile] Loaded');
    },

    render(containerId, callback) {
        if (!window.turnstile) return null;
        return window.turnstile.render(`#${containerId}`, {
            sitekey: this.siteKey,
            callback: callback || ((token) => console.log('[Turnstile] Token:', token))
        });
    },

    reset(widgetId) {
        if (!window.turnstile) return;
        window.turnstile.reset(widgetId);
    },

    getResponse(widgetId) {
        if (!window.turnstile) return null;
        return window.turnstile.getResponse(widgetId);
    }
};
