/**
 * Part 3: Engagement - Email Capture
 * @module config/engagement/email_capture
 */
export const email_capture = {
    // ConvertKit
    // Feature: Creator-focused, unlimited broadcasts
    // Free Limit: 1,000 subscribers, unlimited emails
    convertkit: { formId: '', enabled: true },

    // Mailchimp
    // Feature: Industry leader in email marketing
    // Free Limit: 250 contacts, 500 sends/month (Very restrictive)
    mailchimp: { formAction: '', enabled: false },

    // Sumo - List Building Tools
    // Feature: Simple bars and popups
    // Free Limit: 10,000 emails/month (Generous for capture)
    sumo: { siteId: '', enabled: false },

    // HelloBar
    // Feature: Top bars, sliders, modals
    // Free Limit: 5,000 views/month
    hellobar: { scriptId: '', enabled: false }
};

export const email_capture_priority = ['convertkit', 'sumo', 'mailchimp', 'hellobar'];
