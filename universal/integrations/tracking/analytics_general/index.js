/**
 * Tracking - General Analytics Integrations
 * @module integrations/tracking/analytics_general
 */
import * as ga4 from './ga4.js';
import * as yandex from './yandex.js';
import * as mixpanel from './mixpanel.js';
import * as amplitude from './amplitude.js';
import * as posthog from './posthog.js';
import * as umami from './umami.js';
import * as goatcounter from './goatcounter.js';
import * as heap from './heap.js';
import * as logrocket from './logrocket.js';
import * as beam from './beam.js';
import * as counterdev from './counterdev.js';
import * as cronitor from './cronitor.js';
import * as cloudflare from './cloudflare.js';

export const analytics_general = {
    ga4, yandex, mixpanel, amplitude, posthog, umami, goatcounter,
    heap, logrocket, beam, counterdev, cronitor, cloudflare
};
