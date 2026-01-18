/**
 * Part 1: Monetization - Affiliates
 * @module config/monetization/affiliates
 */

    // ============================================================================
    // AMAZON ASSOCIATES - The Everything Store
    // ============================================================================
    // Description:
    // The world's largest affiliate program. Easy to join, massive product selection.
    //
    // Key Features:
    // - Trust: High conversion rates because everyone trusts Amazon.
    // - Universal Cookie: You earn commission on ANYTHING they buy, not just the link they clicked.
    // - Cookie Duration: 24 hours (very short).
    //
    // Monetization Model:
    // - CPA (Cost Per Action).
    // - Commission Rates: 1% - 10% depending on category (e.g., Luxury=10%, Toys=3%, Tech=1-2%).
    //
    // Requirements:
    // - **180-Day Rule**: You MUST make 3 qualifying sales within the first 180 days or account is closed.
    // - Website must have original content (at least 10 posts).
    // - Disclaimer is MANDATORY on all pages with links.
    //
    // Payout Details:
    // - Minimum Payout: $10 (Direct Deposit/Gift Card), $100 (Check).
    // - Frequency: Net-60 (Paid 60 days after the month ends).
    //
    // Best For:
    // - Review sites, "Best of" lists, Tech blogs.
    //
    amazon: { trackingId: '', marketplace: 'US', enabled: true },

    // ============================================================================
    // SHAREASALE - Reliable & Diverse
    // ============================================================================
    // Description:
    // A massive network connecting publishers with thousands of merchants.
    // Owned by Awin, but operates independently with great tools.
    //
    // Key Features:
    // - 25,000+ Merchants (Reebok, Etsy, etc.).
    // - Real-time tracking and reporting.
    // - "Power Rank" helps you find top-performing merchants.
    // - Deep Linking creation tools.
    //
    // Monetization Model:
    // - CPA (Pay per Sale) and CPL (Pay per Lead).
    // - Commissions vary by merchant (typically 5% - 50%).
    //
    // Requirements:
    // - Free to join for Affiliates (Merchants pay to join).
    // - Website check required (usually fast approval).
    //
    // Payout Details:
    // - Minimum Payout: $50.
    // - Frequency: Monthly (20th of the month).
    // - Methods: Direct Deposit, Check, Payoneer, Wire.
    //
    // Best For:
    // - Fashion, Home, Garden, and Niche blogs.
    //
    shareasale: { affiliateId: '', enabled: true },

    // ============================================================================
    // CLICKBANK - Digital Products King
    // ============================================================================
    // Description:
    // Focuses on digital info-products (courses, e-books) and supplements.
    // Known for incredibly high commission rates.
    //
    // Key Features:
    // - Gravity Score: Shows how many affiliates are currently making sales (vital metric).
    // - High Commissions: Up to 75% - 90% commission on sales.
    // - Recurring Commissions: Reliable income from subscription products.
    // - Upsells: One-click upsells in funnels increase average cart value.
    //
    // Requirements:
    // - Easy sign-up, almost instant approval.
    // - **Dormant Account Fees**: $1/pay period after 90 days of no sales! Keep selling or close it.
    //
    // Payout Details:
    // - Minimum Payout: $10 (Configurable).
    // - Frequency: Weekly or Bi-weekly.
    // - Methods: Check, Direct Deposit, Wire, Payoneer.
    //
    // Best For:
    // - Influencers, Email marketers, "Make Money Online" niche, Health/Fitness niches.
    //
    clickbank: { nickname: '', enabled: true },

    // ============================================================================
    // CJ AFFILIATE (Commission Junction) - Premium Brands
    // ============================================================================
    // Description:
    // One of the oldest and largest networks. Home to Fortune 500 brands.
    //
    // Key Features:
    // - Big names: Apple, Home Depot, Nike, Barnes & Noble.
    // - Content Certified program for top publishers.
    //
    // Payout Details:
    // - Minimum Payout: $50 (Main), $100 (Check).
    //
    // Best For:
    // - Established sites with professional content.
    //
    cjAffiliate: { websiteId: '', enabled: false },

    // ============================================================================
    // RAKUTEN ADVERTISING - Top Tier
    // ============================================================================
    // Description:
    // Voted #1 Affiliate Network for many years. Premium fashion and retail brands.
    //
    // Key Features:
    // - Exclusive brands: Sephora, New Balance, Udemy.
    // - Deep linking and rotating banner tools.
    //
    // Requirements:
    // - Approval can be strict. High-quality site required.
    //
    rakuten: { publisherId: '', enabled: false },

    // ============================================================================
    // AWIN - Global Coverage
    // ============================================================================
    // Description:
    // Massive European and Global network. Over 21,000 advertisers.
    //
    // Key Features:
    // - "Opportunity Marketplace" to pitch directly to brands.
    // - Browser extension for generating links.
    //
    // Requirements:
    // - **Sign-up Fee**: $5 / £5 / €5 deposit (Refundable upon first payout).
    // - Verification purpose only to prevent fraud.
    //
    awin: { publisherId: '', enabled: false }
};

export const affiliates_priority = ['amazon', 'shareasale', 'clickbank', 'cjAffiliate', 'rakuten', 'awin'];
