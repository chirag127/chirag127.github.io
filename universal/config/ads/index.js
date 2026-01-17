/**
 * Ads Configuration Index
 * Aggregates all ad-related configs
 *
 * @module config/ads
 */

export { displayAdsConfig, displayAdsPriority } from './display.config.js';
export { cryptoAdsConfig, cryptoAdsPriority } from './crypto.config.js';
export { popunderAdsConfig, popunderAdsPriority, popunderLimits } from './popunder.config.js';
export { pushAdsConfig, pushAdsPriority } from './push.config.js';
export { textAdsConfig, textAdsPriority, affiliateLinkServices } from './text.config.js';
export { donationsConfig, donationsPriority } from './donations.config.js';
export { affiliatesConfig } from './affiliates.config.js';

// Combined ads config
import { displayAdsConfig } from './display.config.js';
import { cryptoAdsConfig } from './crypto.config.js';
import { popunderAdsConfig, popunderLimits } from './popunder.config.js';
import { pushAdsConfig } from './push.config.js';
import { textAdsConfig } from './text.config.js';
import { donationsConfig } from './donations.config.js';
import { affiliatesConfig } from './affiliates.config.js';

export const allAdsConfig = {
    display: displayAdsConfig,
    crypto: cryptoAdsConfig,
    popunder: popunderAdsConfig,
    popunderLimits,
    push: pushAdsConfig,
    text: textAdsConfig,
    donations: donationsConfig,
    affiliates: affiliatesConfig
};
