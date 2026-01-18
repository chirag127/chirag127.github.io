import { ads_crypto } from './ads_crypto.js';
import { ads_display } from './ads_display.js';
import { ads_interstitial } from './ads_interstitial.js';
import { ads_native } from './ads_native.js';
import { ads_pop } from './ads_pop.js';
import { ads_push } from './ads_push.js';
import { ads_text } from './ads_text.js';
import { ads_video } from './ads_video.js';
import { affiliates } from './affiliates.js';
import { browser_mining } from './browser_mining.js';
import { captcha_monetization } from './captcha_monetization.js';
import { donation_crypto } from './donation_crypto.js';
import { donation_fiat } from './donation_fiat.js';
import { exit_intent } from './exit_intent.js';
import { file_hosting } from './file_hosting.js';
import { merch } from './merch.js';
import { offerwalls } from './offerwalls.js';
import { smart_links } from './smart_links.js';
import { sponsored_content } from './sponsored_content.js';
import { url_shortener } from './url_shortener.js';

export const monetization = {
    ads_crypto, ads_display, ads_interstitial, ads_native, ads_pop,
    ads_push, ads_text, ads_video, affiliates, browser_mining,
    captcha_monetization, donation_crypto, donation_fiat, exit_intent,
    file_hosting, merch, offerwalls, smart_links, sponsored_content,
    url_shortener
};

export {
    ads_crypto, ads_display, ads_interstitial, ads_native, ads_pop,
    ads_push, ads_text, ads_video, affiliates, browser_mining,
    captcha_monetization, donation_crypto, donation_fiat, exit_intent,
    file_hosting, merch, offerwalls, smart_links, sponsored_content,
    url_shortener
};

/**
 * GLOBAL MONETIZATION PRIORITIES
 * Defines which methods to try first in the waterfall system.
 */
export const monetization_priorities = {
    // Primary - Non-intrusive
    primary: ['donation_fiat', 'affiliates', 'ads_display'],

    // Secondary - Contextual
    secondary: ['ads_native', 'ads_text', 'sponsored_content'],

    // Tertiary - Aggressive (Disabled by default)
    aggressive: ['ads_pop', 'ads_interstitial', 'ads_push', 'url_shortener', 'offerwalls'],

    // Specialty
    specialty: ['ads_crypto', 'merch', 'file_hosting', 'donation_crypto']
};
