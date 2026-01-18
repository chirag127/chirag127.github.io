/**
 * Part 3: Utility - Bot Protection (Captcha)
 * BIG TECH: Google reCAPTCHA or Cloudflare Turnstile
 * @module config/utility/captcha
 */

export const captcha = {
    // ============================================================================
    // CLOUDFLARE TURNSTILE - The New Standard (RECOMMENDED)
    // ============================================================================
    // Description:
    // "Frustration-free" smart CAPTCHA replacement.
    // No clicking fire hydrants. Privacy-focused.
    //
    // Free Tier Limits (2024):
    // - UNLIMITED Challenges/Verifications.
    // - Up to 20 Widgets (Sites).
    // - 15 Hostnames per widget.
    //
    // Best For:
    // - EVERYBODY. This is the current best "Generous Free Tier" option.
    //
    turnstile: { siteKey: '', enabled: false },

    // ============================================================================
    // GOOGLE RECAPTCHA V3 / ENTERPRISE
    // ============================================================================
    // Description:
    // The invisible scoring system from Google.
    //
    // IMPORTANT 2024 PRICING UPDATE:
    // - Free tier reduced from 1 Million to **10,000** assessments/month.
    // - $1 per 1,000 assessments after that.
    // - Requires Cloud Billing account.
    //
    // Best For:
    // - Enterprise sites or extremely low volume personal projects.
    //
    recaptcha: { siteKey: '', enabled: false },

    // ============================================================================
    // HCAPTCHA - Privacy Focused
    // ============================================================================
    // Description:
    // Privacy-first alternative.
    //
    hcaptcha: { siteKey: '', enabled: false }
};

export const captcha_priority = ['turnstile', 'hcaptcha', 'recaptcha'];
