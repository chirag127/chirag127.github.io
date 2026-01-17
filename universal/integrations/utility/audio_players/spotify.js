/**
 * Spotify Embed Integration
 */
export const spotify = {
    loaded: false,

    init(config) {
        if (!config.enabled || this.loaded) return;
        this.loaded = true;
        console.log('[Spotify] Ready');
    },

    embedTrack(containerId, trackId, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const height = options.height || 80;
        const theme = options.theme || 0;  // 0 = light, 1 = dark

        container.innerHTML = `
            <iframe src="https://open.spotify.com/embed/track/${trackId}?theme=${theme}"
                    width="100%" height="${height}" frameborder="0"
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">
            </iframe>
        `;
    },

    embedPlaylist(containerId, playlistId, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const height = options.height || 380;

        container.innerHTML = `
            <iframe src="https://open.spotify.com/embed/playlist/${playlistId}"
                    width="100%" height="${height}" frameborder="0"
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">
            </iframe>
        `;
    }
};
