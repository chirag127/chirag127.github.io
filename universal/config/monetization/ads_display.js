/**
 * Part 1: Monetization - Display Advertising
 * SAFE DEFAULTS: Only Google AdSense enabled. Other networks disabled until manually enabled.
 * @module config/monetization/ads_display
 */

export const ads_display = {
    // ============================================================================
    // GOOGLE ADSENSE - The Gold Standard
    // ============================================================================
    // Description:
    // The most reliable and widely used display advertising network.
    // Delivers high-quality, contextual ads that blend with content.
    //
    // Key Features:
    // - Auto Ads: Machine learning places ads automatically for best performance.
    // - High Fill Rate: Nearly 100% fill rate globally.
    // - Brand Safety: Strict policies ensure safe, family-friendly ads.
    // - Variety: Display, text, native, and vignette (interstitial) formats.
    //
    // Monetization Model:
    // - CPC (Cost Per Click) and CPM (Cost Per Mille) hybrid.
    // - You get paid when users click or view ads.
    //
    // Requirements:
    // - High-quality, original content (no scraped/AI spam).
    // - Domain age (sometimes requires 6 months in certain regions).
    // - Strict adherence to Program Policies.
    // - "Sufficient" content (usually 15-30 high-quality posts).
    //
    // Payout Details:
    // - Minimum Payout: $100 / €70 / £60.
    // - Frequency: Monthly (Net-30).
    // - Methods: Bank Transfer (EFT), Check, Wire Transfer.
    //
    // Best For:
    // - Blogs, news sites, tools, and forums with original content.
    // - Publishers seeking stability and passive income.
    //
    adsense: { publisherId: '', enabled: true, autoAds: true, lazyLoad: true },

    // ============================================================================
    // ADSTERRA - The Best Alternative for New Sites
    // ============================================================================
    // Description:
    // A premium advertising network that is extremely beginner-friendly.
    // Known for fast approval and not requiring minimum traffic.
    //
    // Key Features:
    // - 10-minute approval process.
    // - Anti-Adblock technology increases revenue by 20%+.
    // - CPA, CPC, CPM, CPL, CPI models available.
    // - Clean ads (malware protection).
    // - Social Bar: A proprietary, engaging ad format (high CTR).
    //
    // Monetization Model:
    // - CPM (Cost Per 1000 Impressions) & CPA (Cost Per Action).
    //
    // Requirements:
    // - NO minimum traffic requirement.
    // - Accepting of most niches (including crypto, downloads, streaming).
    // - No illegal content.
    //
    // Payout Details:
    // - Minimum Payout: $5 (Paxum, WebMoney), $100 (Bitcoin, USDT, PayPal).
    // - Frequency: Net-15 (Twice a month payments!).
    // - Methods: PayPal, USDT (Tether), Bitcoin, Wire, Paxum.
    //
    // Best For:
    // - New websites with low traffic.
    // - Download, streaming, or utility sites.
    // - Publishers needing crypto payouts.
    //
    adsterra: { enabled: false, zones: { banner: '', native: '', socialBar: '' } },

    // ============================================================================
    // A-ADS (Anonymous Ads) - Crypto & Privacy Focused
    // ============================================================================
    // Description:
    // The first crypto advertising network, prioritizing anonymity.
    // No personal data required to sign up or receive payments.
    //
    // Key Features:
    // - No KYC (Know Your Customer) or sign-up required.
    // - Instant approval for almost any site.
    // - Lightweight ads (HTML/CSS only, no heavy JS tracking).
    // - Accepts gambling/crypto content.
    //
    // Monetization Model:
    // - Daily Budget (Fixed allocation) or CPD (Cost Per Day).
    // - Pure Performance (CPA) options available.
    //
    // Requirements:
    // - None. Literally zero. Just paste the code.
    //
    // Payout Details:
    // - Minimum Payout: ~1 Satoshi (Lightning Network) or 0.001 BTC (On-chain).
    // - Frequency: Daily automatic payouts.
    // - Methods: Bitcoin (BTC) only.
    //
    // Best For:
    // - Crypto faucets, blogs, privacy-focused tool sites.
    // - Publishers who want instant, anonymous monetization.
    //
    aads: { unitId: '', size: '728x90', enabled: false },

    // ============================================================================
    // YLLIX - Aggressive Monetization
    // ============================================================================
    // Description:
    // Global ad network with 100% fill rate worldwide.
    //
    // Key Features:
    // - Daily payments (minimum $1).
    // - Easy approval.
    //
    // Payout Details:
    // - Minimum Payout: $1 (PayPal).
    // - Frequency: Daily.
    //
    // Best For:
    // - Traffic sources that AdSense rejects.
    //
    yllix: { siteId: '', enabled: false }
};

export const ads_display_priority = ['adsense', 'adsterra', 'aads', 'yllix'];
export const ads_display_lazyLoad = true;  // Load ads after page content
