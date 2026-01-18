/**
 * Part 1: Monetization - Display Advertising
 * SAFE DEFAULTS: Only Google AdSense enabled. Other networks disabled until manually enabled.
 * @module config/monetization/ads_display
 */

export const ads_display = {
    // BIG TECH - Preferred (Google)
    // Feature: Highest fill rate, contextual ads
    // Policies: Strict content guidelines
    adsense: { publisherId: '', enabled: false, autoAds: true, lazyLoad: true },  // Enable when approved

    // SAFE NETWORKS - Disabled by default (enable one at a time)
    // Adsterra
    // Feature: Popunders, Social Bar, Direct Link
    // Free Limit: No minimum traffic requirement
    adsterra: { enabled: false, zones: { banner: '', native: '', socialBar: '' } },

    // A-ADS (Anonymous Ads)
    // Feature: Bitcoin payments, Privacy focused, No approval
    // Fees: Daily budget or CPM based
    aads: { unitId: '', size: '728x90', enabled: false },  // Crypto network

    // Yllix
    // Feature: Easy approval, daily payouts
    yllix: { siteId: '', enabled: false },

    // RevenueHits
    // Feature: CPA based (Performance), not CPM
    revenueHits: { publisherId: '', enabled: false },

    // Bidvertiser
    // Feature: Direct advertising bidding
    bidvertiser: { publisherId: '', enabled: false },

    // HilltopAds
    // Feature: Anti-Adblock solutions
    hilltopAds: { siteId: '', enabled: false },

    // Adcash
    // Feature: Global coverage, massive inventory
    adcash: { zoneId: '', enabled: false },

    // Hooligan Media
    // Feature: Premium demand for gaming/entertainment sites
    hooliganMedia: { siteId: '', enabled: false },

    // ⚠️ POTENTIALLY DANGEROUS - Creates smart links, may hijack navigation
    // Monetag (PropellerAds)
    // Feature: High CPM but aggressive formats
    monetag: { zone: '202358', enabled: false, antiAdblock: false },  // DISABLED - Known for aggressive redirects

    // PropellerAds
    // Feature: Push notifications, Popunder specialists
    propeller: { zone: '202358', enabled: false }  // DISABLED - Same network as Monetag
};

export const ads_display_priority = ['adsense', 'adsterra', 'aads', 'yllix'];
export const ads_display_lazyLoad = true;  // Load ads after page content
