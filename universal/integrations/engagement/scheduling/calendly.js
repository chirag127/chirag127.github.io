/**
 * Calendly Scheduling Integration
 */
export const calendly = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.username || this.loaded) return;

        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://assets.calendly.com/assets/external/widget.css';
        document.head.appendChild(link);

        const script = document.createElement('script');
        script.src = 'https://assets.calendly.com/assets/external/widget.js';
        script.async = true;
        document.head.appendChild(script);

        this.username = config.username;
        this.loaded = true;
        console.log('[Calendly] Loaded');
    },

    embed(containerId, eventType = '') {
        const container = document.getElementById(containerId);
        if (!container) return;

        const url = `https://calendly.com/${this.username}${eventType ? '/' + eventType : ''}`;
        container.innerHTML = `
            <div class="calendly-inline-widget"
                 data-url="${url}"
                 style="min-width:320px;height:630px;">
            </div>
        `;
    },

    openPopup(eventType = '') {
        if (!window.Calendly) return;
        const url = `https://calendly.com/${this.username}${eventType ? '/' + eventType : ''}`;
        window.Calendly.initPopupWidget({ url });
    }
};
