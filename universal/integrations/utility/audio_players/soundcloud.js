/**
 * SoundCloud Embed Integration
 */
export const soundcloud = {
    loaded: false,

    init(config) {
        if (!config.enabled || this.loaded) return;
        this.loaded = true;
        console.log('[SoundCloud] Ready');
    },

    embed(containerId, trackUrl, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const height = options.height || 166;
        const color = options.color || 'ff5500';

        container.innerHTML = `
            <iframe width="100%" height="${height}" scrolling="no" frameborder="no"
                    src="https://w.soundcloud.com/player/?url=${encodeURIComponent(trackUrl)}&color=%23${color}&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false">
            </iframe>
        `;
    }
};
