/**
 * Part 1: Monetization - Sponsored Content
 * @module config/monetization/sponsored_content
 */

export const sponsored_content = {
    // Flyout
    // Feature: Sell sponsored posts on your blog
    flyout: { publisherId: '', enabled: false },

    // Publisuites
    // Feature: Marketplace for sponsored articles
    publisuites: { siteId: '', enabled: false }
};

export const sponsored_content_priority = ['flyout', 'publisuites'];
