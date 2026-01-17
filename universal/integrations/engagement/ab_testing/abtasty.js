/**
 * AB Tasty Integration
 */
export const abtasty = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.accountId || this.loaded) return;

        const script = document.createElement('script');
        script.src = `https://try.abtasty.com/${config.accountId}.js`;
        script.async = true;
        document.head.appendChild(script);

        this.loaded = true;
        console.log('[ABTasty] Loaded:', config.accountId);
    }
};
