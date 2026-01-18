/**
 * Part 3: BaaS - Headless CMS
 * Content management for static sites
 * @module config/baas/cms
 */

export const cms = {
    // Contentful - Headless CMS
    // Feature: Flexible content model, GraphQL API
    // Free Limit: 25k records, 2TB bandwidth/mo, 5 users
    contentful: { spaceId: '', accessToken: '', enabled: false },

    // Sanity - Headless CMS
    // Feature: Real-time collaboration, structured content (Groq)
    // Free Limit: Generous free tier, pay-as-you-go overages
    sanity: { projectId: '', dataset: '', enabled: false },

    // Strapi - Headless CMS
    // Feature: 100% JavaScript, Self-hosted or Cloud
    // Free Limit: Self-hosted is free (Community Edition), Cloud starts paid
    strapi: { apiUrl: '', enabled: false }
};

export const cms_priority = ['contentful', 'sanity'];
