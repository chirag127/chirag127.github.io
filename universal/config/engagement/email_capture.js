/**
 * Part 3: Engagement - Email Capture & Marketing
 * @module config/engagement/email_capture
 */

export const email_capture = {
    // ============================================================================
    // MAILERLITE - The Best Free Generosity (2025)
    // ============================================================================
    // Description:
    // Clean, modern, and high-deliverability email marketing.
    //
    // Key Features:
    // - **FREE Automations** (Unlike Mailchimp).
    // - Landing pages and popups.
    //
    // Free Tier Limits (Updated Sept 2025):
    // - **500 Subscribers** (Reduced from 1,000).
    // - **12,000 Emails / month**.
    // - Full Automation features included.
    //
    mailerlite: { apiKey: '', enabled: true },

    // ============================================================================
    // MAILCHIMP - The Big Brand
    // ============================================================================
    // Description:
    // The most recognizable name in email.
    //
    // Free Tier Limits (2025):
    // - **500 Contacts**.
    // - **1,000 Emails / month** (Very low limit).
    // - **NO Automation** on free plan (as of June 2025).
    //
    mailchimp: { apiKey: '', serverPrefix: '', enabled: false },

    // ============================================================================
    // CONVERTKIT (SEVA)
    // ============================================================================
    // Free Tier:
    // - 1,000 Subscribers.
    // - Unlimited landing pages.
    //
    convertkit: { apiKey: '', enabled: false }
};

export const email_capture_priority = ['mailerlite', 'convertkit', 'mailchimp'];
