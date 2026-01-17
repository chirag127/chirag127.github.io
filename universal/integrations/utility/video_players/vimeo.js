/**
 * Vimeo Player Integration
 */
export const vimeo = {
    loaded: false,
    players: {},

    init(config) {
        if (!config.enabled || this.loaded) return;

        const script = document.createElement('script');
        script.src = 'https://player.vimeo.com/api/player.js';
        script.onload = () => {
            this.ready = true;
            console.log('[Vimeo] API Ready');
        };
        document.head.appendChild(script);

        this.loaded = true;
    },

    createPlayer(containerId, videoId, options = {}) {
        if (!this.ready || !window.Vimeo) return null;

        const container = document.getElementById(containerId);
        if (!container) return null;

        this.players[containerId] = new window.Vimeo.Player(container, {
            id: videoId,
            width: options.width || '100%',
            autopause: options.autopause !== false,
            autoplay: options.autoplay || false,
            loop: options.loop || false,
            muted: options.muted || false,
            ...options
        });

        return this.players[containerId];
    },

    getPlayer(containerId) {
        return this.players[containerId];
    }
};
