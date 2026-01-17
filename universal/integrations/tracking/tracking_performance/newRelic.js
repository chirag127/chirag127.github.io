/**
 * New Relic Browser Integration
 */
export const newRelic = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.licenseKey || !config.applicationId || this.loaded) return;

        window.NREUM || (NREUM = {});
        NREUM.init = {
            distributed_tracing: { enabled: true },
            privacy: { cookies_enabled: true },
            ajax: { deny_list: ['bam.nr-data.net'] }
        };
        NREUM.loader_config = {
            accountID: config.accountId || '',
            trustKey: config.trustKey || '',
            agentID: config.agentId || config.applicationId,
            licenseKey: config.licenseKey,
            applicationID: config.applicationId
        };
        NREUM.info = {
            beacon: 'bam.nr-data.net',
            errorBeacon: 'bam.nr-data.net',
            licenseKey: config.licenseKey,
            applicationID: config.applicationId,
            sa: 1
        };

        const script = document.createElement('script');
        script.src = 'https://js-agent.newrelic.com/nr-loader-spa-current.min.js';
        script.async = true;
        document.head.appendChild(script);

        this.loaded = true;
        console.log('[NewRelic] Loaded:', config.applicationId);
    },

    noticeError(error, customAttributes) {
        if (window.newrelic) {
            window.newrelic.noticeError(error, customAttributes);
        }
    },

    setCustomAttribute(name, value) {
        if (window.newrelic) {
            window.newrelic.setCustomAttribute(name, value);
        }
    }
};
