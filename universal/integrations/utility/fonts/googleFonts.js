/**
 * Google Fonts Integration
 * Loads Google Fonts dynamically based on configuration
 */
export const googleFonts = {
    loaded: false,

    init(config) {
        if (!config.enabled || this.loaded) return;

        const families = config.families || ['Inter:wght@400;500;600;700'];
        const familyString = families.map(f => f.replace(/ /g, '+')).join('&family=');

        // Preconnect for performance
        const preconnect1 = document.createElement('link');
        preconnect1.rel = 'preconnect';
        preconnect1.href = 'https://fonts.googleapis.com';
        document.head.appendChild(preconnect1);

        const preconnect2 = document.createElement('link');
        preconnect2.rel = 'preconnect';
        preconnect2.href = 'https://fonts.gstatic.com';
        preconnect2.crossOrigin = 'anonymous';
        document.head.appendChild(preconnect2);

        // Load stylesheet
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = `https://fonts.googleapis.com/css2?family=${familyString}&display=swap`;
        document.head.appendChild(link);

        this.loaded = true;
        console.log('[GoogleFonts] Loaded:', families);
    }
};
