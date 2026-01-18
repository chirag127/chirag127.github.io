/**
 * Part 3: BaaS - Headless CMS (Content Management Systems)
 * Manage and deliver content for static sites without a traditional backend
 * @module config/baas/cms
 */

export const cms = {
    // ============================================================================
    // CONTENTFUL - Industry-Leading Headless CMS
    // ============================================================================
    // What it does:
    // - Provides API-first content management with flexible content modeling
    // - Delivers content via REST and GraphQL APIs
    // - Offers real-time content preview and multi-language support
    // - Includes built-in image optimization and CDN delivery
    //
    // What it doesn't do:
    // - No built-in authentication/user management
    // - No file storage beyond content assets
    // - No server-side logic execution
    //
    // Free Tier Limits (Community Plan):
    // - 25,000 records (content entries)
    // - 2TB bandwidth per month
    // - 5 users (team members)
    // - 2 locales (languages)
    // - 48 content types
    // - Unlimited API calls
    //
    // Best for: Marketing sites, blogs, documentation, e-commerce product catalogs
    // Website: https://www.contentful.com
    contentful: { spaceId: '', accessToken: '', enabled: false },

    // ============================================================================
    // SANITY - Real-Time Collaborative CMS
    // ============================================================================
    // What it does:
    // - Real-time collaborative editing (multiple users simultaneously)
    // - Structured content with GROQ query language (like GraphQL but simpler)
    // - Customizable editing interface (Sanity Studio)
    // - Built-in image pipeline and asset management
    // - Version history and content scheduling
    //
    // What it doesn't do:
    // - No built-in hosting (you host Sanity Studio yourself)
    // - No user authentication system
    // - No email/notification services
    //
    // Free Tier Limits (Free Plan):
    // - Unlimited documents and API requests
    // - 3 users (non-admin)
    // - 10GB bandwidth per month
    // - 5GB assets storage
    // - 2 datasets
    // - Pay-as-you-go for overages (very affordable)
    //
    // Best for: News sites, collaborative content teams, real-time applications
    // Website: https://www.sanity.io
    sanity: { projectId: '', dataset: '', enabled: false },

    // ============================================================================
    // STRAPI - Open Source Headless CMS
    // ============================================================================
    // What it does:
    // - 100% JavaScript/Node.js based CMS
    // - Self-hosted (full control) or cloud-hosted options
    // - Built-in REST and GraphQL APIs
    // Strapi - Headless CMS
    // Feature: 100% JavaScript, Self-hosted or Cloud. REST & GraphQL.
    // Free Limit (Cloud): 10k requests/mo, 10GB storage, 10GB bandwidth, 500 DB entries.
    // Free Limit (Self-Hosted): Unlimited (depends on your server). The "Free Forever" choice if you host it.
    strapi: { apiUrl: '', enabled: false }
};

export const cms_priority = ['sanity', 'contentful', 'strapi'];

// Made with Bob
