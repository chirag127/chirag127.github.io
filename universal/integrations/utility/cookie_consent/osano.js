/**
 * Osano Cookie Consent Integration
 */
export const osano = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.scriptUrl || this.loaded) return;

        const script = document.createElement('script');
        script.src = config.scriptUrl;
        script.async = true;
        document.head.appendChild(script);

        this.loaded = true;
        console.log('[Osano] Loaded');
    }
};
