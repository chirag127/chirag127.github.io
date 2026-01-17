/**
 * Amazon Associates Integration
 */
export const amazon = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.trackingId || this.loaded) return;

        this.trackingId = config.trackingId;
        this.marketplace = config.marketplace || 'US';
        this.loaded = true;
        console.log('[AmazonAssociates] Ready:', config.trackingId);
    },

    createLink(asin, text = 'Buy on Amazon') {
        const domains = {
            US: 'amazon.com', UK: 'amazon.co.uk', DE: 'amazon.de',
            FR: 'amazon.fr', IT: 'amazon.it', ES: 'amazon.es',
            CA: 'amazon.ca', JP: 'amazon.co.jp', IN: 'amazon.in'
        };
        const domain = domains[this.marketplace] || domains.US;
        return `<a href="https://www.${domain}/dp/${asin}?tag=${this.trackingId}" target="_blank" rel="nofollow noopener">${text}</a>`;
    },

    loadNativeAds(containerId, keywords) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const script = document.createElement('script');
        script.type = 'text/javascript';
        script.innerHTML = `
            amzn_assoc_placement = "adunit";
            amzn_assoc_search_bar = "false";
            amzn_assoc_tracking_id = "${this.trackingId}";
            amzn_assoc_ad_mode = "search";
            amzn_assoc_ad_type = "smart";
            amzn_assoc_marketplace = "${this.marketplace.toLowerCase()}";
            amzn_assoc_region = "${this.marketplace}";
            amzn_assoc_default_search_phrase = "${keywords || ''}";
            amzn_assoc_default_category = "All";
            amzn_assoc_linkid = "";
        `;
        container.appendChild(script);

        const adScript = document.createElement('script');
        adScript.src = '//z-na.amazon-adsystem.com/widgets/onejs?MarketPlace=' + this.marketplace;
        container.appendChild(adScript);
    }
};
