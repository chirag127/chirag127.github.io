/**
 * Weglot Translation Integration
 */
export const weglot = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.apiKey || this.loaded) return;

        window.Weglot = window.Weglot || {};

        const script = document.createElement('script');
        script.src = 'https://cdn.weglot.com/weglot.min.js';
        script.onload = () => {
            window.Weglot.initialize({
                api_key: config.apiKey,
                ...config.options
            });
            this.ready = true;
            console.log('[Weglot] Ready');
        };
        document.head.appendChild(script);

        this.loaded = true;
    },

    switchLanguage(langCode) {
        if (window.Weglot) {
            window.Weglot.switchTo(langCode);
        }
    },

    getCurrentLanguage() {
        return window.Weglot ? window.Weglot.getCurrentLang() : null;
    }
};
