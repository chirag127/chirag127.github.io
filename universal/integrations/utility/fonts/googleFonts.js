export const googleFonts = {
    init: (config) => {
        if (!config.enabled) return;
        config.families.forEach(family => {
            const link = document.createElement('link');
            link.href = `https://fonts.googleapis.com/css2?family=${family}&display=swap`;
            link.rel = 'stylesheet';
            document.head.appendChild(link);
        });
    }
};
