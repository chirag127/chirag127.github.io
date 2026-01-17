/**
 * Monitoring Configuration
 * Public keys for error monitoring providers
 * @module config/monitoring
 */

export const monitoringConfig = {
    sentry: {
        dsn: 'https://45890ca96ce164182a3c74cca6018e3e@o4509333332164608.ingest.de.sentry.io/4509333334458448',
        enabled: true
    },
    honeybadger: {
        apiKey: 'hbp_x8dJHBTim5uTkF7pIZVqj55X4wedmR11iovM',
        enabled: true
    },
    rollbar: {
        accessToken: '88062048efd74f7c8e11659187da782b',
        enabled: true
    },
    bugsnag: {
        apiKey: '84afb61cb3bf458037f4f15eeab394c4',
        enabled: true
    },
    glitchtip: {
        dsn: 'https://fe8b6978187b4ef09020464050d17b06@app.glitchtip.com/19542',
        enabled: true
    }
};
