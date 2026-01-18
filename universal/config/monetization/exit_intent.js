/**
 * Part 1: Monetization - Exit Intent
 * Popup when mouse leaves window
 * @module config/monetization/exit_intent
 */

export const exit_intent = {
    // ============================================================================
    // OUIBOUNCE - Open Source Freedom
    // ============================================================================
    // Description:
    // A free, open-source JavaScript library to detect exit intent.
    //
    // Features:
    // - 100% Free Forever.
    // - Adjustable sensitivity.
    // - Zero external dependencies.
    //
    // Best For:
    // - Developers who can code their own modal/popup HTML/CSS.
    //
    ouibounce: { enabled: true },

    // ============================================================================
    // POPTIN - Smart Popups
    // ============================================================================
    // Description:
    // Zero-code popup builder with advanced exit intent triggers.
    //
    // Free Tier Limits:
    // - 1,000 Visitors/month.
    // - 1 Domain.
    // - Unlimited Poptins (Popups).
    // - Branding present on free tier.
    //
    // Best For:
    // - Small sites wanting a polished, no-code solution.
    //
    poptin_exit: { siteKey: '', enabled: false }
};

export const exit_intent_priority = ['ouibounce', 'poptin_exit'];
