/**
 * Part 3: Utility - Search
 * ENABLED - Site search for user experience
 * @module config/utility/search
 */

export const search = {
    // ============================================================================
    // GOOGLE PROGRAMMABLE SEARCH (CSE)
    // ============================================================================
    // Description:
    // Uses Google's index of your site.
    //
    // Free Limits:
    // - Unlimited queries (Ad-supported version).
    // - 100 queries/day (JSON API version without ads).
    //
    googleSearch: { cx: '', enabled: true },

    // ============================================================================
    // ALGOLIA - Instant Search
    // ============================================================================
    // Description:
    // Fast, typo-tolerant search-as-you-type.
    //
    // Free Limits:
    // - 10,000 Records.
    // - 10,000 requests/month.
    //
    algolia: { appId: '', searchKey: '', indexName: '', enabled: false }
};

export const search_priority = ['googleSearch', 'algolia'];
