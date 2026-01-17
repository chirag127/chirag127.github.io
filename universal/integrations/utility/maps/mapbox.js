/**
 * Mapbox Integration
 */
export const mapbox = {
    loaded: false,
    maps: {},

    init(config) {
        if (!config.enabled || !config.accessToken || this.loaded) return;

        // Load Mapbox CSS
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://api.mapbox.com/mapbox-gl-js/v3.0.1/mapbox-gl.css';
        document.head.appendChild(link);

        // Load Mapbox JS
        const script = document.createElement('script');
        script.src = 'https://api.mapbox.com/mapbox-gl-js/v3.0.1/mapbox-gl.js';
        script.onload = () => {
            window.mapboxgl.accessToken = config.accessToken;
            this.ready = true;
            console.log('[Mapbox] Ready');
        };
        document.head.appendChild(script);

        this.loaded = true;
    },

    createMap(containerId, options = {}) {
        if (!this.ready || !window.mapboxgl) return null;

        const map = new window.mapboxgl.Map({
            container: containerId,
            style: options.style || 'mapbox://styles/mapbox/streets-v12',
            center: [options.lng || -74.5, options.lat || 40],
            zoom: options.zoom || 9
        });

        this.maps[containerId] = map;
        return map;
    },

    addMarker(containerId, lng, lat, options = {}) {
        const map = this.maps[containerId];
        if (!map || !window.mapboxgl) return null;

        const marker = new window.mapboxgl.Marker(options)
            .setLngLat([lng, lat])
            .addTo(map);

        return marker;
    }
};
