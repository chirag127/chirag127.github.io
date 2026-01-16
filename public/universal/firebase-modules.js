/* FIREBASE V12 MODULE LOADER
   Hosted at: /universal/firebase-modules.js
*/

import { initializeApp } from "https://www.gstatic.com/firebasejs/12.8.0/firebase-app.js";
import { getAnalytics, logEvent } from "https://www.gstatic.com/firebasejs/12.8.0/firebase-analytics.js";
import { getFirestore, doc, setDoc, updateDoc, arrayUnion, serverTimestamp } from "https://www.gstatic.com/firebasejs/12.8.0/firebase-firestore.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/12.8.0/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyCx--SPWCNaIY5EJpuJ_Hk28VtrVhBo0Ng",
    authDomain: "fifth-medley-408209.firebaseapp.com",
    projectId: "fifth-medley-408209",
    storageBucket: "fifth-medley-408209.firebasestorage.app",
    messagingSenderId: "1017538017299",
    appId: "1:1017538017299:web:bd8ccb096868a6f394e7e6",
    measurementId: "G-BPSZ007KGR"
};

// Initialize
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const db = getFirestore(app);
const auth = getAuth(app);

// Data Collection Logic
async function collectUserEdge() {
    const pagePath = window.location.pathname;
    const deviceData = {
        userAgent: navigator.userAgent,
        language: navigator.language,
        platform: navigator.platform,
        screen: `${window.screen.width}x${window.screen.height}`,
        referrer: document.referrer || "direct",
        timestamp: new Date().toISOString()
    };

    // Standard Analytics Log
    logEvent(analytics, 'page_view', { page_path: pagePath });

    // Custom Firestore Logging
    try {
        let userId = auth.currentUser ? auth.currentUser.uid : 'anon_' + Math.random().toString(36).substr(2, 9);
        const userRef = doc(db, "site_visits", userId);

        await setDoc(userRef, {
            last_visit: serverTimestamp(),
            visits: arrayUnion({
                url: window.location.href,
                time: new Date().toISOString(),
                ...deviceData
            })
        }, { merge: true });

        console.log("🔥 [Firebase] Edge data synced.");
    } catch (e) {
        console.error("🔥 [Firebase] Sync failed:", e);
    }
}

collectUserEdge();

export { app, analytics, db, auth };
