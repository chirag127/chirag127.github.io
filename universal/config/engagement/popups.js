/**
 * Part 3: Engagement - Popups & Lead Magnets
 * @module config/engagement/popups
 */

export const popups = {
    // ============================================================================
    // POPTIN - Interactive Visual Builder
    // ============================================================================
    // Description:
    // Create professional-looking popups, overlays, and sticky bars.
    //
    // Free Tier Limits (2025):
    // - **1,000 Visitors / month**.
    // - Unlimited Poptins.
    // - Poptin branding included.
    //
    poptin: { siteKey: '', enabled: false },

    // ============================================================================
    // WISERPOST - Smart Popups
    // ============================================================================
    // Free Limits:
    // - 5,000 Pageviews / month.
    //
    wiserpost: { apiKey: '', enabled: false },

    // ============================================================================
    // NATIVE POPUP (Core Engine)
    // ============================================================================
    // Description:
    // Built-in simple popup system within the Universal Core.
    // **100% Free** and lightweight.
    //
    native_popup: { enabled: true }
};

export const popups_priority = ['native_popup', 'poptin'];
