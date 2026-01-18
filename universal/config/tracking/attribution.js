/**
 * Part 2: Tracking - Attribution
 * Deep linking and attribution tracking
 * @module config/tracking/attribution
 */

export const attribution = {
    // Branch.io
    // Feature: Deep linking for mobile apps
    // Free Limit: 10,000 MAUs (Launch Plan)
    branch: { key: '', enabled: false },  // Deep linking

    // AppsFlyer
    // Feature: Marketing attribution
    // Free Limit: 12,000 conversions (Zero Plan)
    appsflyer: { devKey: '', enabled: false }  // App attribution
};

export const attribution_priority = ['branch'];
