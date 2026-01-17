/**
 * Part 3: Utility - Cookie Consent (GDPR)
 * @module config/utility/cookie_consent
 */

export const cookie_consent = {
    // Free options
    cookiebot: { domainGroupId: '', enabled: false },  // Requires signup
    termly: { websiteId: '', enabled: false },
    osano: { scriptUrl: '', enabled: false },
    iubenda: { policyId: '', enabled: false }
};

export const cookie_consent_priority = ['cookiebot', 'termly'];
