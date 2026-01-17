/**
 * Part 3: BaaS - Database
 * Cloud databases for client-side apps
 * @module config/baas/database
 */

export const database = {
    // BIG TECH - Google Firebase
    firestore: {
        projectId: 'fifth-medley-408209',
        enabled: true  // YOUR PROJECT
    },

    // ALTERNATIVES
    supabase: { url: '', anonKey: '', enabled: false },  // Open source Postgres
    surrealdb: { endpoint: '', enabled: false }
};

export const database_priority = ['firestore', 'supabase'];
