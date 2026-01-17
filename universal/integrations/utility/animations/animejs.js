/**
 * Anime.js Animation Integration
 */
export const animejs = {
    loaded: false,

    init(config) {
        if (!config.enabled || this.loaded) return;

        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/animejs@3.2.1/lib/anime.min.js';
        script.onload = () => {
            this.ready = true;
            console.log('[Anime.js] Ready');
        };
        document.head.appendChild(script);

        this.loaded = true;
    },

    animate(targets, properties) {
        if (!window.anime) return null;
        return window.anime({
            targets,
            ...properties
        });
    }
};
