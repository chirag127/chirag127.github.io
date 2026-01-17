/**
 * IPinfo Geolocation Integration
 */
export const ipinfo = {
    loaded: false,
    data: null,

    init(config) {
        if (!config.enabled || this.loaded) return;

        this.token = config.token;
        this.loaded = true;
        console.log('[IPinfo] Ready');
    },

    async getLocation() {
        if (this.data) return this.data;

        try {
            const url = this.token
                ? `https://ipinfo.io/json?token=${this.token}`
                : 'https://ipinfo.io/json';
            const response = await fetch(url);
            this.data = await response.json();
            return this.data;
        } catch (error) {
            console.error('[IPinfo] Error:', error);
            return null;
        }
    },

    async getCountry() {
        const data = await this.getLocation();
        return data?.country || null;
    },

    async getCity() {
        const data = await this.getLocation();
        return data?.city || null;
    }
};
