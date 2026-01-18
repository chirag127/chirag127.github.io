/**
 * Part 3: BaaS - Database
 * Cloud databases for client-side apps
 * @module config/baas/database
 */

export const database = {
    // BIG TECH - Google Firebase (Firestore)
    // Feature: Real-time NoSQL, Authentication included, easy integration
    // Free Limit (Spark Plan): 1GB storage, 10GB bandwidth/mo, 50k reads/day, 20k writes/day.
    // VERY Generous for read-heavy apps.
    firestore: {
        projectId: 'fifth-medley-408209',
        enabled: true  // YOUR PROJECT
    },

    // ALTERNATIVES
    // Supabase - Open Source Firebase Alternative
    // Feature: Postgres DB, Auth, Storage, Realtime, Edge Functions
    // Free Limit: 500MB database, 1GB file storage, 5GB bandwidth (egress), 50k MAU.
    // Excellent "Free Forever" choice for relational data.
    supabase: { url: '', anonKey: '', enabled: false },

    // SurrealDB - Multi-model Database
    // Feature: SQL, NoSQL, Graph combined, realtime queries
    // Free Limit (Cloud): 1GB storage for dataset, limited compute.
    // Good for testing modern graph/multi-model concepts.
    surrealdb: { endpoint: '', enabled: false }
};

export const database_priority = ['firestore', 'supabase', 'surrealdb'];
