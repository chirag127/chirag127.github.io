/**
 * Heatmaps & Session Recording Providers Index
 * @module heatmaps
 */

// Microsoft Clarity is in analytics since it does both
import * as hotjar from './hotjar.js';
import * as smartlook from './smartlook.js';

export { hotjar, smartlook };

export const providers = { hotjar, smartlook };
