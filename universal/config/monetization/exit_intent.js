/**
 * Part 1: Monetization - Exit Intent
 * Catching users before they leave
 * @module config/monetization/exit_intent
 */

export const exit_intent = {
    // ============================================================================
    // OUIBOUNCE - Open Source Freedom
    // ============================================================================
    // Description:
    // A library that detects when a mouse leaves the viewport.
    //
    // Advantages:
    // - 100% Free - No limits.
    // - Privacy-first (No external tracking).
    // - Lightweight.
    //
    // Best For:
    // - Default recommendation for custom tools.
    //
    // ⚠️ DISABLED: Creates pop-up overlay when user tries to leave
    // Reason: Overlays content and interrupts exit flow. Considered intrusive UX.
    // Re-enable for newsletter signups or specific exit messaging.
    ouibounce: { enabled: false },

    // ============================================================================
    // POPTIN - Interactive Popups
    // ============================================================================
    // Description:
    // Visual builder for high-converting popups.
    //
    // Free Tier Limits (2025):
    // - 1,000 Visitors per month.
    // - Unlimited Poptins.
    // - Includes Poptin branding.
    //
    // Best For:
    // - Beginners wanting a visual editor.
    //
    poptin_exit: { siteKey: '', enabled: false }
};

export const exit_intent_priority = ['ouibounce', 'poptin_exit'];
