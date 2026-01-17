export const googleSearchConsole = {
    init: (config) => {
        if (!config.enabled || !config.verificationTag) return;
        const meta = document.createElement('meta');
        meta.name = "google-site-verification";
        meta.content = config.verificationTag;
        document.head.appendChild(meta);
    }
};
