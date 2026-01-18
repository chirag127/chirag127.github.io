/**
 * Part 2: Tracking - Auth/Firebase (ALL user IDs)
 * @module config/tracking/auth
 */

export const auth = {
    // ============================================================================
    // FIREBASE AUTH (Google)
    // ============================================================================
    // Description:
    // The gold standard for serverless authentication.
    // Supports Email/Pass, Social, Phone, Anonymous.
    //
    // Free Limits:
    // - 50,000 Monthly Active Users (MAUs).
    // - Unlimited "Daily" Active Users (legacy concept, basically huge limits).
    // - Free SMS: 10/day (Generous limits primarily for Email/Social).
    //
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

    // ============================================================================
    // SUPABASE AUTH
    // ============================================================================
    // Description:
    // Auth built for Postgres.
    //
    // Free Limits:
    // - 50,000 MAUs.
    //
    supabase: { url: '', anonKey: '', enabled: false },

    // ============================================================================
    // CLERK
    // ============================================================================
    // Description:
    // Beautiful, drop-in React components for auth.
    //
    // Free Limits:
    // - 10,000 MAUs.
    //
    clerk: { publishableKey: '', enabled: false },

    // ============================================================================
    // AUTH0
    // ============================================================================
    // Description:
    // Enterprise identity management.
    //
    // Free Limits:
    // - 7,000 MAUs.
    //
    auth0: { domain: '', clientId: '', enabled: false },

    // ============================================================================
    // APPWRITE
    // ============================================================================
    // Description:
    // Open source backend server.
    //
    // Free Limits:
    // - Unlimited (Self-hosted).
    // - Cloud: 75,000 MAUs.
    //
    appwrite: { endpoint: '', projectId: '', enabled: false }
};

export const auth_priority = ['firebase', 'supabase', 'clerk', 'appwrite', 'auth0'];
