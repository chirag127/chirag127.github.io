/**
 * BaaS - Cms Integrations
 * @module integrations/baas/cms
 */

import * as contentful from './contentful.js';
import * as sanity from './sanity.js';
import * as strapi from './strapi.js';

export const cms = {
    contentful, sanity, strapi
};
