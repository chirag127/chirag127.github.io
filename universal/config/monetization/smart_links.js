/**
 * Part 1: Monetization - Smart Links / Direct Links
 * ⛔ WARNING: These can be intrusive as they redirect users through ad waterfalls.
 * @module config/monetization/smart_links
 */

export const smart_links = {
    // ============================================================================
    // ADSTERRA SMART LINK - Direct Monetization
    // ============================================================================
    // Description:
    // A single URL that automatically picks the best ad for the visitor.
    //
    // ⚠️ WARNING:
    // - May trigger "Malicious Site" warnings in some browsers.
    // - Best used for "Extra" buttons or behind generic calls to action.
    //
    adsterra: { linkUrl: '', enabled: false },

    // ============================================================================
    // HILLTOPADS - 100% Safe Direct Links
    // ============================================================================
    // Description:
    // Focuses on "pre-approved" and safe ad content.
    //
    // Key Features:
    // - Global reach.
    // - Weekly payouts.
    //
    hilltopads: { linkUrl: '', enabled: false },

    // ============================================================================
    // LOS POLLOS - "Smart" Waterfalls
    // ============================================================================
    // Description:
    // Advanced algorithm to monetize any type of traffic.
    //
    // ⚠️ WARNING: Potentially aggressive redirects.
    //
    // ⚠️ DISABLED: Link hijacking - redirects ALL user clicks through ad waterfalls
    // Reason: Severely damages UX and trust. Never recommended.
    losPollos: { publisherId: '', enabled: false, _warning: 'HIJACKS ALL CLICKS' },

    // ============================================================================
    // SMARTYADS
    // ============================================================================
    // ⚠️ DISABLED: Link hijacking - redirects ALL user clicks through ad waterfalls
    // Reason: Severely damages UX and trust. Never recommended.
    smartyAds: { publisherId: '', enabled: false, _warning: 'HIJACKS ALL CLICKS' }
};

export const smart_links_priority = ['hilltopads', 'adsterra'];
