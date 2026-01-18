/**
 * Utility - Captcha Integrations
 * @module integrations/utility/captcha
 */
import * as recaptcha from './recaptcha.js';
import * as hcaptcha from './hcaptcha.js';
import * as turnstile from './turnstile.js';

export const captcha = {
    recaptcha, hcaptcha, turnstile
};
