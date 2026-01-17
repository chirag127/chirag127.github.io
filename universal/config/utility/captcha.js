/**
 * Part 3: Utility - Bot Protection (Captcha)
 * BIG TECH: Google reCAPTCHA or Cloudflare Turnstile
 * @module config/utility/captcha
 */

export const captcha = {
    // BIG TECH - Pick ONE
    recaptcha: { siteKey: '', enabled: false },  // Google - Most compatible
    turnstile: { siteKey: '', enabled: false },  // Cloudflare - Privacy-friendly
    hcaptcha: { siteKey: '', enabled: false }    // Pays you for captcha solves
};

export const captcha_priority = ['recaptcha', 'turnstile', 'hcaptcha'];
