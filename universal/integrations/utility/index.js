/**
 * Utility Providers Index
 * Captcha, cookies, consent management
 * @module utility
 */

import * as recaptcha from './recaptcha.js';
import * as hcaptcha from './hcaptcha.js';
import * as turnstile from './turnstile.js';
import * as cookiebot from './cookiebot.js';

export { recaptcha, hcaptcha, turnstile, cookiebot };

export const providers = { recaptcha, hcaptcha, turnstile, cookiebot };

// Captcha priority (use one at a time)
export const captchaPriority = ['turnstile', 'hcaptcha', 'recaptcha'];
