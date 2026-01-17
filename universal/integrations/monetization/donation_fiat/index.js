/**
 * Monetization - Fiat Donations Integrations
 * @module integrations/monetization/donation_fiat
 */
import { buymeacoffee } from './buymeacoffee.js';
import { kofi } from './kofi.js';
import { paypal } from './paypal.js';
import { liberapay } from './liberapay.js';

export const donation_fiat = {
    buymeacoffee, kofi, paypal, liberapay
};
