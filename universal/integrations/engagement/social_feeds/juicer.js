/**
 * Juicer Social Aggregator Integration
 */
export const juicer = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.feedId || this.loaded) return;

        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://assets.juicer.io/embed.css';
        document.head.appendChild(link);

        const script = document.createElement('script');
        script.src = 'https://assets.juicer.io/embed.js';
        document.head.appendChild(script);

        this.feedId = config.feedId;
        this.loaded = true;
        console.log('[Juicer] Loaded');
    },

    render(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `<ul class="juicer-feed" data-feed-id="${this.feedId}"></ul>`;
    }
};
