/**
 * BaaS - Database Integrations
 * @module integrations/baas/database
 */

import * as firestore from './firestore.js';
import * as supabase from './supabase.js';
import * as surrealdb from './surrealdb.js';

export const database = {
    firestore, supabase, surrealdb
};
