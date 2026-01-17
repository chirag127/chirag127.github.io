/**
 * GraphComment Integration
 */
export const graphcomment = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.websiteId || this.loaded) return;

        window.gc_params = {
            graphcomment_id: config.websiteId,
            fixed_header_height: 0
        };

        const script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://graphcomment.com/js/integration.js';
        document.head.appendChild(script);

        this.loaded = true;
        console.log('[GraphComment] Loaded:', config.websiteId);
    },

    render(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.id = 'graphcomment';
    }
};
