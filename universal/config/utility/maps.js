/**
 * Part 5: Utility - Maps
 * @module config/utility/maps
 */
export const maps = {
    // Google Maps
    // Feature: The gold standard for map data
    // Free Limit: $200 monthly credit (~28k loads)
    googleMaps: { apiKey: '', enabled: false },

    // Mapbox
    // Feature: Highly customizable vector maps
    // Free Limit: 50,000 map loads/month
    mapbox: { accessToken: '', enabled: false },

    // OpenStreetMap
    // Feature: Community driven, open data
    // Free Limit: 100% Free
    openStreetMap: { enabled: true }
};
