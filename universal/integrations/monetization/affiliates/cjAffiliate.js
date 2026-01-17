/**
 * CJ Affiliate (Commission Junction) Integration
 */
export const cjAffiliate = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.websiteId || this.loaded) return;

        this.websiteId = config.websiteId;
        this.loaded = true;
        console.log('[CJAffiliate] Ready:', config.websiteId);
    },

    createLink(advertiserId, linkId, destination) {
        return `https://www.anrdoezrs.net/click-${this.websiteId}-${linkId}?url=${encodeURIComponent(destination)}`;
    },

    loadWidget(containerId, widgetId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const script = document.createElement('script');
        script.src = `https://www.cjwidget.com/script.js?id=${widgetId}`;
        script.async = true;
        container.appendChild(script);
    }
};
