/**
 * Part 2: Tracking - Performance (RUM) & SEO
 * @module config/tracking/tracking_performance
 */

export const tracking_performance = {
    newRelic: { licenseKey: '', applicationId: '', enabled: false },
    datadog: { clientToken: '', applicationId: '', enabled: false },
    pingdom: { siteId: '', enabled: false },
    webVitals: { enabled: true, sendToAnalytics: true }
};

export const tracking_seo = {
    googleSearchConsole: { verificationTag: '', enabled: true },
    bingWebmaster: { verificationTag: '', enabled: true },
    yandexWebmaster: { verificationTag: '', enabled: true }
};

export const tracking_performance_priority = ['webVitals', 'newRelic', 'datadog', 'pingdom'];
export const tracking_seo_priority = ['googleSearchConsole', 'bingWebmaster', 'yandexWebmaster'];
