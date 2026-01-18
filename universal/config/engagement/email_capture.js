/**
 * Part 3: Engagement - Email Capture
 * @module config/engagement/email_capture
 */
export const email_capture = {
    mailchimp: { formAction: '', enabled: true },
    sumo: { siteId: '', enabled: true },
    hellobar: { scriptId: '', enabled: true },
    convertkit: { formId: '', enabled: true }
};

export const email_capture_priority = ['mailchimp', 'sumo', 'hellobar', 'convertkit'];
