/**
 * Part 3: Utility - Geolocation (IP Detection)
 * @module config/utility/geolocation
 */

export const geolocation = {
    // IPInfo
    // Feature: Detailed ISP/ASN data
    // Free Limit: 50,000 requests/month
    ipinfo: { token: '', enabled: true },  // Get user country

    // Ipify
    // Feature: Simple Public IP Address API
    // Free Limit: Unlimited
    ipify: { enabled: true }  // Simple IP detection
};

export const geolocation_priority = ['ipinfo', 'ipify'];
