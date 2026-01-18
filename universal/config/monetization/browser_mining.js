/**
 * Part 1: Monetization - Browser Mining
 * ⛔ DISABLED - Kills SEO and user trust
 * @module config/monetization/browser_mining
 */

export const browser_mining = {
    // ⛔ NEVER ENABLE - Destroys reputation
    // WebMinePool (Monero Mining)
    // Feature: Uses visitor CPU to mine crypto
    // Warning: Detected as malware by AV, drains battery, kills SEO
    webminepool: { siteKey: '', enabled: false, _warning: 'KILLS SEO' }
};

export const browser_mining_priority = [];
