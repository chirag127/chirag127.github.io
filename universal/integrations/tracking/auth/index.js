/**
 * Auth Index
 */
import * as firebase from './firebase.js';
import * as supabase from './supabase.js';
import * as auth0 from './auth0.js';
import * as clerk from './clerk.js';
import * as appwrite from './appwrite.js';

export const auth = { firebase, supabase, auth0, clerk, appwrite };
