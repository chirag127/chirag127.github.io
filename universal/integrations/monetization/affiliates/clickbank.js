/**
 * ClickBank Affiliate Integration
 */
export const clickbank = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.nickname || this.loaded) return;

        this.nickname = config.nickname;
        this.loaded = true;
        console.log('[ClickBank] Ready:', config.nickname);
    },

    createHopLink(vendor, tid) {
        const tidParam = tid ? `&tid=${tid}` : '';
        return `https://${this.nickname}.${vendor}.hop.clickbank.net/${tidParam}`;
    },

    render(containerId, vendor, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <a href="${this.createHopLink(vendor, options.tid)}"
               target="_blank"
               rel="nofollow noopener"
               style="display:inline-block;padding:12px 24px;background:${options.bgColor || '#28a745'};color:#fff;text-decoration:none;border-radius:6px;font-weight:bold;">
                ${options.text || 'Get It Now'}
            </a>
        `;
    }
};
