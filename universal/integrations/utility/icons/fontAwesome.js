/**
 * FontAwesome Integration
 */
export const fontAwesome = {
    loaded: false,

    init(config) {
        if (!config.enabled || this.loaded) return;

        if (config.kitCode) {
            // Kit-based loading (recommended)
            const script = document.createElement('script');
            script.src = `https://kit.fontawesome.com/${config.kitCode}.js`;
            script.crossOrigin = 'anonymous';
            script.defer = true;
            document.head.appendChild(script);
        } else {
            // CDN fallback (Free icons only)
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css';
            link.integrity = 'sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==';
            link.crossOrigin = 'anonymous';
            link.referrerPolicy = 'no-referrer';
            document.head.appendChild(link);
        }

        this.loaded = true;
        console.log('[FontAwesome] Loaded');
    }
};
