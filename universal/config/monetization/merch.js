/**
 * Part 1: Monetization - Merch / Print on Demand
 * @module config/monetization/merch
 */

export const merch = {
    // ============================================================================
    // SPREADSHOP - The Most Generous Free Tier
    // ============================================================================
    // Description:
    // A completely free print-on-demand shop system.
    // No upfront costs, no monthly fees, and no transaction fees.
    //
    // Key Features:
    // - 100% Free shop hosting.
    // - Embedded integration (seamlessly fits into your website).
    // - Hundreds of products (Apparel, Accessories, Home).
    // - "Success Bonus": Lower base prices as you sell more (Higher margins!).
    //
    // Monetization Model:
    // - You set the Retail Price.
    // - You keep the difference: (Retail Price - Base Price) = Your Profit.
    // - Example: Sell shirt for $25, Base price is $12, You keep $13.
    //
    // Free Tier Limits:
    // - Unlimited Products for sale.
    // - Design Upload Limit: Starts at 50 designs (Pilot tier).
    // - Limit increases to 500 (Astronaut) and Unlimited as you sell.
    // - NO Traffic requirements.
    //
    // Best For:
    // - Brand new sites, bands, creators wanting a "white-label" feel.
    //
    spreadshop: { shopId: '', enabled: false },

    // ============================================================================
    // SPRING (Formerly Teespring) - Social Integration
    // ============================================================================
    // Description:
    // Large POD marketplace with deep integrations into YouTube/Twitch/TikTok.
    //
    // Key Features:
    // - "Merch Shelf" on YouTube (requires 10k subs).
    // - Digital products support.
    // - Custom launcher.
    //
    // Monetization Model:
    // - Base Cost Model (similar to Spreadshop).
    // - Flat profit margins.
    //
    // Free Tier Limits:
    // - 100% Free to use.
    // - Design Launcher: Unlimited uploads.
    // - Listing cycle: Listings may expire if no sales, but can be relaunched.
    //
    // Best For:
    // - Social media influencers, YouTubers.
    //
    spring: { storeUrl: '', enabled: false },

    // ============================================================================
    // REDBUBBLE - The "Marketplace" (Tiered Fees Apply)
    // ============================================================================
    // Description:
    // Massive independent marketplace. You upload art; they sell it on their site.
    // Great for organic traffic from *their* search engine.
    //
    // Key Features:
    // - Huge organic traffic (customers come to Redbubble to buy).
    // - Easy upload to 60+ products at once.
    //
    // IMPORTANT FEE UPDATE (2024):
    // - "Standard" Account Tier (New Users): Pays a ~50% "Account Fee" on earnings!
    // - "Premium" Account Tier: Pays ~20% fee.
    // - "Pro" Account Tier: Pays 0% fee.
    // - This means if you are new, you keep LESS money than Spreadshop/Spring.
    //
    // Monetization Model:
    // - Artist Margin (Default 20%, adjustable).
    // - Minus Account Fees.
    //
    // Best For:
    // - Artists who want Redbubble to bring the customers.
    //
    redbubble: { storeUrl: '', enabled: false }
};

export const merch_priority = ['spreadshop', 'spring', 'redbubble'];
