/**
 * Part 3: Utility - Cookie Consent (GDPR)
 * @module config/utility/cookie_consent
 */

export const cookie_consent = {
    // Free options
    // Cookiebot
    // Feature: Automatic scanning and blocking
    // Free Limit: 1 domain, < 100 pages
    cookiebot: { domainGroupId: '', enabled: false },  // Requires signup

    // Termly
    // Feature: Policy generator included
    // Free Limit: 1 policy, 100 scans/month
    termly: { websiteId: '', enabled: false },

    // Osano
    // Feature: Open source consent manager options
    // Free Limit: 1 domain, 5,000 visitors/mo
    osano: { scriptUrl: '', enabled: false },

    // Iubenda
    // Feature: Legal text generator
    // Free Limit: Privacy policy only (Consent paid)
    iubenda: { policyId: '', enabled: false }
};

export const cookie_consent_priority = ['cookiebot', 'termly'];
