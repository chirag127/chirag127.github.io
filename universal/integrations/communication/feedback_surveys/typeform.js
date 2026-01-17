/**
 * Typeform Integration
 */
export const typeform = {
    loaded: false,

    init(config) {
        if (!config.enabled || this.loaded) return;

        const script = document.createElement('script');
        script.src = '//embed.typeform.com/next/embed.js';
        script.async = true;
        script.onload = () => {
            this.ready = true;
            console.log('[Typeform] Ready');
        };
        document.head.appendChild(script);

        this.loaded = true;
    },

    embed(containerId, formId, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.dataset.tfWidget = formId;
        container.dataset.tfInlineOnMobile = 'true';
        container.dataset.tfMedium = 'snippet';
        container.style.width = options.width || '100%';
        container.style.height = options.height || '500px';

        if (window.tf) {
            window.tf.createWidget();
        }
    },

    popup(formId, options = {}) {
        if (!window.tf) return;

        window.tf.createPopup(formId, {
            mode: options.mode || 'popup',
            size: options.size || 70,
            autoClose: options.autoClose || 3000
        }).open();
    }
};
