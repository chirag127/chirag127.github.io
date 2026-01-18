/**
 * Part 3: BaaS - Email API
 * Send emails directly from client-side JavaScript without a backend server
 * @module config/baas/email
 */

export const email = {
    // ============================================================================
    // EMAILJS - Client-Side Email Service (No Backend Required)
    // ============================================================================
    // What it does:
    // - Send emails directly from JavaScript (browser or Node.js)
    // - No backend server required - works purely client-side
    // - Email templates with dynamic variables
    // - SMTP integration with your email provider
    // - Spam protection and rate limiting
    // - Email delivery tracking and logs
    //
    // What it doesn't do:
    // - No bulk email campaigns (use Mailchimp for that)
    // - No email list management
    // - No advanced automation workflows
    // - Limited to transactional emails (contact forms, notifications)
    //
    // Free Tier Limits (Free Plan):
    // - 200 emails per month
    // - 2 email templates
    // - 1 email service connection
    // - Basic email tracking
    // - Community support
    //
    // Best for: Contact forms, simple notifications, small websites
    // Website: https://www.emailjs.com
    // Note: Perfect for static sites without backend
    emailjs: { serviceId: '', templateId: '', publicKey: '', enabled: false },

    // ============================================================================
    // RESEND - Modern Developer Email API
    // ============================================================================
    // What it does:
    // - Developer-first email API with simple integration
    // - React Email support (build emails with React components)
    // - Email validation and verification
    // - Webhook support for email events
    // - Email analytics and tracking
    // - Custom domain support
    // - Batch email sending
    //
    // What it doesn't do:
    // - Requires backend/server-side code (not client-side)
    // - No visual email template builder
    // - No marketing automation features
    // - No email list segmentation
    //
    // Free Tier Limits (Free Plan):
    // - 3,000 emails per month
    // - 100 emails per day
    // - 1 custom domain
    // - Email API access
    // - Webhook support
    // - Basic analytics
    //
    // Best for: Transactional emails, password resets, order confirmations, React apps
    // Website: https://resend.com
    // Note: Requires server-side implementation (Next.js API routes, serverless functions)
    resend: { apiKey: '', enabled: false }
};

export const email_priority = ['emailjs'];

// Made with Bob
