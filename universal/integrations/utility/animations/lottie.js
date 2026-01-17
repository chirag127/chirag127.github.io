/**
 * LottieFiles Animation Integration
 */
export const lottie = {
    loaded: false,

    init(config) {
        if (!config.enabled || this.loaded) return;

        const script = document.createElement('script');
        script.src = 'https://unpkg.com/@dotlottie/player-component@1/dist/dotlottie-player.js';
        script.type = 'module';
        document.head.appendChild(script);

        this.loaded = true;
        console.log('[Lottie] Loaded');
    },

    play(containerId, animationUrl, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <dotlottie-player
                src="${animationUrl}"
                background="transparent"
                speed="${options.speed || 1}"
                style="width:${options.width || '300px'};height:${options.height || '300px'}"
                ${options.loop !== false ? 'loop' : ''}
                ${options.autoplay !== false ? 'autoplay' : ''}>
            </dotlottie-player>
        `;
    }
};
