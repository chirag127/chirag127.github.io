/**
 * Part 2: Tracking - Auth/Firebase (ALL user IDs)
 * @module config/tracking/auth
 */

export const auth = {
    // Firebase Auth
    // Feature: The gold standard for serverless auth
    // Free Limit: 50,000 MAUs (Generous)
    firebase: {
        apiKey: 'AIzaSyCx--SPWCNaIY5EJpuJ_Hk28VtrVhBo0Ng',
        authDomain: 'fifth-medley-408209.firebaseapp.com',
        projectId: 'fifth-medley-408209',
        storageBucket: 'fifth-medley-408209.firebasestorage.app',
        messagingSenderId: '1017538017299',
        appId: '1:1017538017299:web:bd8ccb096868a6f394e7e6',
        measurementId: 'G-BPSZ007KGR',
        enabled: true
    },

    // Supabase Auth
    // Feature: SQL based, rigorous security
    // Free Limit: 50,000 MAUs
    supabase: { url: '', anonKey: '', enabled: false },

    // Auth0
    // Feature: Enterprise identity management
    // Free Limit: 7,000 MAUs
    auth0: { domain: '', clientId: '', enabled: false },

    // Clerk
    // Feature: Drop-in React components
    // Free Limit: 5,000 MAUs
    clerk: { publishableKey: '', enabled: false },

    // Appwrite
    // Feature: Open source Firebase alternative
    // Free Limit: Unlimited (Self-hosted)
    appwrite: { endpoint: '', projectId: '', enabled: false }
};

export const auth_priority = ['firebase', 'supabase', 'auth0', 'clerk', 'appwrite'];
