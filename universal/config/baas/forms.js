/**
 * Part 3: BaaS - Form Handling
 * Contact forms without backend
 * @module config/baas/forms
 */

export const forms = {
    // BIG TECH - Google Forms
    googleForms: { enabled: true },  // Embed iframes

    // FREE ALTERNATIVES (pick one)
    formspree: { formId: '', enabled: false },  // Free tier
    formsubmit: { email: '', enabled: false },  // No API key needed
    netlifyForms: { enabled: false },  // Only if on Netlify
    web3forms: { accessKey: '', enabled: false }
};

export const forms_priority = ['googleForms', 'formspree', 'formsubmit'];
