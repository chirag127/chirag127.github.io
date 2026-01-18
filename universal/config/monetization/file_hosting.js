/**
 * Part 1: Monetization - File Hosting (PPD)
 * Pay Per Download - disabled by default
 * @module config/monetization/file_hosting
 */

export const file_hosting = {
    // Upload4ever
    // Feature: Pay per download
    upload4ever: { apiKey: '', enabled: false },

    // Up-Files
    // Feature: File sharing monetization
    upfiles: { apiKey: '', enabled: false },

    // DaUpload
    // Feature: High storage limits
    daupload: { apiKey: '', enabled: false }
};

export const file_hosting_priority = ['upload4ever', 'upfiles', 'daupload'];
