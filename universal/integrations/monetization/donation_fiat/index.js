/**
 * Monetization - Fiat Donations Integrations
 * @module integrations/monetization/donation_fiat
 */
import * as buymeacoffee from './buymeacoffee.js';
import * as kofi from './kofi.js';
import * as paypal from './paypal.js';
import * as liberapay from './liberapay.js';

export const donation_fiat = {
    buymeacoffee, kofi, paypal, liberapay
};
