/**
 * RafflePress Integration
 */
export const rafflepress = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.widgetId || this.loaded) return;
        this.widgetId = config.widgetId;
        this.loaded = true;
        console.log('[RafflePress] Ready');
    },

    embed(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `<div id="rafflepress-${this.widgetId}"></div>`;
    }
};
