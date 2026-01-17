/**
 * YouTube Embed Integration
 */
export const youtube = {
    loaded: false,
    players: {},

    init(config) {
        if (!config.enabled || this.loaded) return;

        window.onYouTubeIframeAPIReady = () => {
            this.ready = true;
            console.log('[YouTube] API Ready');
        };

        const script = document.createElement('script');
        script.src = 'https://www.youtube.com/iframe_api';
        const firstScript = document.getElementsByTagName('script')[0];
        firstScript.parentNode.insertBefore(script, firstScript);

        this.loaded = true;
    },

    createPlayer(containerId, videoId, options = {}) {
        if (!this.ready || !window.YT) return null;

        this.players[containerId] = new window.YT.Player(containerId, {
            videoId: videoId,
            width: options.width || '100%',
            height: options.height || 360,
            playerVars: {
                autoplay: options.autoplay ? 1 : 0,
                controls: options.controls !== false ? 1 : 0,
                modestbranding: 1,
                rel: 0,
                ...options.playerVars
            },
            events: options.events || {}
        });

        return this.players[containerId];
    },

    getPlayer(containerId) {
        return this.players[containerId];
    }
};
