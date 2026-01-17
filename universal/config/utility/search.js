/**
 * Part 3: Utility - Search
 * ENABLED - Site search for user experience
 * @module config/utility/search
 */

export const search = {
    // GOOGLE PROGRAMMABLE SEARCH - Free, reliable
    googleSearch: { cx: '', enabled: true },
    algolia: { appId: '', searchKey: '', indexName: '', enabled: false }  // Needs setup
};

export const search_priority = ['googleSearch', 'algolia'];
