/**
 * Pop-Under & Interstitial Advertising Configuration
 * Higher revenue but more aggressive ad formats
 *
 * WARNING: These can affect user experience. Use sparingly.
 * WARNING: May conflict with Google AdSense policies if too aggressive.
 *
 * @module config/ads/popunder
 */

export const popunderAdsConfig = {

    // =========================================================================
    // POPADS - Industry leader for pop-unders
    // =========================================================================
    // HOW TO GET: https://www.popads.net/
    // 1. Sign up at https://www.popads.net/
    // 2. Add website verification
    // 3. Get publisher code
    // PAYOUT: $5 minimum, DAILY payouts available!
    // TIP: Best CPM rates in the industry for pops
    popads: {
        enabled: true,
        publisherId: '',
        frequency: 1,  // Pops per user per day
        delay: 0       // Seconds delay before pop
    },

    // =========================================================================
    // POPCASH - Stable and reliable
    // =========================================================================
    // HOW TO GET: https://popcash.net/
    // 1. Register at https://popcash.net/register
    // 2. Add your website
    // 3. Get JavaScript code
    // PAYOUT: $10 minimum
    popcash: {
        enabled: true,
        publisherId: '',
        frequency: 1
    },

    // =========================================================================
    // CLICKADU - Good CPM rates
    // =========================================================================
    // HOW TO GET: https://clickadu.com/
    // 1. Sign up as publisher
    // 2. Pass moderation
    // 3. Get integration code
    // PAYOUT: $10 minimum
    clickadu: {
        enabled: true,
        siteId: '',
        zoneId: ''
    },

    // =========================================================================
    // ADMAVEN - Famous for pop-unders
    // =========================================================================
    // HOW TO GET: https://ad-maven.com/
    // 1. Sign up at https://ad-maven.com/publisher/
    // 2. Add website
    // 3. Get code
    // PAYOUT: $50 minimum for wire, $10 PayPal
    admaven: {
        enabled: true,
        publisherId: '',
        scriptKey: ''
    },

    // =========================================================================
    // EXOCLICK - Giant network, all traffic types
    // =========================================================================
    // HOW TO GET: https://www.exoclick.com/
    // 1. Register at https://www.exoclick.com/
    // 2. Add websites
    // 3. Create zones
    // PAYOUT: $20 minimum
    exoclick: {
        enabled: false,
        publisherId: '',
        zoneId: ''
    },

    // =========================================================================
    // TRAFFICFORCE - High volume
    // =========================================================================
    // HOW TO GET: https://trafficforce.com/
    // 1. Apply as publisher
    // 2. Get approved
    // PAYOUT: Various
    trafficforce: {
        enabled: false,
        publisherId: ''
    }
};

// Only use one pop network at a time to avoid conflicts
export const popunderAdsPriority = [
    'popads',      // Best rates, daily payout
    'popcash',     // Reliable
    'clickadu',    // Good CPM
    'admaven',     // Established
    'exoclick',    // Volume
    'trafficforce'
];

// Recommended: Use max 1 pop per 24 hours per user
export const popunderLimits = {
    maxPopsPerDay: 1,
    delayBetweenPops: 86400,  // 24 hours in seconds
    excludePages: ['/privacy', '/terms', '/about']  // Don't pop on legal pages
};
