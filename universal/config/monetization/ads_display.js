/**
 * Part 1: Monetization - Display Advertising
 * @module config/monetization/ads_display
 */

export const ads_display = {
    adsense: { publisherId: '', enabled: false, autoAds: true },
    aads: { unitId: '', size: '728x90', enabled: true },
    adsterra: { enabled: true, zones: { banner: '', native: '', socialBar: '' } },
    monetag: { zone: '202358', enabled: true, antiAdblock: true },  // YOUR ID
    propeller: { zone: '202358', enabled: true },  // YOUR ID
    hooliganMedia: { siteId: '', enabled: false },
    yllix: { siteId: '', enabled: true },
    revenueHits: { publisherId: '', enabled: true },
    bidvertiser: { publisherId: '', enabled: true },
    hilltopAds: { siteId: '', enabled: true },
    adcash: { zoneId: '', enabled: true }
};

export const ads_display_priority = ['adsense', 'monetag', 'propeller', 'adsterra', 'aads', 'yllix', 'revenueHits', 'bidvertiser', 'hilltopAds', 'adcash'];
