/**
 * Part 3: BaaS - Form Handling
 * Contact forms without backend
 * @module config/baas/forms
 */

export const forms = {
    // BIG TECH - Google Forms
    // Feature: Easy iframe embed, Google Sheets integration
    // Free Limit: Unlimited responses (storage depends on Google Drive)
    googleForms: { enabled: true },

    // FREE ALTERNATIVES (pick one)
    // Formspree
    // Feature: Simple form endpoint, spam protection
    // Free Limit: 50 submissions/month (Free Plan)
    formspree: { formId: '', enabled: false },

    // Formsubmit
    // Feature: No API key required, easy setup
    // Free Limit: Unlimited submissions (Generic free tier)
    formsubmit: { email: '', enabled: false },

    // Netlify Forms
    // Feature: Built-in if hosting on Netlify
    // Free Limit: 100 submissions/month, 10MB uploads
    netlifyForms: { enabled: false },

    // Web3Forms
    // Feature: No server required, CAPTCHA included
    // Free Limit: 250 submissions/month (Free Plan)
    web3forms: { accessKey: '', enabled: false }
};

export const forms_priority = ['googleForms', 'formspree', 'formsubmit'];
