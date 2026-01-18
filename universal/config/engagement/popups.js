/**
 * Part 4: Engagement - Popups & Lead Magnets
 * Email capture popups
 * @module config/engagement/popups
 */

export const popups = {
    // Sumo
    // Feature: Powerful popups and welcome mats
    // Free Limit: 10,000 emails/month (Generous)
    sumo: { siteId: '', enabled: true },  // Heavy

    // HelloBar
    // Feature: High converting sticky bars
    // Free Limit: 5,000 views/month
    hellobar: { scriptId: '', enabled: false },

    // Poptin
    // Feature: Smart exit-intent popups
    // Free Limit: 1,000 visitors/month, 1 domain
    poptin: { siteKey: '', enabled: false }
};

export const popups_priority = ['sumo', 'hellobar', 'poptin'];
