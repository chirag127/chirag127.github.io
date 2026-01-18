/**
 * Part 3: Utility - Search
 * ENABLED - Site search for user experience
 * @module config/utility/search
 */

export const search = {
    // GOOGLE PROGRAMMABLE SEARCH - Free, reliable
    // Feature: Uses Google's index of your site
    // Free Limit: Unlimited (Ad-supported), or 100 queries/day (API)
    googleSearch: { cx: '', enabled: true },

    // Algolia
    // Feature: Instant search-as-you-type, typo tolerance
    // Free Limit: 10k records, 10k requests/month
    algolia: { appId: '', searchKey: '', indexName: '', enabled: false }  // Needs setup
};

export const search_priority = ['googleSearch', 'algolia'];
