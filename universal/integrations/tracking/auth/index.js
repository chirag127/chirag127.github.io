/**
 * Auth Index
 */
import { firebase } from './firebase.js';
import { supabase } from './supabase.js';
import { auth0 } from './auth0.js';
import { clerk } from './clerk.js';
import { appwrite } from './appwrite.js';

export const auth = { firebase, supabase, auth0, clerk, appwrite };
