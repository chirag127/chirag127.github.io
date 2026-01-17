/**
 * Ouo.io URL Shortener Integration
 */
export const ouoio = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.apiToken || this.loaded) return;

        this.apiToken = config.apiToken;
        this.loaded = true;
        console.log('[Ouo.io] Ready');
    },

    async shorten(url) {
        if (!this.apiToken) return url;

        try {
            const response = await fetch(`https://ouo.io/api/${this.apiToken}?s=${encodeURIComponent(url)}`);
            const shortUrl = await response.text();
            return shortUrl || url;
        } catch (error) {
            console.error('[Ouo.io] Error:', error);
            return url;
        }
    },

    wrapLinks(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const links = container.querySelectorAll('a[href^="http"]');
        links.forEach(async (link) => {
            const originalHref = link.href;
            const shortUrl = await this.shorten(originalHref);
            link.href = shortUrl;
        });
    }
};
