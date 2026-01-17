export const fontAwesome = {
    init: (config) => {
        if (!config.enabled || !config.kitCode) return;
        const script = document.createElement('script');
        script.src = `https://kit.fontawesome.com/${config.kitCode}.js`;
        script.crossOrigin = 'anonymous';
        document.head.appendChild(script);
    }
};
