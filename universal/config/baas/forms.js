/**
 * Part 3: BaaS - Form Handling
 * Handle contact forms and submissions without a backend server
 * @module config/baas/forms
 */

export const forms = {
    // ============================================================================
    // GOOGLE FORMS - Free Unlimited Form Submissions
    // ============================================================================
    // What it does:
    // - Create forms with Google's form builder
    // - Unlimited form responses
    // - Automatic data collection in Google Sheets
    // - Email notifications for new submissions
    // - File upload support
    // - Form logic and branching
    // - Easy iframe embedding
    //
    // What it doesn't do:
    // - Limited customization (Google branding)
    // - No custom domain for forms
    // - Basic design options only
    // - No advanced spam protection
    //
    // Free Tier Limits:
    // - UNLIMITED responses
    // - Storage limited by Google Drive quota (15GB free)
    // - Unlimited forms
    // - Unlimited questions per form
    //
    // Best for: Simple forms, surveys, event registrations, data collection
    // Website: https://forms.google.com
    // Note: Most generous free tier - truly unlimited responses
    googleForms: { enabled: true },

    // ============================================================================
    // FORMSPREE - Simple Form Backend
    // ============================================================================
    // What it does:
    // - Form endpoint for HTML forms (no backend needed)
    // - Email notifications for submissions
    // - Spam protection with reCAPTCHA
    // - File uploads
    // - Custom redirect after submission
    // - Webhook support
    // - Form data export
    //
    // What it doesn't do:
    // - No form builder (you write HTML)
    // - Limited submissions on free tier
    // - No advanced automation
    // - No conditional logic
    //
    // Free Tier Limits (Free Plan):
    // - 50 submissions per month per form
    // - Unlimited forms
    // - Basic spam filtering
    // - Email notifications
    // - 7-day data retention
    //
    // Best for: Contact forms, feedback forms, simple data collection
    // Website: https://formspree.io
    // Note: Good for developers who want to code their own forms
    formspree: { formId: '', enabled: false },

    // ============================================================================
    // FORMSUBMIT - No Registration Required
    // ============================================================================
    // What it does:
    // - Form-to-email service with zero configuration
    // - No API key or registration required
    // - Spam protection
    // - Custom redirect and thank you pages
    // - File attachments
    // - Auto-response emails
    // - AJAX support
    //
    // What it doesn't do:
    // - No dashboard to view submissions
    // - No data storage (emails only)
    // - Limited customization
    // - No analytics
    //
    // Free Tier Limits:
    // - UNLIMITED submissions
    // - No registration required
    // - Basic spam protection
    // - Email delivery only
    //
    // Best for: Quick contact forms, no-setup solutions, temporary forms
    // Website: https://formsubmit.co
    // Note: Easiest setup - just point form to their endpoint
    formsubmit: { email: '', enabled: false },

    // ============================================================================
    // NETLIFY FORMS - Built-in for Netlify Hosting
    // ============================================================================
    // What it does:
    // - Automatic form handling if hosted on Netlify
    // - Spam filtering with Akismet
    // - Email notifications
    // - Webhook support
    // - Form data in Netlify dashboard
    // - File uploads
    //
    // What it doesn't do:
    // - Only works with Netlify hosting
    // - Limited submissions on free tier
    // - No advanced form logic
    //
    // Free Tier Limits (Netlify Free):
    // - 100 submissions per month
    // - 10MB file upload limit
    // - Basic spam filtering
    // - Email notifications
    //
    // Best for: Sites hosted on Netlify
    // Website: https://www.netlify.com/products/forms/
    // Note: Only enable if you're hosting on Netlify
    netlifyForms: { enabled: false },

    // ============================================================================
    // WEB3FORMS - Privacy-Focused Form Backend
    // ============================================================================
    // What it does:
    // - Form-to-email service with privacy focus
    // - Built-in CAPTCHA (hCaptcha)
    // - Custom email templates
    // - File attachments
    // - Webhook support
    // - No data storage (privacy-first)
    // - Auto-response emails
    //
    // What it doesn't do:
    // - No form builder
    // - No submission dashboard
    // - Limited to email delivery
    //
    // Free Tier Limits (Free Plan):
    // - 250 submissions per month
    // - Unlimited forms
    // - CAPTCHA included
    // - Email notifications
    // - No data retention (privacy)
    //
    // Best for: Privacy-conscious sites, GDPR compliance, contact forms
    // Website: https://web3forms.com
    // Note: Good balance of features and privacy
    web3forms: { accessKey: '', enabled: false }
};

export const forms_priority = ['googleForms', 'formspree', 'formsubmit'];

// Made with Bob
