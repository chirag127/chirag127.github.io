/**
 * Shorte.st URL Shortener Integration
 */
export const shortest = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.apiToken || this.loaded) return;

        this.apiToken = config.apiToken;
        this.loaded = true;
        console.log('[Shorte.st] Ready');
    },

    async shorten(url) {
        if (!this.apiToken) return url;

        try {
            const response = await fetch('https://api.shorte.st/v1/data/url', {
                method: 'PUT',
                headers: {
                    'public-api-token': this.apiToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ urlToShorten: url })
            });
            const data = await response.json();
            return data.shortenedUrl || url;
        } catch (error) {
            console.error('[Shorte.st] Error:', error);
            return url;
        }
    }
};
