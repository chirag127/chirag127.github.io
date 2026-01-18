/**
 * Monetization - Crypto Donations Integrations
 * @module integrations/monetization/donation_crypto
 */
import * as coinbase from './coinbase.js';
import * as nowpayments from './nowpayments.js';

export const donation_crypto = {
    coinbase, nowpayments
};
