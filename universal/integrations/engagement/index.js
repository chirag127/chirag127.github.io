/**
 * Engagement Providers Index
 * Social sharing, comments, push notifications
 * @module engagement
 */

import * as addthis from './addthis.js';
import * as disqus from './disqus.js';
import * as onesignal from './onesignal.js';

// Export individual providers
export { addthis, disqus, onesignal };

// Providers object for dynamic iteration
export const providers = { addthis, disqus, onesignal };

// Category groups
export const shareProviders = { addthis };
export const commentProviders = { disqus };
export const pushProviders = { onesignal };
