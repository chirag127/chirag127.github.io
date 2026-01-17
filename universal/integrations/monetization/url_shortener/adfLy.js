/**
 * Adf.ly / Linkvertise URL Shortener Integration
 */
export const adfLy = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.userId || this.loaded) return;

        this.userId = config.userId;
        this.loaded = true;
        console.log('[Adf.ly] Ready');
    },

    async shorten(url, options = {}) {
        if (!this.userId) return url;

        try {
            const domain = options.domain || 'adf.ly';
            const adType = options.adType || 1; // 1 = interstitial, 2 = banner
            const response = await fetch(`https://api.adf.ly/v1/shorten?key=${this.apiKey}&user_id=${this.userId}&domain=${domain}&advert_type=${adType}&url=${encodeURIComponent(url)}`);
            const data = await response.json();
            return data.data?.[0]?.short_url || url;
        } catch (error) {
            console.error('[Adf.ly] Error:', error);
            return url;
        }
    }
};
