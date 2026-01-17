/**
 * Display Advertising Configuration
 * Standard banner ads from various networks
 *
 * PRIORITY: Use in order. If one fails, next one loads.
 * WARNING: Google AdSense may conflict with some networks. Read their policies.
 *
 * @module config/ads/display
 */

export const displayAdsConfig = {

    // =========================================================================
    // GOOGLE ADSENSE - Primary (Goal network, strict policies)
    // =========================================================================
    // HOW TO GET: https://www.google.com/adsense/start/
    // 1. Sign up with Google account
    // 2. Add your site and wait for approval (can take weeks)
    // 3. Get your Publisher ID (ca-pub-XXXXXXXXXX)
    // 4. Create ad units and get slot IDs
    // WARNING: Most strict policies. Don't use with aggressive ad networks.
    adsense: {
        publisherId: '',  // ca-pub-XXXXXXXXXX
        enabled: false,   // Enable when approved
        autoAds: true,    // Let Google place ads automatically
        slots: {
            // Create in AdSense dashboard -> Ads -> By ad unit
            banner: '',   // Slot ID for banner
            sidebar: '',  // Slot ID for sidebar
            inArticle: '' // Slot ID for in-article
        }
    },

    // =========================================================================
    // ADSTERRA - Easy approval, good for new sites
    // =========================================================================
    // HOW TO GET: https://adsterra.com/
    // 1. Sign up at https://publishers.adsterra.com/
    // 2. Add your website (approval in 24-48 hours)
    // 3. Get your publisher code from Dashboard -> Websites -> Get Code
    // PAYOUT: $5 minimum via PayPal/Bitcoin
    adsterra: {
        enabled: true,
        scriptUrl: '',  // Your Adsterra script URL
        zones: {
            banner: '',     // Banner zone ID
            native: '',     // Native banner ID
            socialBar: ''   // Social bar ID
        }
    },

    // =========================================================================
    // MONETAG (PropellerAds) - AI optimized, very easy approval
    // =========================================================================
    // HOW TO GET: https://monetag.com/ OR https://propellerads.com/
    // 1. Sign up at https://monetag.com/
    // 2. Add site and verify ownership (meta tag or file)
    // 3. Get zone ID from Dashboard -> Sites -> Create Zone
    // PAYOUT: $5 minimum
    monetag: {
        enabled: true,
        zone: '202358',  // Your existing zone ID
        antiAdblock: true
    },

    // =========================================================================
    // A-ADS (ANONYMOUS ADS) - No approval needed, pays in Bitcoin
    // =========================================================================
    // HOW TO GET: https://a-ads.com/
    // 1. No signup required! Just create ad unit
    // 2. Enter your Bitcoin address
    // 3. Get embed code immediately
    // PAYOUT: 0.00001 BTC minimum, daily payouts
    aads: {
        enabled: true,
        unitId: '',  // Get from https://a-ads.com/ -> Create Ad Unit
        size: '728x90'
    },

    // =========================================================================
    // HOOLIGAN MEDIA - Good CPM for new sites
    // =========================================================================
    // HOW TO GET: https://hooliganmedia.com/
    // 1. Apply at https://hooliganmedia.com/publishers/
    // 2. Wait for email approval
    // 3. Get ad tags from dashboard
    // PAYOUT: NET30
    hooliganMedia: {
        enabled: false,
        scriptUrl: '',
        siteId: ''
    },

    // =========================================================================
    // YLLIX - Accepts almost everyone
    // =========================================================================
    // HOW TO GET: https://yllix.com/
    // 1. Sign up at https://yllix.com/register
    // 2. Add website (instant approval usually)
    // 3. Create ad units
    // PAYOUT: $1 minimum via PayPal/Bitcoin
    yllix: {
        enabled: false,
        siteId: ''
    },

    // =========================================================================
    // BIDVERTISER - Bidding system, easy entry
    // =========================================================================
    // HOW TO GET: https://www.bidvertiser.com/
    // 1. Sign up as publisher
    // 2. Add your website
    // 3. Get XML feed or JavaScript code
    // PAYOUT: $10 minimum
    bidvertiser: {
        enabled: false,
        publisherId: ''
    },

    // =========================================================================
    // HILLTOPADS - Good for gaming/file sharing sites
    // =========================================================================
    // HOW TO GET: https://hilltopads.com/
    // 1. Register at https://hilltopads.com/publishers
    // 2. Add your website
    // 3. Get embed code
    // PAYOUT: $50 minimum for wire, $20 for PayPal
    hilltopAds: {
        enabled: false,
        siteId: ''
    },

    // =========================================================================
    // REVENUHITS - CPA based (pay per action)
    // =========================================================================
    // HOW TO GET: https://www.revenuhits.com/
    // 1. Sign up as publisher
    // 2. Add site and wait for approval
    // 3. Get performance-based ad code
    // PAYOUT: $20 minimum
    revenueHits: {
        enabled: false,
        publisherId: ''
    },

    // =========================================================================
    // ADCASH - Global coverage
    // =========================================================================
    // HOW TO GET: https://adcash.com/
    // 1. Register at https://publisher.adcash.com/
    // 2. Add website and verify
    // 3. Create zones
    // PAYOUT: $25 minimum
    adcash: {
        enabled: false,
        zoneId: ''
    }
};

// Fallback order for display ads
export const displayAdsPriority = [
    'adsense',      // Try Google first if approved
    'monetag',      // Then PropellerAds
    'adsterra',     // Then Adsterra
    'aads',         // Anonymous crypto ads
    'yllix',        // Low threshold
    'bidvertiser',
    'hilltopAds',
    'revenueHits',
    'adcash',
    'hooliganMedia'
];
