/**
 * MagicBell Notification Integration
 */
export const magicbell = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.apiKey || this.loaded) return;

        const script = document.createElement('script');
        script.src = 'https://assets.magicbell.com/magicbell-embedded.min.js';
        script.async = true;
        document.head.appendChild(script);

        this.apiKey = config.apiKey;
        this.userExternalId = config.userExternalId;
        this.loaded = true;
        console.log('[MagicBell] Loaded');
    },

    render(containerId) {
        const container = document.getElementById(containerId);
        if (!container || !window.MagicBell) return;

        window.MagicBell.Widget.initialize({
            apiKey: this.apiKey,
            userExternalId: this.userExternalId,
            target: container
        });
    }
};
