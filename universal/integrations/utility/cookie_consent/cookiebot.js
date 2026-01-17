/**
 * Cookiebot Integration
 */
export const cookiebot = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.domainGroupId || this.loaded) return;

        const script = document.createElement('script');
        script.id = 'Cookiebot';
        script.src = 'https://consent.cookiebot.com/uc.js';
        script.dataset.cbid = config.domainGroupId;
        script.dataset.blockingmode = 'auto';
        script.type = 'text/javascript';
        script.async = true;
        document.head.appendChild(script);

        this.loaded = true;
        console.log('[Cookiebot] Loaded:', config.domainGroupId);
    },

    renew() {
        if (window.Cookiebot) {
            window.Cookiebot.renew();
        }
    },

    getConsent() {
        return window.Cookiebot ? window.Cookiebot.consent : null;
    }
};
