/**
 * Part 3: Utility - Cookie Consent (GDPR)
 * @module config/utility/cookie_consent
 */

export const cookie_consent = {
    // ============================================================================
    // OSANO / SILKTIDE (Open Source Libraries)
    // ============================================================================
    // Description:
    // Free, open-source cookie consent managers you host yourself.
    //
    // Limits:
    // - 100% Free code.
    // - No "automatic scanning" (usually manual config).
    //
    osano: { scriptUrl: '', enabled: false },

    // ============================================================================
    // COOKIEBOT
    // ============================================================================
    // Free Limit:
    // - 1 Domain.
    // - Under 100 subpages.
    //
    cookiebot: { domainGroupId: '', enabled: false },

    // ============================================================================
    // TERMLY
    // ============================================================================
    // Free Limit:
    // - 1 Policy.
    // - 100 Scans/month.
    //
    termly: { websiteId: '', enabled: false }
};

export const cookie_consent_priority = ['osano', 'cookiebot', 'termly'];
