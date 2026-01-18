/**
 * Tracking - Bug Tracking Integrations
 * @module integrations/tracking/tracking_bugs
 */
import * as sentry from './sentry.js';
import * as bugsnag from './bugsnag.js';
import * as rollbar from './rollbar.js';
import * as honeybadger from './honeybadger.js';
import * as glitchtip from './glitchtip.js';

export const tracking_bugs = {
    sentry, bugsnag, rollbar, honeybadger, glitchtip
};
