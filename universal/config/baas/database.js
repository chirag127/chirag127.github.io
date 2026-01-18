/**
 * Part 3: BaaS - Database
 * Cloud databases for client-side apps
 * @module config/baas/database
 */

export const database = {
    // BIG TECH - Google Firebase
    // Feature: Real-time NoSQL, Authentication included
    // Free Limit: 1GB storage, 10GB transfer, 50k reads/day (Spark Plan)
    firestore: {
        projectId: 'fifth-medley-408209',
        enabled: true  // YOUR PROJECT
    },

    // ALTERNATIVES
    // Supabase - Open Source Firebase Alternative
    // Feature: Postgres DB, Auth, Storage, Realtime
    // Free Limit: 500MB database, 1GB file storage, 2GB bandwidth
    supabase: { url: '', anonKey: '', enabled: false },

    // SurrealDB - Multi-model Database
    // Feature: SQL, NoSQL, Graph combined
    // Free Limit: Open Source (Self-host free), Cloud has beta free tier
    surrealdb: { endpoint: '', enabled: false }
};

export const database_priority = ['firestore', 'supabase'];
