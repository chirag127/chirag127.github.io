/**
 * Wistia Player Integration
 */
export const wistia = {
    loaded: false,

    init(config) {
        if (!config.enabled || this.loaded) return;

        const script = document.createElement('script');
        script.src = 'https://fast.wistia.com/assets/external/E-v1.js';
        script.async = true;
        document.head.appendChild(script);

        this.loaded = true;
        console.log('[Wistia] Loaded');
    },

    embed(containerId, videoId, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="wistia_embed wistia_async_${videoId}"
                 style="height:${options.height || '360px'};width:${options.width || '100%'}">
            </div>
        `;
    }
};
