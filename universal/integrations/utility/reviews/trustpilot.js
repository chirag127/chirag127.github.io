/**
 * Trustpilot Reviews Widget Integration
 */
export const trustpilot = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.businessUnitId || this.loaded) return;

        const script = document.createElement('script');
        script.src = '//widget.trustpilot.com/bootstrap/v5/tp.widget.bootstrap.min.js';
        script.async = true;
        script.onload = () => {
            this.ready = true;
            console.log('[Trustpilot] Ready');
        };
        document.head.appendChild(script);

        this.businessUnitId = config.businessUnitId;
        this.loaded = true;
    },

    render(containerId, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.className = 'trustpilot-widget';
        container.dataset.locale = options.locale || 'en-US';
        container.dataset.templateId = options.templateId || '53aa8807dec7e10d38f59f32';
        container.dataset.businessunitId = this.businessUnitId;
        container.dataset.styleHeight = options.height || '150px';
        container.dataset.styleWidth = options.width || '100%';
        container.dataset.theme = options.theme || 'light';

        if (window.Trustpilot) {
            window.Trustpilot.loadFromElement(container, true);
        }
    }
};
