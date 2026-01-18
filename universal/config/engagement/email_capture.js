/**
 * Part 3: Engagement - Email Capture
 * @module config/engagement/email_capture
 */
export const email_capture = {
    // Mailchimp
    // Feature: Industry leader in email marketing
    // Free Limit: 500 contacts, 1000 sends/month
    mailchimp: { formAction: '', enabled: true },

    // Sumo - List Building Tools
    // Feature: Simple bars and popups
    // Free Limit: Free basic email collection
    sumo: { siteId: '', enabled: true },

    // HelloBar
    // Feature: Top bars, sliders, modals
    // Free Limit: 5,000 views/month
    hellobar: { scriptId: '', enabled: true },

    // ConvertKit
    // Feature: Creator-focused, simple automation
    // Free Limit: 1,000 subscribers, unlimited broadcasts
    convertkit: { formId: '', enabled: true }
};

export const email_capture_priority = ['mailchimp', 'sumo', 'hellobar', 'convertkit'];
