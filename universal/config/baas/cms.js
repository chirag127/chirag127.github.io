/**
 * Part 3: BaaS - Headless CMS
 * Content management for static sites
 * @module config/baas/cms
 */

export const cms = {
    contentful: { spaceId: '', accessToken: '', enabled: false },
    sanity: { projectId: '', dataset: '', enabled: false },
    strapi: { apiUrl: '', enabled: false }
};

export const cms_priority = ['contentful', 'sanity'];
