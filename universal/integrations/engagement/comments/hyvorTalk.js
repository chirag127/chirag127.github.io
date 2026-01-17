/**
 * Hyvor Talk Comments Integration
 */
export const hyvorTalk = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.websiteId || this.loaded) return;

        this.websiteId = config.websiteId;

        const script = document.createElement('script');
        script.src = 'https://talk.hyvor.com/embed/embed.js';
        script.type = 'module';
        document.head.appendChild(script);

        this.loaded = true;
        console.log('[HyvorTalk] Loaded:', config.websiteId);
    },

    render(containerId, pageId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `<hyvor-talk-comments website-id="${this.websiteId}" page-id="${pageId || window.location.pathname}"></hyvor-talk-comments>`;
    }
};
