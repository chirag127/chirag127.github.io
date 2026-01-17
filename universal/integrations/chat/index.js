/**
 * Chat Providers Index
 * Aggregates all chat provider modules
 * @module chat
 */

import * as tawkto from './tawkto.js';
import * as crisp from './crisp.js';
import * as intercom from './intercom.js';
import * as drift from './drift.js';

// Export individual providers
export {
    tawkto,
    crisp,
    intercom,
    drift
};

// Export providers object for dynamic iteration
export const providers = {
    tawkto,
    crisp,
    intercom,
    drift
};

// Legacy export for backward compatibility
export const Chat = providers;
