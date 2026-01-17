/**
 * ConvertKit Integration
 */
export const convertkit = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.formId || this.loaded) return;

        this.formId = config.formId;
        this.loaded = true;
        console.log('[ConvertKit] Ready:', config.formId);
    },

    render(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const script = document.createElement('script');
        script.src = `https://f.convertkit.com/${this.formId}/${this.formId}.js`;
        script.async = true;
        script.dataset.uid = this.formId;
        container.appendChild(script);
    }
};
