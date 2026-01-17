/**
 * Part 1: Monetization - Index
 * @module config/monetization
 */

import { ads_display, ads_display_priority } from './ads_display.js';
import { ads_crypto, ads_crypto_priority } from './ads_crypto.js';
import { ads_pop, ads_pop_priority, ads_pop_limits } from './ads_pop.js';
import { ads_push, ads_push_priority } from './ads_push.js';
import { ads_text, ads_text_priority } from './ads_text.js';
import { url_shortener, url_shortener_priority } from './url_shortener.js';
import { donation_fiat, donation_fiat_priority } from './donation_fiat.js';
import { donation_crypto, donation_crypto_priority } from './donation_crypto.js';
import { affiliates, affiliates_priority } from './affiliates.js';

export const monetization = {
    ...ads_display, ...ads_crypto, ...ads_pop, ...ads_push, ...ads_text,
    ...url_shortener, ...donation_fiat, ...donation_crypto, ...affiliates, ads_pop_limits
};

export const monetization_priorities = {
    ads_display: ads_display_priority, ads_crypto: ads_crypto_priority,
    ads_pop: ads_pop_priority, ads_push: ads_push_priority, ads_text: ads_text_priority,
    url_shortener: url_shortener_priority, donation_fiat: donation_fiat_priority,
    donation_crypto: donation_crypto_priority, affiliates: affiliates_priority
};

export { ads_display, ads_crypto, ads_pop, ads_push, ads_text, url_shortener, donation_fiat, donation_crypto, affiliates };
