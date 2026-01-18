/**
 * Part 1: Monetization - Offerwalls (CPA)
 * Content lockers - user completes task to unlock content
 * @module config/monetization/offerwalls
 */

export const offerwalls = {
    // ============================================================================
    // CPALEAD - The Beginner Friendly Giant
    // ============================================================================
    // Description:
    // A massive CPA/CPI network known for having the lowest payout threshold.
    // Perfect for new publishers who want to see their first dollar quickly.
    //
    // Key Features:
    // - Fast Pay: Select offers pay Daily (Net-0).
    // - Content Lockers: Lock files/links until user completes an offer.
    // - Offer Wall: Rewards users for installing apps/surveys.
    // - Mobile App Installs (CPI): specialized focus.
    //
    // Monetization Model:
    // - CPA (Cost Per Action) & CPI (Cost Per Install).
    // - Rates vary by geo (Tier 1 countries pay significantly more).
    //
    // Requirements:
    // - Instant Approval (usually).
    // - No minimum traffic requirements.
    //
    // Payout Details:
    // - Minimum Payout: $1 (Fast Pay via PayPal), $10 (Standard), $50 (Wire).
    // - Frequency: Daily, Weekly, Net-15, Net-30 (depends on offer status).
    //
    // Best For:
    // - Locking game mods, eBooks, or premium content.
    // - Publishers wanting DAILY payments.
    // - Mobile traffic.
    //
    cpalead: { publisherId: '', enabled: false },

    // ============================================================================
    // OGADS - Mobile Content Locking King
    // ============================================================================
    // Description:
    // The #1 network for Mobile Content Locking.
    // Highly optimized for iOS/Android traffic.
    //
    // Key Features:
    // - Custom landing pages provided.
    // - Highest converting mobile offers in the industry.
    // - "Content Locker" optimized for touch screens.
    //
    // Requirements:
    // - Approval required (can be strict).
    // - Good social media traffic preferred (TikTok/Instagram/YouTube).
    //
    // Payout Details:
    // - Minimum Payout: $50.
    // - Frequency: Net-30, Net-7 (for higher earners).
    // - Methods: PayPal, Payoneer, Wire, Crypto (USDC/Bitcoin).
    //
    // Best For:
    // - Mobile game hacks/tweaks niche (Game niche).
    // - Social media traffic sources.
    //
    ogads: { publisherId: '', enabled: false },

    // ============================================================================
    // ADWORKMEDIA - Global Performance
    // ============================================================================
    // Description:
    // A long-standing CPA affiliate network.
    //
    // Key Features:
    // - Product Lockers (Shopping style).
    // - Global Reach (Offers for almost every country).
    //
    // Review Note (2024):
    // - Some reports of slow support/payout delays recently.
    // - Still widely widely used, but proceed with caution compared to CPALead.
    //
    // Payout Details:
    // - Minimum Payout: $35.
    // - Frequency: Net-30, Net-15, Net-7.
    // - Methods: PayPal, Check, Wire, Payoneer, Crypto.
    //
    // Best For:
    // - General international traffic.
    //
    adworkMedia: { publisherId: '', enabled: false }
};

export const offerwalls_priority = ['cpalead', 'ogads', 'adworkMedia'];
