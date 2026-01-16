/**
 * Unified Monitoring Module
 * Consolidates error tracking/monitoring integrations.
 */

export const Monitoring = {
    sentry: {
        init: (config, loadScript) => {
            if (!config.dsn) return;
            loadScript('https://js.sentry-cdn.com/' + config.dsn.split('@')[0].split('//')[1] + '.min.js')
                .then(() => {
                    // Sentry loader script usually initializes itself via the CDN logic,
                    // or we can init explicitly if using the bundle.
                    // For modern Sentry loader, just the script tag with the public key is enough often.
                    // But if strict explicit init is needed:
                    if (window.Sentry) {
                        Sentry.init({ dsn: config.dsn });
                    }
                });
        }
    },
    honeybadger: {
        init: (config, loadScript) => {
            if (!config.key) return;
            loadScript('//js.honeybadger.io/v3.2/honeybadger.min.js')
                .then(() => {
                    if (window.Honeybadger) {
                        Honeybadger.configure({ apiKey: config.key });
                    }
                });
        }
    },
    bugsnag: {
        init: (config, loadScript) => {
            if (!config.key) return;
            loadScript('//d2wy8f7a9ursnm.cloudfront.net/v7/bugsnag.min.js')
                .then(() => {
                   if (window.Bugsnag) Bugsnag.start({ apiKey: config.key });
                });
        }
    },
    glitchtip: {
        init: (config, loadScript) => {
            if (!config.dsn) return;
            // GlitchTip is Sentry compatible
            loadScript('https://browser.sentry-cdn.com/7.54.0/bundle.min.js')
                .then(() => {
                     if (window.Sentry) {
                         Sentry.init({ dsn: config.dsn });
                     }
                });
        }
    }
};
