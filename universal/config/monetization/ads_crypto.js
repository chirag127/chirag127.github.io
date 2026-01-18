/**
 * Part 1: Monetization - Crypto Advertising
 * Safe crypto ad networks - no link hijacking
 * @module config/monetization/ads_crypto
 */

export const ads_crypto = {
    // ============================================================================
    // COINZILLA - Premium Crypto Network
    // ============================================================================
    // Description:
    // A top-tier advertising network specifically for the finance and crypto sectors.
    // Known for high-quality campaigns and strict publisher acceptance.
    //
    // Key Features:
    // - Native & Banner Formats: High-performing, non-intrusive formats.
    // - Liquidity: High fill rates for crypto-specific traffic.
    // - Automated Payouts: Weekly or monthly options.
    //
    // Monetization Model:
    // - CPM (Cost Per Mille) & CPC (Cost Per Click).
    //
    // Requirements:
    // - Website MUST be crypto/finance related.
    // - Website must be at least 3 months old.
    // - Strict quality check (Good design, unique content required).
    // - No bot traffic tolerances.
    //
    // Payout Details:
    // - Minimum Payout: €50 (EUR).
    // - Frequency: Automatic (Weekly/Monthly) or on Request (Daily).
    // - Methods: Bitcoin, Ethereum, USDT (ERC20), Bank Transfer (SEPA/SWIFT).
    //
    // Best For:
    // - Established crypto news sites, blogs, and tools.
    // - Publishers wanting premium, clean ads.
    //
    coinzilla: { zoneId: '04f0bcb8c5793e809c1b6d64b32b5772', format: 'banner', enabled: false },

    // ============================================================================
    // A-ADS (Anonymous Ads) - Privacy First
    // ============================================================================
    // Description:
    // The oldest Bitcoin advertising network (since 2011). Unique for widespread
    // acceptance and zero-data collection policy.
    //
    // Key Features:
    // - No KYC/Sign-up: Instant account creation.
    // - Lightweight: text/banner ads, no heavy JS scripts.
    // - Privacy: Does not track user data (cookies).
    //
    // Monetization Model:
    // - CPD (Cost Per Day) & CPA (Cost Per Action) share.
    // - Daily Budget share (share of advertiser's daily spend).
    //
    // Requirements:
    // - None. No traffic minimums.
    // - Accepts almost all sites (excluding illegal content).
    //
    // Payout Details:
    // - Minimum Payout: 0.001 BTC (~$40-$50 depending on rates) or ~1 Satoshi (Lightning).
    // - Frequency: Automatic Daily payouts.
    // - Methods: Bitcoin (BTC) Only.
    //
    // Best For:
    // - Faucets, small blogs, privacy-focused tools.
    // - Publishers needing instant approval.
    //
    aads: { unitId: '', enabled: false },

    // ============================================================================
    // COINTRAFFIC - Performance Network
    // ============================================================================
    // Description:
    // Leading crypto ad network partnering with top blockchain projects.
    // Focuses on high-impact formats like Press Releases and Native ads.
    //
    // Key Features:
    // - High CPMs: Premium advertisers in the space.
    // - Dedicated Managers: Personal support for optimization.
    //
    // Monetization Model:
    // - CPM & Fixed price (for PRs).
    //
    // Requirements:
    // - Quality content focused on Crypto/Finance.
    // - Moderate to High traffic (Quality matters more than raw numbers).
    //
    // Payout Details:
    // - Minimum Payout: €25.
    // - Frequency: On Request (Fast processing).
    // - Methods: Bitcoin, Ethereum, USDT, Bank Transfer.
    //
    // Best For:
    // - News portals requiring Press Release monetization.
    // - High-quality crypto blogs.
    //
    cointraffic: { publisherId: '', enabled: false },

    // ============================================================================
    // BITMEDIA.IO - Deep Targeting
    // ============================================================================
    // Description:
    // A sophisticated network offering deep targeting for advertisers, meaning
    // relevant ads for your users.
    //
    // Key Features:
    // - High Fill Rate: Large pool of advertisers.
    // - Flexible Models: CPM and CPC available.
    //
    // Requirements:
    // - Organic traffic only (Strict verification).
    // - No specific minimum stated, but verifies activity.
    //
    // Payout Details:
    // - Minimum Payout: $20.
    // - Frequency: Withdrawal on request (processed quickly).
    // - Methods: Bitcoin (BTC).
    //
    // Best For:
    // - Broad range of crypto sites.
    //
    bitmedia: { zoneId: '', enabled: false },

    // ============================================================================
    // COINAD - Platform for Faucets & Rotators
    // ============================================================================
    // Description:
    // Specialized network often dealing with lower-tier traffic like faucets.
    //
    // Key Features:
    // - Faucet-Friendly: specifically targets this niche.
    // - Weekly Payouts.
    //
    // Requirements:
    // - Alexa Rank < 100,000 (for Invite Only tier) OR Open for CoinAd.Media.
    //
    // Payout Details:
    // - Minimum Payout: ~0.005 BTC.
    // - Frequency: Weekly.
    // - Methods: Bitcoin.
    //
    // Best For:
    // - Faucet owners and traffic exchange sites.
    //
    coinad: { publisherId: '', enabled: false },

    // ============================================================================
    // ADSHARES - Decentralized Network
    // ============================================================================
    // Description:
    // A Web3 native ad protocol. Connects publishers and advertisers directly
    // via blockchain, cutting out the middleman fees.
    //
    // Key Features:
    // - Decentralized: No middleman taking 30-50% cuts.
    // - Instant Payments: Earnings streamed to wallet.
    // - AdBlock Resistant options.
    //
    // Monetization Model:
    // - CPV (Cost Per View) / CPA.
    //
    // Requirements:
    // - None. decentralized permissionless entry.
    //
    // Payout Details:
    // - Minimum Payout: No minimum (Dust limits apply).
    // - Frequency: Near Instant / Hourly.
    // - Methods: ADS Token (Native).
    //
    // Best For:
    // - Web3 enthusiasts, dApps, and metaverse projects.
    //
    adshares: { publisherId: '', enabled: false }
};

export const ads_crypto_priority = ['coinzilla', 'aads', 'cointraffic', 'bitmedia', 'adshares', 'coinad'];
