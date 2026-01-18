/**
 * Part 5: Utility - Maps
 * @module config/utility/maps
 */
export const maps = {
    // ============================================================================
    // GOOGLE MAPS PLATFORM
    // ============================================================================
    // Description:
    // The gold standard for map data and accuracy.
    //
    // Free Tier Limits:
    // - Recurring $200 Monthly Credit.
    // - Equivalent to ~28,000 map loads (Dynamic Maps).
    // - Or ~100,000 Static map loads.
    // - **Credit Card Required**.
    //
    googleMaps: { apiKey: '', enabled: false },

    // ============================================================================
    // MAPBOX - Beautiful Custom Maps
    // ============================================================================
    // Description:
    // Highly customizable, designer-friendly maps.
    //
    // Free Tier Limits:
    // - 50,000 Map loads/month.
    // - 200,000 Static Tiles.
    //
    mapbox: { accessToken: '', enabled: false },

    // ============================================================================
    // OPENSTREETMAP (Leaflet) - 100% Free Data
    // ============================================================================
    // Description:
    // Open source map data. Usually rendered via Leaflet.js.
    //
    // Limits:
    // - Data is free (ODbL).
    // - **Tile Hosting**: Do NOT abuse main OSM tile servers.
    // - Use for light traffic or self-host tiles.
    //
    openStreetMap: { enabled: true }
};

export const maps_priority = ['googleMaps', 'mapbox', 'openStreetMap'];
