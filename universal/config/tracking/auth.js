/**
 * Part 2: Tracking - User Authentication & Identity
 * SECURITY FOCUS: Managing User Access
 * @module config/tracking/auth
 */

export const auth = {
    // ============================================================================
    // FIREBASE AUTH (Google)
    // ============================================================================
    // Description:
    // Scalable, secure auth for web and mobile.
    //
    // Key Features:
    // - One-click social login (Google, Facebook, GitHub, etc).
    // - Passwordless (email link) login.
    // - Anonymous auth.
    //
    // Free Limits (2025):
    // - **50,000 Monthly Active Users (MAUs)** (Standard auth).
    // - Huge scalability for hobbyist and startup projects.
    //
    firebase: {
        apiKey: 'AIzaSyCx--SPWCNaIY5EJpuJ_Hk28VtrVhBo0Ng',
        authDomain: 'fifth-medley-408209.firebaseapp.com',
        projectId: 'fifth-medley-408209',
        enabled: true
    },

    // ============================================================================
    // CLERK - The Developer Experience King
    // ============================================================================
    // Description:
    // Modern user management with pre-built UI components.
    //
    // Key Features:
    // - Beautiful "drop-in" components.
    // - Built-in Multi-Factor Authentication (MFA).
    //
    // Free Limits (2025):
    // - **10,000 Monthly Active Users (MAUs)**.
    // - Unlimited social logins.
    //
    clerk: { publishableKey: '', enabled: false },

    // ============================================================================
    // SUPABASE AUTH
    // ============================================================================
    // Description:
    // Open source alternative to Firebase Auth.
    //
    // Free Limits:
    // - **50,000 MAUs**.
    //
    supabase: { url: '', anonKey: '', enabled: false },

    // ============================================================================
    // AUTH0 (Okta)
    // ============================================================================
    // Description:
    // Enterprise-grade identity management.
    //
    // Free Limits (2025):
    // - **7,500 MAUs** (Recently increased from 7,000).
    // - Up to 10 Social Connections.
    //
    auth0: { domain: '', clientId: '', enabled: false }
};

export const auth_priority = ['firebase', 'supabase', 'clerk', 'auth0'];
