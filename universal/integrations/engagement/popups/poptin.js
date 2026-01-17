/**
 * Poptin Popup Integration
 */
export const poptin = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.siteKey || this.loaded) return;

        const script = document.createElement('script');
        script.src = `https://cdn.popt.in/pixel.js?id=${config.siteKey}`;
        script.id = 'pixel-script-poptin';
        script.async = true;
        document.head.appendChild(script);

        this.loaded = true;
        console.log('[Poptin] Loaded');
    }
};
