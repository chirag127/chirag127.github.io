/**
 * Engagement Providers Index
 * Social sharing, comments, push marketing
 * @module engagement
 */

import * as addthis from './addthis.js';
import * as sharethis from './sharethis.js';
import * as addtoany from './addtoany.js';
import * as disqus from './disqus.js';
import * as onesignal from './onesignal.js';

export { addthis, sharethis, addtoany, disqus, onesignal };

export const providers = { addthis, sharethis, addtoany, disqus, onesignal };

// Sub-categories
export const shareProviders = { addthis, sharethis, addtoany };
export const commentProviders = { disqus };
export const pushProviders = { onesignal };

// Priority arrays
export const sharePriority = ['addthis', 'sharethis', 'addtoany'];
export const commentPriority = ['disqus'];
