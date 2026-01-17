/**
 * Monetization Integrations Master Index
 * @module integrations/monetization
 */
import { ads_display } from './ads_display/index.js';
import { ads_crypto } from './ads_crypto/index.js';
import { ads_pop } from './ads_pop/index.js';
import { ads_push } from './ads_push/index.js';
import { ads_text } from './ads_text/index.js';
import { donation_fiat } from './donation_fiat/index.js';
import { donation_crypto } from './donation_crypto/index.js';
import { affiliates } from './affiliates/index.js';
import { url_shortener } from './url_shortener/index.js';

export const monetization = {
    ads_display, ads_crypto, ads_pop, ads_push, ads_text,
    donation_fiat, donation_crypto, affiliates, url_shortener
};
