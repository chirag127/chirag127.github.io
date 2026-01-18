/**
 * Part 3: BaaS - Email API
 * Send emails from client-side
 * @module config/baas/email
 */

export const email = {
    // EmailJS - Works purely client-side
    // Feature: Send email directly from JS, no backend needed
    // Free Limit: 200 emails/month, 2 email templates
    emailjs: { serviceId: '', templateId: '', publicKey: '', enabled: false },

    // Resend - Modern Email API
    // Feature: Developer-first, React Email support
    // Free Limit: 3000 emails/month, 100/day
    resend: { apiKey: '', enabled: false }
};

export const email_priority = ['emailjs'];
