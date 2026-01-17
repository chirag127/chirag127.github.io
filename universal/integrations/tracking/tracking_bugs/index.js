/**
 * Tracking - Bug Tracking Integrations
 * @module integrations/tracking/tracking_bugs
 */
import { sentry } from './sentry.js';
import { bugsnag } from './bugsnag.js';
import { rollbar } from './rollbar.js';
import { honeybadger } from './honeybadger.js';
import { glitchtip } from './glitchtip.js';

export const tracking_bugs = {
    sentry, bugsnag, rollbar, honeybadger, glitchtip
};
