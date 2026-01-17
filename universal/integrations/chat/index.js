/**
 * Chat Providers Index
 * @module chat
 */

import * as tawkto from './tawkto.js';
import * as crisp from './crisp.js';
import * as intercom from './intercom.js';
import * as drift from './drift.js';
import * as tidio from './tidio.js';

export { tawkto, crisp, intercom, drift, tidio };

export const providers = { tawkto, crisp, intercom, drift, tidio };
export const Chat = providers;

// Priority for fallback
export const chatPriority = ['tawk', 'crisp', 'tidio', 'drift', 'intercom'];
