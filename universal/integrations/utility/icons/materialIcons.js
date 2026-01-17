/**
 * Material Icons Integration
 */
export const materialIcons = {
    loaded: false,

    init(config) {
        if (!config.enabled || this.loaded) return;

        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://fonts.googleapis.com/icon?family=Material+Icons|Material+Icons+Outlined|Material+Icons+Round';
        document.head.appendChild(link);

        this.loaded = true;
        console.log('[MaterialIcons] Loaded');
    }
};
