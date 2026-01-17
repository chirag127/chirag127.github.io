/**
 * HelloBar Integration
 */
export const hellobar = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.scriptId || this.loaded) return;

        const script = document.createElement('script');
        script.src = `https://my.hellobar.com/${config.scriptId}.js`;
        script.type = 'text/javascript';
        script.async = true;
        document.head.appendChild(script);

        this.loaded = true;
        console.log('[HelloBar] Loaded:', config.scriptId);
    }
};
