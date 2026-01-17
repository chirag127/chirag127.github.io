/**
 * OneTrust Cookie Consent Integration
 */
export const onetrust = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.domainId || this.loaded) return;

        const script = document.createElement('script');
        script.src = `https://cdn.cookielaw.org/scripttemplates/otSDKStub.js`;
        script.dataset.domainScript = config.domainId;
        script.type = 'text/javascript';
        script.charset = 'UTF-8';
        document.head.appendChild(script);

        // OptanonWrapper callback
        window.OptanonWrapper = function() {
            console.log('[OneTrust] Consent updated');
        };

        this.loaded = true;
        console.log('[OneTrust] Loaded:', config.domainId);
    }
};
