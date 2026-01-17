/**
 * OpenStreetMap (Leaflet) Integration
 */
export const openStreetMap = {
    loaded: false,
    maps: {},

    init(config) {
        if (!config.enabled || this.loaded) return;

        // Load Leaflet CSS
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
        link.integrity = 'sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=';
        link.crossOrigin = '';
        document.head.appendChild(link);

        // Load Leaflet JS
        const script = document.createElement('script');
        script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
        script.integrity = 'sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=';
        script.crossOrigin = '';
        script.onload = () => {
            this.ready = true;
            console.log('[OpenStreetMap] Leaflet Ready');
        };
        document.head.appendChild(script);

        this.loaded = true;
    },

    createMap(containerId, options = {}) {
        if (!this.ready || !window.L) return null;

        const map = window.L.map(containerId).setView(
            [options.lat || 51.505, options.lng || -0.09],
            options.zoom || 13
        );

        window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        this.maps[containerId] = map;
        return map;
    },

    addMarker(containerId, lat, lng, popupText) {
        const map = this.maps[containerId];
        if (!map || !window.L) return null;

        const marker = window.L.marker([lat, lng]).addTo(map);
        if (popupText) marker.bindPopup(popupText);
        return marker;
    }
};
