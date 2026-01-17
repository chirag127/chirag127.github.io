/**
 * Display Advertising Configuration
 * General banner ad networks for monetization
 *
 * FALLBACK PATTERN: If AdSense fails → Adsterra → Monetag → HilltopAds → Yllix
 *
 * HOW TO ACQUIRE:
 *
 * Google AdSense:
 *   1. Go to https://www.google.com/adsense/start/
 *   2. Apply with your website (requires good content, privacy policy)
 *   3. Wait for approval (can take weeks for new sites)
 *   4. Get your publisher ID: ca-pub-XXXXXXXXXXXXXXXX
 *   WARNING: Don't use other aggressive ad networks while waiting for AdSense!
 *
 * Adsterra:
 *   1. Go to https://adsterra.com/
 *   2. Sign up as Publisher
 *   3. Add your website
 *   4. Get your ad unit code (contains your zone ID)
 *   5. Fast approval, usually 24-48 hours
 *
 * Monetag (PropellerAds):
 *   1. Go to https://monetag.com/ or https://propellerads.com/
 *   2. Sign up → Add site → Get zone ID
 *   3. Very fast approval
 *
 * A-ADS (Anonymous Ads):
 *   1. Go to https://a-ads.com/
 *   2. NO APPROVAL NEEDED - just create ad unit
 *   3. Get your ad unit ID
 *   4. Pays in Bitcoin
 *
 * HilltopAds:
 *   1. Go to https://hilltopads.com/
 *   2. Register as publisher
 *   3. Add site, get zone ID
 *
 * Yllix:
 *   1. Go to https://yllix.com/
 *   2. Sign up, accepts almost all sites
 *   3. Get your publisher ID
 *
 * RevenueHits:
 *   1. Go to https://www.revenuehits.com/
 *   2. CPA-based (pay per action, not impression)
 *   3. Good for download sites
 *
 * BidVertiser:
 *   1. Go to https://www.bidvertiser.com/
 *   2. Bidding-based system
 *   3. Get ad code
 *
 * @module config/ads-display
 */

export const adsDisplayConfig = {
    // Priority order for fallback loading
    _priority: ['adsense', 'adsterra', 'monetag', 'aads', 'hilltopads', 'yllix', 'revenuehits', 'bidvertiser'],
    _fallbackEnabled: true,

    // Google AdSense - THE GOAL (disabled until approved)
    adsense: {
        id: '',  // ca-pub-XXXXXXXXXXXXXXXX
        enabled: false,  // Enable ONLY after AdSense approval
        autoAds: true,
        // WARNING: Disable aggressive networks before applying!
        adSenseSafe: true
    },

    // Adsterra - Fast approval, good rates
    adsterra: {
        zoneId: '',
        scriptUrl: '',  // Your full script URL from Adsterra
        enabled: false,
        adSenseSafe: true  // Generally safe
    },

    // Monetag (PropellerAds) - AI optimized
    monetag: {
        zone: '202358',  // Your existing zone
        enabled: true,
        scriptUrl: 'https://quge5.com/88/tag.min.js',
        adSenseSafe: false  // Can be aggressive
    },

    // A-ADS - No approval needed, pays in BTC
    aads: {
        adUnitId: '',
        size: '728x90',  // or 300x250, 468x60
        enabled: false,
        adSenseSafe: true
    },

    // HilltopAds
    hilltopads: {
        zoneId: '',
        enabled: false,
        adSenseSafe: true
    },

    // Yllix - Accepts everyone
    yllix: {
        publisherId: '',
        enabled: false,
        adSenseSafe: true
    },

    // RevenueHits - CPA based
    revenuehits: {
        publisherId: '',
        enabled: false,
        adSenseSafe: true
    },

    // BidVertiser
    bidvertiser: {
        publisherId: '',
        enabled: false,
        adSenseSafe: true
    }
};
