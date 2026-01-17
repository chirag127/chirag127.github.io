/**
 * Algolia Search Integration
 */
export const algolia = {
    loaded: false,
    client: null,
    index: null,

    init(config) {
        if (!config.enabled || !config.appId || !config.searchKey || this.loaded) return;

        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/algoliasearch@4/dist/algoliasearch-lite.umd.js';
        script.onload = () => {
            this.client = window.algoliasearch(config.appId, config.searchKey);
            if (config.indexName) {
                this.index = this.client.initIndex(config.indexName);
            }
            this.ready = true;
            console.log('[Algolia] Ready:', config.appId);
        };
        document.head.appendChild(script);

        this.loaded = true;
    },

    async search(query, options = {}) {
        if (!this.index) return { hits: [] };

        try {
            return await this.index.search(query, {
                hitsPerPage: options.limit || 10,
                ...options
            });
        } catch (error) {
            console.error('[Algolia] Search error:', error);
            return { hits: [] };
        }
    }
};
