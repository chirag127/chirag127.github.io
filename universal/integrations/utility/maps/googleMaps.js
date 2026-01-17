/**
 * Google Maps Integration
 */
export const googleMaps = {
    loaded: false,
    maps: {},

    init(config) {
        if (!config.enabled || !config.apiKey || this.loaded) return;

        window.initGoogleMaps = () => {
            this.ready = true;
            console.log('[GoogleMaps] Ready');
        };

        const script = document.createElement('script');
        script.src = `https://maps.googleapis.com/maps/api/js?key=${config.apiKey}&callback=initGoogleMaps`;
        script.async = true;
        script.defer = true;
        document.head.appendChild(script);

        this.loaded = true;
    },

    createMap(containerId, options = {}) {
        if (!this.ready || !window.google) return null;

        const container = document.getElementById(containerId);
        if (!container) return null;

        const map = new window.google.maps.Map(container, {
            center: { lat: options.lat || 40.7128, lng: options.lng || -74.006 },
            zoom: options.zoom || 12,
            ...options
        });

        this.maps[containerId] = map;
        return map;
    },

    addMarker(containerId, lat, lng, title) {
        const map = this.maps[containerId];
        if (!map || !window.google) return null;

        return new window.google.maps.Marker({
            position: { lat, lng },
            map: map,
            title: title
        });
    }
};
