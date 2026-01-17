/**
 * Utility - Captcha Integrations
 * @module integrations/utility/captcha
 */
import { recaptcha } from './recaptcha.js';
import { hcaptcha } from './hcaptcha.js';
import { turnstile } from './turnstile.js';

export const captcha = {
    recaptcha, hcaptcha, turnstile
};
