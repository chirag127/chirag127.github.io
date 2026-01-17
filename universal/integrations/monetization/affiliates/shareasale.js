/**
 * ShareASale Affiliate Integration
 */
export const shareasale = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.affiliateId || this.loaded) return;

        this.affiliateId = config.affiliateId;
        this.loaded = true;
        console.log('[ShareASale] Ready:', config.affiliateId);
    },

    createLink(merchantId, urlId, options = {}) {
        return `https://www.shareasale.com/r.cfm?b=${urlId}&u=${this.affiliateId}&m=${merchantId}`;
    },

    loadBanner(containerId, merchantId, bannerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <a target="_blank" href="https://www.shareasale.com/r.cfm?b=${bannerId}&u=${this.affiliateId}&m=${merchantId}&urllink=&afftrack=">
                <img src="https://www.shareasale.com/image/${merchantId}/${bannerId}.gif" border="0" alt="affiliate banner"/>
            </a>
        `;
    }
};
