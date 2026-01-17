/**
 * hCaptcha Integration
 */
export const hcaptcha = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.siteKey || this.loaded) return;

        const script = document.createElement('script');
        script.src = 'https://js.hcaptcha.com/1/api.js';
        script.async = true;
        script.defer = true;
        document.head.appendChild(script);

        this.siteKey = config.siteKey;
        this.loaded = true;
        console.log('[hCaptcha] Loaded');
    },

    render(containerId) {
        if (!window.hcaptcha) return null;
        return window.hcaptcha.render(containerId, {
            sitekey: this.siteKey
        });
    },

    getResponse(widgetId) {
        if (!window.hcaptcha) return null;
        return window.hcaptcha.getResponse(widgetId);
    },

    reset(widgetId) {
        if (!window.hcaptcha) return;
        window.hcaptcha.reset(widgetId);
    }
};
