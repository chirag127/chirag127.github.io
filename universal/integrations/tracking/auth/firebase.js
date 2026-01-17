/**
 * Firebase Authentication Integration
 */
export const firebase = {
    loaded: false,
    app: null,
    auth: null,

    init(config) {
        if (!config.enabled || !config.apiKey || this.loaded) return;

        // Load Firebase SDK
        const script = document.createElement('script');
        script.src = 'https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js';
        script.onload = () => {
            const authScript = document.createElement('script');
            authScript.src = 'https://www.gstatic.com/firebasejs/10.7.0/firebase-auth-compat.js';
            authScript.onload = () => {
                // Initialize Firebase
                this.app = window.firebase.initializeApp({
                    apiKey: config.apiKey,
                    authDomain: config.authDomain,
                    projectId: config.projectId,
                    storageBucket: config.storageBucket,
                    messagingSenderId: config.messagingSenderId,
                    appId: config.appId,
                    measurementId: config.measurementId
                });

                this.auth = window.firebase.auth();
                this.ready = true;
                console.log('[Firebase] Ready:', config.projectId);
            };
            document.head.appendChild(authScript);
        };
        document.head.appendChild(script);

        this.loaded = true;
    },

    async signInWithGoogle() {
        if (!this.auth) return null;
        const provider = new window.firebase.auth.GoogleAuthProvider();
        return this.auth.signInWithPopup(provider);
    },

    async signInWithEmail(email, password) {
        if (!this.auth) return null;
        return this.auth.signInWithEmailAndPassword(email, password);
    },

    async signUp(email, password) {
        if (!this.auth) return null;
        return this.auth.createUserWithEmailAndPassword(email, password);
    },

    async signOut() {
        if (!this.auth) return;
        return this.auth.signOut();
    },

    getCurrentUser() {
        return this.auth ? this.auth.currentUser : null;
    },

    onAuthStateChanged(callback) {
        if (this.auth) {
            this.auth.onAuthStateChanged(callback);
        }
    }
};
