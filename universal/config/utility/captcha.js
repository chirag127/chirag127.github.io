/**
 * Part 3: Utility - Bot Protection (Captcha)
 * BIG TECH: Google reCAPTCHA or Cloudflare Turnstile
 * @module config/utility/captcha
 */

export const captcha = {
    // BIG TECH - Pick ONE
    // reCAPTCHA (Google)
    // Feature: Standard bot protection
    // Free Limit: 1 Million assessments/month
    recaptcha: { siteKey: '', enabled: false },  // Google - Most compatible

    // Turnstile (Cloudflare)
    // Feature: Privacy-first, no puzzles
    // Free Limit: Unlimited (100% Free)
    turnstile: { siteKey: '', enabled: false },  // Cloudflare - Privacy-friendly

    // hCaptcha
    // Feature: Privacy focused, pays publishers
    // Free Limit: Free basic plan
    hcaptcha: { siteKey: '', enabled: false }    // Pays you for captcha solves
};

export const captcha_priority = ['recaptcha', 'turnstile', 'hcaptcha'];
