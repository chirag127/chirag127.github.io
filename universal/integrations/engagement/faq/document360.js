/**
 * Document360 Knowledge Base Integration
 */
export const document360 = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.projectId || this.loaded) return;

        this.projectId = config.projectId;
        this.loaded = true;
        console.log('[Document360] Ready');
    },

    embed(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <iframe src="https://${this.projectId}.document360.io/"
                    style="width:100%;height:600px;border:none;">
            </iframe>
        `;
    }
};
