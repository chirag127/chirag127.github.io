/**
 * Sumo Popup Integration
 */
export const sumo = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.siteId || this.loaded) return;

        window.sumoSiteId = config.siteId;

        const script = document.createElement('script');
        script.src = 'https://load.sumo.com/';
        script.async = true;
        script.dataset.sumoSiteId = config.siteId;
        document.head.appendChild(script);

        this.loaded = true;
        console.log('[Sumo] Loaded');
    }
};
