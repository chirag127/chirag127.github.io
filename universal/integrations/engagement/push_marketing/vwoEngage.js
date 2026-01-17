/**
 * VWO Engage (Push Notifications) Integration
 */
export const vwoEngage = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.accountId || this.loaded) return;

        const script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = `https://d27rboub0d9ysq.cloudfront.net/web-push-lib.min.js`;
        script.onload = () => {
            if (window.vwo_web_push) {
                window.vwo_web_push({
                    title: config.title || 'Get Notified',
                    message: config.message || 'Subscribe to receive updates',
                    account_id: config.accountId
                });
            }
        };
        document.head.appendChild(script);

        this.loaded = true;
        console.log('[VWOEngage] Loaded:', config.accountId);
    }
};
