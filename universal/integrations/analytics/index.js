/**
 * Analytics Providers Index
 * Aggregates all analytics provider modules
 * @module analytics
 */

import * as ga4 from './ga4.js';
import * as yandex from './yandex.js';
import * as clarity from './clarity.js';
import * as posthog from './posthog.js';
import * as umami from './umami.js';
import * as cloudflare from './cloudflare.js';
import * as mixpanel from './mixpanel.js';
import * as goatcounter from './goatcounter.js';
import * as heap from './heap.js';
import * as logrocket from './logrocket.js';
import * as amplitude from './amplitude.js';
import * as beam from './beam.js';
import * as counterdev from './counterdev.js';
import * as cronitor from './cronitor.js';

// Export individual providers
export {
    ga4,
    yandex,
    clarity,
    posthog,
    umami,
    cloudflare,
    mixpanel,
    goatcounter,
    heap,
    logrocket,
    amplitude,
    beam,
    counterdev,
    cronitor
};

// Export providers object for dynamic iteration
export const providers = {
    ga4,
    yandex,
    clarity,
    posthog,
    umami,
    cloudflare,
    mixpanel,
    goatcounter,
    heap,
    logrocket,
    amplitude,
    beam,
    counterdev,
    cronitor
};

// Legacy export for backward compatibility
export const Analytics = providers;
