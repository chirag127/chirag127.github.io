/**
 * ShrinkEarn URL Shortener Integration
 */
export const shrinkEarn = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.apiKey || this.loaded) return;

        this.apiKey = config.apiKey;
        this.loaded = true;
        console.log('[ShrinkEarn] Ready');
    },

    async shorten(url) {
        if (!this.apiKey) return url;

        try {
            const response = await fetch(`https://shrinkearn.com/api?api=${this.apiKey}&url=${encodeURIComponent(url)}`);
            const data = await response.json();
            return data.shortenedUrl || url;
        } catch (error) {
            console.error('[ShrinkEarn] Error:', error);
            return url;
        }
    }
};
