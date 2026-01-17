/**
 * Affiliate Networks Configuration
 * Promote products and earn commission
 *
 * @module config/ads/affiliates
 */

export const affiliatesConfig = {

    // =========================================================================
    // AMAZON ASSOCIATES - World's largest affiliate program
    // =========================================================================
    // HOW TO GET: https://affiliate-program.amazon.com/
    // 1. Sign up for Associates
    // 2. Add your website(s)
    // 3. Get your tracking ID (tag)
    // PAYOUT: Monthly, $10 minimum
    // TIP: Use Native Shopping Ads widget
    amazon: {
        enabled: true,
        trackingId: '',     // example: yourtag-20
        marketplace: 'US',  // US, UK, IN, etc.
        nativeAds: {
            enabled: true,
            adId: ''
        }
    },

    // =========================================================================
    // CLICKBANK - Digital products
    // =========================================================================
    // HOW TO GET: https://www.clickbank.com/
    // 1. Create account
    // 2. Get affiliate nickname
    // 3. Find products in marketplace
    // PAYOUT: Weekly, $10 minimum
    clickbank: {
        enabled: false,
        affiliateId: ''  // Your ClickBank nickname
    },

    // =========================================================================
    // SHAREASALE - Variety of merchants
    // =========================================================================
    // HOW TO GET: https://www.shareasale.com/
    // 1. Apply as affiliate
    // 2. Get approved by merchants
    // 3. Use deep links or banners
    // PAYOUT: Monthly, $50 minimum
    shareasale: {
        enabled: false,
        affiliateId: ''
    },

    // =========================================================================
    // CJ AFFILIATE (Commission Junction)
    // =========================================================================
    // HOW TO GET: https://www.cj.com/
    // 1. Apply at CJ
    // 2. Get publisher ID
    // 3. Join advertiser programs
    // PAYOUT: Monthly, varies by method
    cjAffiliate: {
        enabled: false,
        publisherId: ''
    },

    // =========================================================================
    // IMPACT - Premium affiliate platform
    // =========================================================================
    // HOW TO GET: https://impact.com/
    // 1. Sign up as partner
    // 2. Join brand programs
    // PAYOUT: Varies by brand
    impact: {
        enabled: false,
        accountId: ''
    },

    // =========================================================================
    // RAKUTEN ADVERTISING
    // =========================================================================
    // HOW TO GET: https://rakutenadvertising.com/
    // Large network with major brands
    rakuten: {
        enabled: false,
        affiliateId: ''
    }
};
