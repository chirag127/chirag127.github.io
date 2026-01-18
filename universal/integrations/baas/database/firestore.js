/**
 * BaaS Provider: firestore
 * Category: database
 */

export const name = 'firestore';
export const configKey = 'firestore';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing database/firestore');

    // Use Firebase Compat libraries for easiest CDN global usage
    Promise.all([
        loadScript('https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js', 'firebase-app'),
        loadScript('https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore-compat.js', 'firebase-firestore')
    ]).then(() => {
        if (window.firebase) {
            const app = window.firebase.initializeApp({
                projectId: config.projectId,
                // Add other keys if provided in config, but typically projectId is key for simpler setups or public data
                apiKey: config.apiKey,
                authDomain: config.authDomain,
                storageBucket: config.storageBucket,
                messagingSenderId: config.messagingSenderId,
                appId: config.appId
            });
            window.firestoreDb = app.firestore();
            console.log('[BaaS] Firestore ready as window.firestoreDb');
        }
    });
}
