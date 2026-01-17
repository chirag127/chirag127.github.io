/**
 * Google Programmable Search Engine Integration
 */
export const googleSearch = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.cx || this.loaded) return;

        window.__gcse = {
            parsetags: 'onload',
            callback: () => {
                this.ready = true;
                console.log('[GoogleSearch] Ready');
            }
        };

        const script = document.createElement('script');
        script.src = `https://cse.google.com/cse.js?cx=${config.cx}`;
        script.async = true;
        document.head.appendChild(script);

        this.cx = config.cx;
        this.loaded = true;
    },

    render(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `<div class="gcse-search"></div>`;
    },

    renderSearchBox(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `<div class="gcse-searchbox"></div>`;
    },

    renderSearchResults(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `<div class="gcse-searchresults"></div>`;
    }
};
