/**
 * Ads Providers Index
 * Aggregates all ad provider modules
 * @module ads
 */

import * as propeller from './propeller.js';
import * as adsense from './adsense.js';
import * as coinzilla from './coinzilla.js';
import * as adsterra from './adsterra.js';
import * as carbon from './carbon.js';
import * as buysellads from './buysellads.js';

// Export individual providers
export {
    propeller,
    adsense,
    coinzilla,
    adsterra,
    carbon,
    buysellads
};

// Export providers object for dynamic iteration
export const providers = {
    propeller,
    adsense,
    coinzilla,
    adsterra,
    carbon,
    buysellads
};

// Legacy export for backward compatibility
export const Ads = providers;
