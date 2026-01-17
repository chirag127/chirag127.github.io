/**
 * Adobe Fonts (Typekit) Integration
 */
export const adobeFonts = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.projectId || this.loaded) return;

        const script = document.createElement('script');
        script.src = `https://use.typekit.net/${config.projectId}.js`;
        script.onload = () => {
            try {
                window.Typekit.load({ async: true });
                console.log('[AdobeFonts] Loaded:', config.projectId);
            } catch (e) {
                console.error('[AdobeFonts] Error:', e);
            }
        };
        document.head.appendChild(script);
        this.loaded = true;
    }
};
