/**
 * Part 1: Monetization - Display Advertising
 * SAFE DEFAULTS: Only Google AdSense enabled. Other networks disabled until manually enabled.
 * @module config/monetization/ads_display
 */

export const ads_display = {
    // BIG TECH - Preferred (Google)
    adsense: { publisherId: '', enabled: false, autoAds: true, lazyLoad: true },  // Enable when approved

    // SAFE NETWORKS - Disabled by default (enable one at a time)
    adsterra: { enabled: false, zones: { banner: '', native: '', socialBar: '' } },
    aads: { unitId: '', size: '728x90', enabled: false },  // Crypto network
    yllix: { siteId: '', enabled: false },
    revenueHits: { publisherId: '', enabled: false },
    bidvertiser: { publisherId: '', enabled: false },
    hilltopAds: { siteId: '', enabled: false },
    adcash: { zoneId: '', enabled: false },
    hooliganMedia: { siteId: '', enabled: false },

    // ⚠️ POTENTIALLY DANGEROUS - Creates smart links, may hijack navigation
    monetag: { zone: '202358', enabled: false, antiAdblock: false },  // DISABLED - Known for aggressive redirects
    propeller: { zone: '202358', enabled: false }  // DISABLED - Same network as Monetag
};

export const ads_display_priority = ['adsense', 'adsterra', 'aads', 'yllix'];
export const ads_display_lazyLoad = true;  // Load ads after page content
