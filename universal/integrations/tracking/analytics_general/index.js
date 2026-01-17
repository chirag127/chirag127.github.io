/**
 * Tracking - General Analytics Integrations
 * @module integrations/tracking/analytics_general
 */
import { ga4 } from './ga4.js';
import { yandex } from './yandex.js';
import { mixpanel } from './mixpanel.js';
import { amplitude } from './amplitude.js';
import { posthog } from './posthog.js';
import { umami } from './umami.js';
import { goatcounter } from './goatcounter.js';
import { heap } from './heap.js';
import { logrocket } from './logrocket.js';
import { beam } from './beam.js';
import { counterdev } from './counterdev.js';
import { cronitor } from './cronitor.js';
import { cloudflare } from './cloudflare.js';

export const analytics_general = {
    ga4, yandex, mixpanel, amplitude, posthog, umami, goatcounter,
    heap, logrocket, beam, counterdev, cronitor, cloudflare
};
