/**
 * Part 2: Tracking - Auth/Firebase (ALL user IDs)
 * @module config/tracking/auth
 */

export const auth = {
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
    supabase: { url: '', anonKey: '', enabled: false },
    auth0: { domain: '', clientId: '', enabled: false },
    clerk: { publishableKey: '', enabled: false },
    appwrite: { endpoint: '', projectId: '', enabled: false }
};

export const auth_priority = ['firebase', 'supabase', 'auth0', 'clerk', 'appwrite'];
