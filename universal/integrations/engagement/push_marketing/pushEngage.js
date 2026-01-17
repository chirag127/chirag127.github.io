/**
 * PushEngage Integration
 */
export const pushEngage = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.siteId || this.loaded) return;

        window._peq = window._peq || [];

        const script = document.createElement('script');
        script.src = `https://clientcdn.pushengage.com/core/${config.siteId}.js`;
        script.async = true;
        document.head.appendChild(script);

        this.loaded = true;
        console.log('[PushEngage] Loaded:', config.siteId);
    },

    subscribe() {
        if (window._peq) {
            window._peq.push(['init']);
        }
    }
};
