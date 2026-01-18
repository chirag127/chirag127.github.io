/**
 * Part 1: Monetization - Merch / Print on Demand
 * @module config/monetization/merch
 */

export const merch = {
    // ============================================================================
    // SPREADSHOP - The Best for Embedding (Low Friction)
    // ============================================================================
    // Description:
    // Focuses on giving you a "white-label" shop you can embed in your site.
    //
    // Key Features:
    // - 0 Monthly Fees.
    // - 200+ Products.
    // - Performance Bonus: Sell more, lower your base cost.
    //
    // Monetization Model:
    // - You keep (Retail Price - Base Price).
    // - You control your own margins.
    //
    // Best For:
    // - Embedding a shop directly into a tool-hub or personal brand site.
    //
    spreadshop: { shopId: '', enabled: false },

    // ============================================================================
    // SPRING (Formerly Teespring) - Social King
    // ============================================================================
    // Description:
    // Massive fulfillment network with strong social media tie-ins.
    //
    // ⚠️ STATUS NOTE (2025):
    // - Still widely used but creators report some payout delays.
    // - Best for YouTube/TikTok influencers.
    //
    spring: { storeUrl: '', enabled: false },

    // ============================================================================
    // REDBUBBLE - The Organic Traffic Powerhouse
    // ============================================================================
    // Description:
    // They bring the customers, you provide the art.
    //
    // ⚠️ CRITICAL FEE UPDATE (September 2025):
    // - **Standard Tier: 50% Platform Fee** (Deducted from your earnings).
    // - **Premium Tier: 20% Platform Fee**.
    // - **Pro Tier: 0% Platform Fee**.
    // - *Warning*: New users suffer high fees unless they upgrade accounts via sales history.
    //
    // Best For:
    // - Artists who want Redbubble's search engine to drive traffic.
    //
    redbubble: { storeUrl: '', enabled: false }
};

export const merch_priority = ['spreadshop', 'spring', 'redbubble'];
