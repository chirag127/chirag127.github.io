/**
 * Part 3: Utility - Geolocation (IP Detection)
 * @module config/utility/geolocation
 */

export const geolocation = {
    ipinfo: { token: '', enabled: true },  // Get user country
    ipify: { enabled: true }  // Simple IP detection
};

export const geolocation_priority = ['ipinfo', 'ipify'];
