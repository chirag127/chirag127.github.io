/**
 * OneSignal Push Notifications Provider
 * @module engagement/onesignal
 */

export const name = 'onesignal';
export const configKey = 'onesignal';

export function init(config, loadScript) {
    if (!config.appId || !config.enabled) return;

    // OneSignal SDK
    window.OneSignal = window.OneSignal || [];

    // Load OneSignal
    loadScript('https://cdn.onesignal.com/sdks/OneSignalSDK.js')
        .then(() => {
            OneSignal.push(function() {
                OneSignal.init({
                    appId: config.appId,
                    safari_web_id: config.safari_web_id,
                    notifyButton: {
                        enable: true
                    },
                    welcomeNotification: {
                        title: "Thanks for subscribing!",
                        message: "You'll receive updates from us."
                    }
                });
            });
        });
}
