/**
 * Auth Configuration
 * Public keys for authentication providers
 * @module config/auth
 */

export const authConfig = {
    auth0: {
        domain: '',
        clientId: '',
        enabled: false
    },
    clerk: {
        publishableKey: '',
        enabled: false
    },
    supabase: {
        url: '',
        anonKey: '',
        enabled: false
    },
    firebase: {
        apiKey: '',
        authDomain: '',
        projectId: '',
        enabled: false
    }
};
