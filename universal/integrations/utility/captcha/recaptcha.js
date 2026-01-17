/**
 * Google reCAPTCHA v3 Integration
 */
export const recaptcha = {
    loaded: false,
    ready: false,

    init(config) {
        if (!config.enabled || !config.siteKey || this.loaded) return;

        window.onRecaptchaLoad = () => {
            this.ready = true;
            console.log('[reCAPTCHA] Ready');
        };

        const script = document.createElement('script');
        script.src = `https://www.google.com/recaptcha/api.js?render=${config.siteKey}&onload=onRecaptchaLoad`;
        script.async = true;
        script.defer = true;
        document.head.appendChild(script);

        this.siteKey = config.siteKey;
        this.loaded = true;
    },

    async execute(action = 'submit') {
        if (!this.ready) {
            console.warn('[reCAPTCHA] Not ready yet');
            return null;
        }
        return new Promise((resolve) => {
            window.grecaptcha.ready(() => {
                window.grecaptcha.execute(this.siteKey, { action }).then(resolve);
            });
        });
    }
};
