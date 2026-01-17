/**
 * Monitoring Providers Index
 * Aggregates all monitoring provider modules
 * @module monitoring
 */

import * as sentry from './sentry.js';
import * as honeybadger from './honeybadger.js';
import * as bugsnag from './bugsnag.js';
import * as glitchtip from './glitchtip.js';
import * as rollbar from './rollbar.js';

// Export individual providers
export {
    sentry,
    honeybadger,
    bugsnag,
    glitchtip,
    rollbar
};

// Export providers object for dynamic iteration
export const providers = {
    sentry,
    honeybadger,
    bugsnag,
    glitchtip,
    rollbar
};

// Legacy export for backward compatibility
export const Monitoring = providers;
