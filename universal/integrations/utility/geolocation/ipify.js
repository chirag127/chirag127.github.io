/**
 * Ipify Simple IP Detection
 */
export const ipify = {
    loaded: false,

    init(config) {
        if (!config.enabled || this.loaded) return;
        this.loaded = true;
        console.log('[Ipify] Ready');
    },

    async getIP() {
        try {
            const response = await fetch('https://api.ipify.org?format=json');
            const data = await response.json();
            return data.ip;
        } catch (error) {
            console.error('[Ipify] Error:', error);
            return null;
        }
    }
};
