/**
 * GPlinks URL Shortener Integration
 */
export const gplinks = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.apiKey || this.loaded) return;

        this.apiKey = config.apiKey;
        this.loaded = true;
        console.log('[GPlinks] Ready');
    },

    async shorten(url) {
        if (!this.apiKey) return url;

        try {
            const response = await fetch(`https://gplinks.com/api?api=${this.apiKey}&url=${encodeURIComponent(url)}`);
            const data = await response.json();
            return data.shortenedUrl || url;
        } catch (error) {
            console.error('[GPlinks] Error:', error);
            return url;
        }
    }
};
