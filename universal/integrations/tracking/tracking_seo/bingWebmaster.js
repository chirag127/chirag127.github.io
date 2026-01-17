export const bingWebmaster = {
    init: (config) => {
        if (!config.enabled || !config.verificationTag) return;
        const meta = document.createElement('meta');
        meta.name = "msvalidate.01";
        meta.content = config.verificationTag;
        document.head.appendChild(meta);
    }
};
