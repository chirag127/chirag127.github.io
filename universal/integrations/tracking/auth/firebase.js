export const firebase = {
    init: (config) => {
        if (!config.enabled) return;
        // Basic firebase loader
        const script = document.createElement('script');
        script.src = "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
        script.onload = () => {
             // Init logic would go here
             console.log("Firebase loaded");
        };
        document.head.appendChild(script);
    }
};
