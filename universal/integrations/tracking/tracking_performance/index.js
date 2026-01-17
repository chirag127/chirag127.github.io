/**
 * Performance Tracking Index
 */
import { webVitals } from './webVitals.js';
import { newRelic } from './newRelic.js';
import { datadog } from './datadog.js';

export const tracking_performance = { webVitals, newRelic, datadog };
