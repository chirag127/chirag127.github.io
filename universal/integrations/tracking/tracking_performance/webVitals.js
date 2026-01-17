/**
 * Web Vitals Integration
 */
export const webVitals = {
    loaded: false,
    metrics: {},

    init(config) {
        if (!config.enabled || this.loaded) return;

        const script = document.createElement('script');
        script.src = 'https://unpkg.com/web-vitals@3/dist/web-vitals.iife.js';
        script.onload = () => {
            const { onCLS, onFID, onFCP, onLCP, onTTFB, onINP } = window.webVitals;

            const handleMetric = (metric) => {
                this.metrics[metric.name] = metric.value;
                console.log(`[WebVitals] ${metric.name}:`, metric.value);

                // Send to analytics if configured
                if (config.sendToAnalytics && window.gtag) {
                    window.gtag('event', metric.name, {
                        value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
                        event_label: metric.id,
                        non_interaction: true
                    });
                }
            };

            onCLS(handleMetric);
            onFID(handleMetric);
            onFCP(handleMetric);
            onLCP(handleMetric);
            onTTFB(handleMetric);
            onINP(handleMetric);

            this.ready = true;
            console.log('[WebVitals] Ready');
        };
        document.head.appendChild(script);

        this.loaded = true;
    },

    getMetrics() {
        return this.metrics;
    }
};
