/**
 * Datadog RUM Integration
 */
export const datadog = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.clientToken || !config.applicationId || this.loaded) return;

        const script = document.createElement('script');
        script.src = 'https://www.datadoghq-browser-agent.com/us1/v5/datadog-rum.js';
        script.onload = () => {
            window.DD_RUM.init({
                clientToken: config.clientToken,
                applicationId: config.applicationId,
                site: config.site || 'datadoghq.com',
                service: config.service || 'web-app',
                env: config.env || 'production',
                version: config.version || '1.0.0',
                sessionSampleRate: config.sampleRate || 100,
                sessionReplaySampleRate: config.replaySampleRate || 20,
                trackUserInteractions: true,
                trackResources: true,
                trackLongTasks: true,
                defaultPrivacyLevel: 'mask-user-input'
            });

            window.DD_RUM.startSessionReplayRecording();
            this.ready = true;
            console.log('[Datadog] RUM Ready');
        };
        document.head.appendChild(script);

        this.loaded = true;
    },

    setUser(user) {
        if (window.DD_RUM) {
            window.DD_RUM.setUser(user);
        }
    },

    addError(error, context) {
        if (window.DD_RUM) {
            window.DD_RUM.addError(error, context);
        }
    }
};
