/**
 * Authentication Configuration
 * Auth providers for user management
 *
 * @module config/auth
 */

export const authConfig = {

    // =========================================================================
    // FIREBASE - Google's auth platform
    // =========================================================================
    // HOW TO GET: https://console.firebase.google.com/
    // 1. Create project
    // 2. Add web app
    // 3. Enable Authentication
    // 4. Copy config object
    firebase: {
        apiKey: 'AIzaSyCx--SPWCNaIY5EJpuJ_Hk28VtrVhBo0Ng',  // YOUR EXISTING KEY
        authDomain: 'fifth-medley-408209.firebaseapp.com',
        projectId: 'fifth-medley-408209',
        storageBucket: 'fifth-medley-408209.firebasestorage.app',
        messagingSenderId: '1017538017299',
        appId: '1:1017538017299:web:bd8ccb096868a6f394e7e6',
        measurementId: 'G-BPSZ007KGR',
        enabled: true
    },

    // =========================================================================
    // SUPABASE - Open source Firebase alternative
    // =========================================================================
    // HOW TO GET: https://supabase.com/
    // 1. Create project
    // 2. Get URL and anon key from Settings -> API
    supabase: {
        url: '',
        anonKey: '',
        enabled: false
    },

    // =========================================================================
    // AUTH0 - Enterprise auth
    // =========================================================================
    // HOW TO GET: https://auth0.com/
    // 1. Create tenant
    // 2. Create application
    // 3. Get domain and client ID
    auth0: {
        domain: '',
        clientId: '',
        enabled: false
    },

    // =========================================================================
    // CLERK - Modern auth
    // =========================================================================
    // HOW TO GET: https://clerk.com/
    // 1. Create application
    // 2. Get publishable key
    clerk: {
        publishableKey: '',
        enabled: false
    },

    // =========================================================================
    // APPWRITE - Open source backend
    // =========================================================================
    // HOW TO GET: https://appwrite.io/
    // 1. Create project
    // 2. Get endpoint and project ID
    appwrite: {
        endpoint: '',
        projectId: '',
        enabled: false
    },

    // =========================================================================
    // USERFRONT - Auth for React
    // =========================================================================
    // HOW TO GET: https://userfront.com/
    // 1. Create workspace
    // 2. Get tenant ID
    userfront: {
        tenantId: '',
        enabled: false
    }
};

// Auth priority - use first enabled
export const authPriority = [
    'firebase',   // Primary
    'supabase',
    'auth0',
    'clerk',
    'appwrite'
];
