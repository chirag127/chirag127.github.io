/**
 * Part 3: BaaS - Email API
 * Send emails from client-side
 * @module config/baas/email
 */

export const email = {
    // EmailJS - Works purely client-side
    emailjs: { serviceId: '', templateId: '', publicKey: '', enabled: false },
    resend: { apiKey: '', enabled: false }
};

export const email_priority = ['emailjs'];
