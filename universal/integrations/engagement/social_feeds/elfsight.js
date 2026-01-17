/**
 * Elfsight Widget Integration
 * Embed social media feeds (Instagram, TikTok, etc.)
 */
export const elfsight = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.appId || this.loaded) return;

        const script = document.createElement('script');
        script.src = 'https://static.elfsight.com/platform/platform.js';
        script.dataset.useServiceCore = '';
        script.defer = true;
        document.head.appendChild(script);

        this.appId = config.appId;
        this.loaded = true;
        console.log('[Elfsight] Loaded');
    },

    render(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `<div class="elfsight-app-${this.appId}"></div>`;
    }
};
