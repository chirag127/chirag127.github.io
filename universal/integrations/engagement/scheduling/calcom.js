/**
 * Cal.com Scheduling Integration
 */
export const calcom = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.username || this.loaded) return;

        const script = document.createElement('script');
        script.src = 'https://cal.com/embed.js';
        script.async = true;
        document.head.appendChild(script);

        this.username = config.username;
        this.loaded = true;
        console.log('[Cal.com] Loaded');
    },

    embed(containerId, eventType = '') {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <cal-inline calLink="${this.username}${eventType ? '/' + eventType : ''}"
                        style="width:100%;height:100%;overflow:scroll">
            </cal-inline>
        `;
    }
};
