/**
 * Ionicons Integration
 */
export const ionicons = {
    loaded: false,

    init(config) {
        if (!config.enabled || this.loaded) return;

        const script = document.createElement('script');
        script.type = 'module';
        script.src = 'https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.esm.js';
        document.head.appendChild(script);

        const scriptNoModule = document.createElement('script');
        scriptNoModule.noModule = true;
        scriptNoModule.src = 'https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.js';
        document.head.appendChild(scriptNoModule);

        this.loaded = true;
        console.log('[Ionicons] Loaded');
    }
};
