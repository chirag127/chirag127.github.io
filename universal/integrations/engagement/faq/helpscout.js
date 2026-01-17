/**
 * HelpScout Beacon Integration
 */
export const helpscout = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.beaconId || this.loaded) return;

        window.Beacon = function(method, options, data) {
            window.Beacon.readyQueue.push({ method, options, data });
        };
        window.Beacon.readyQueue = [];

        const script = document.createElement('script');
        script.src = 'https://beacon-v2.helpscout.net';
        script.async = true;
        script.onload = () => {
            window.Beacon('init', config.beaconId);
        };
        document.head.appendChild(script);

        this.loaded = true;
        console.log('[HelpScout] Loaded');
    },

    open() {
        if (window.Beacon) window.Beacon('open');
    },

    toggle() {
        if (window.Beacon) window.Beacon('toggle');
    }
};
