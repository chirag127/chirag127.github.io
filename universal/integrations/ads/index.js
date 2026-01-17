/**
 * Ads Providers Master Index
 * ALL advertising provider modules by category
 * @module ads
 */

// =========== DISPLAY ADS ===========
import * as propeller from './propeller.js';
import * as adsense from './adsense.js';
import * as aads from './aads.js';
import * as adsterra from './adsterra.js';
import * as monetag from './monetag.js';
import * as yllix from './yllix.js';
import * as bidvertiser from './bidvertiser.js';
import * as hilltopads from './hilltopads.js';
import * as revenuehits from './revenuehits.js';
import * as adcash from './adcash.js';

// =========== CRYPTO ADS ===========
import * as coinzilla from './coinzilla.js';
import * as cointraffic from './cointraffic.js';
import * as bitmedia from './bitmedia.js';
import * as coinad from './coinad.js';
import * as adshares from './adshares.js';

// =========== POP-UNDER ADS ===========
import * as popads from './popads.js';
import * as popcash from './popcash.js';
import * as clickadu from './clickadu.js';
import * as admaven from './admaven.js';
import * as exoclick from './exoclick.js';
import * as trafficforce from './trafficforce.js';

// =========== PUSH ADS ===========
import * as evadav from './evadav.js';
import * as richads from './richads.js';
import * as pushhouse from './pushhouse.js';
import * as tacoloco from './tacoloco.js';

// =========== TEXT/CONTEXTUAL ADS ===========
import * as infolinks from './infolinks.js';
import * as medianet from './medianet.js';

// =========== DONATIONS (FIAT) ===========
import * as buymeacoffee from './buymeacoffee.js';
import * as kofi from './kofi.js';
import * as paypal from './paypal.js';
import * as liberapay from './liberapay.js';

// =========== CRYPTO TIPPING ===========
import * as nowpayments from './nowpayments.js';
import * as coinbase from './coinbase.js';

// =========== OTHER ===========
import * as carbon from './carbon.js';
import * as buysellads from './buysellads.js';

// Export all individually
export {
    // Display
    propeller, adsense, aads, adsterra, monetag, yllix, bidvertiser, hilltopads, revenuehits, adcash,
    // Crypto
    coinzilla, cointraffic, bitmedia, coinad, adshares,
    // Pop-under
    popads, popcash, clickadu, admaven, exoclick, trafficforce,
    // Push
    evadav, richads, pushhouse, tacoloco,
    // Text
    infolinks, medianet,
    // Donations
    buymeacoffee, kofi, paypal, liberapay,
    // Crypto Tipping
    nowpayments, coinbase,
    // Other
    carbon, buysellads
};

// Categorized providers
export const displayProviders = { propeller, adsense, aads, adsterra, monetag, yllix, bidvertiser, hilltopads, revenuehits, adcash };
export const cryptoProviders = { coinzilla, cointraffic, bitmedia, coinad, adshares };
export const popunderProviders = { popads, popcash, clickadu, admaven, exoclick, trafficforce };
export const pushProviders = { evadav, richads, pushhouse, tacoloco };
export const textProviders = { infolinks, medianet };
export const donationProviders = { buymeacoffee, kofi, paypal, liberapay };
export const cryptoTippingProviders = { nowpayments, coinbase };
export const otherProviders = { carbon, buysellads };

// All providers combined
export const providers = {
    ...displayProviders,
    ...cryptoProviders,
    ...popunderProviders,
    ...pushProviders,
    ...textProviders,
    ...donationProviders,
    ...cryptoTippingProviders,
    ...otherProviders
};

// Legacy export
export const Ads = providers;

// Priority arrays for fallback logic
export const displayPriority = ['adsense', 'monetag', 'adsterra', 'aads', 'propeller', 'yllix', 'bidvertiser', 'hilltopads', 'revenuehits', 'adcash'];
export const cryptoPriority = ['coinzilla', 'cointraffic', 'bitmedia', 'coinad', 'adshares'];
export const popunderPriority = ['popads', 'popcash', 'clickadu', 'admaven', 'exoclick', 'trafficforce'];
export const pushPriority = ['evadav', 'richads', 'pushhouse', 'tacoloco'];
export const textPriority = ['infolinks', 'medianet'];
export const donationPriority = ['buymeacoffee', 'kofi', 'paypal', 'liberapay', 'nowpayments', 'coinbase'];
