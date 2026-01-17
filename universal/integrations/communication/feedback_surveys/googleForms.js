/**
 * Google Forms Integration
 */
export const googleForms = {
    loaded: false,

    init(config) {
        if (!config.enabled || this.loaded) return;

        this.formUrl = config.formUrl;
        this.loaded = true;
        console.log('[GoogleForms] Ready');
    },

    embed(containerId, formUrl, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const url = formUrl || this.formUrl;
        if (!url) return;

        container.innerHTML = `
            <iframe src="${url}?embedded=true"
                    width="${options.width || '100%'}"
                    height="${options.height || '600'}"
                    frameborder="0"
                    marginheight="0"
                    marginwidth="0"
                    style="border:none;">
                Loading…
            </iframe>
        `;
    }
};
