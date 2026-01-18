/**
 * APEX Auto-Tracking Module
 * @module integrations/tracking/auto-track
 */

export const name = 'auto_track';
export const configKey = 'auto_track';

// Default config
const defaults = {
    enabled: true,
    trackClicks: true,
    trackForms: true,
    trackUploads: true,
    trackDownloads: true,
    trackScroll: true,
    trackEngagement: true,
    debug: false
};

// State
let engagementStartTime = Date.now();
let isEngaged = true;
let maxScroll = 0;

export function init(config = {}, loadScript) {
    const settings = { ...defaults, ...config };
    if (!settings.enabled) return;

    console.log('[APEX Tracking] Initializing Auto-Tracking...');

    // 1. Click Tracking
    if (settings.trackClicks) {
        document.addEventListener('click', (e) => {
            const element = e.target;

            // Track button clicks
            if (element.matches('button, .btn, input[type="submit"], [role="button"]')) {
                trackEvent('button_click', {
                    element_text: element.textContent.trim().substring(0, 50),
                    element_type: element.tagName.toLowerCase(),
                    element_id: element.id || 'undefined',
                    element_class: element.className
                });
            }

            // Track download clicks
            if (element.matches('a[href*="download"], [data-download], a[download]')) {
                trackEvent('download_click', {
                    element_text: element.textContent.trim(),
                    href: element.href || 'none',
                    file_type: element.href ? element.href.split('.').pop() : 'unknown'
                });
            }

            // Track specific tool actions
            if (element.matches('[data-action], .process-btn, .convert-btn')) {
                trackEvent('tool_action', {
                    action: element.dataset.action || element.textContent.trim(),
                    button_text: element.textContent.trim()
                });
            }
        });
    }

    // 2. File Upload Tracking
    if (settings.trackUploads) {
        document.addEventListener('change', (e) => {
            if (e.target.type === 'file' && e.target.files.length > 0) {
                trackEvent('file_upload', {
                    file_count: e.target.files.length,
                    file_types: Array.from(e.target.files).map(f => f.type).join(','),
                    total_size: Array.from(e.target.files).reduce((acc, f) => acc + f.size, 0)
                });
            }
        });
    }

    // 3. Form Submission Tracking
    if (settings.trackForms) {
        document.addEventListener('submit', (e) => {
            const form = e.target;
            trackEvent('form_submission', {
                form_id: form.id || 'unnamed_form',
                form_action: form.action || 'none'
            });
        });
    }

    // 4. Engagement Tracking (Time on Page)
    if (settings.trackEngagement) {
        let timeOnPage = 0;
        const interval = setInterval(() => {
            // Only count if tab is visible
            if (!document.hidden) {
                timeOnPage += 15;
                if (timeOnPage === 30) trackEvent('engaged_30s');
                if (timeOnPage === 60) trackEvent('engaged_60s');
                if (timeOnPage === 120) trackEvent('engaged_2min');
                if (timeOnPage === 300) trackEvent('engaged_5min');
            }
        }, 15000);

        // Visibility API for session tracking
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                if (isEngaged) {
                    const duration = Math.round((Date.now() - engagementStartTime) / 1000);
                    trackEvent('engagement_session', {
                        duration_seconds: duration,
                        session_type: 'active'
                    });
                    isEngaged = false;
                }
            } else {
                engagementStartTime = Date.now();
                isEngaged = true;
            }
        });

        // Final session tracking
        window.addEventListener('beforeunload', () => {
            if (isEngaged) {
                const duration = Math.round((Date.now() - engagementStartTime) / 1000);
                trackEvent('engagement_session', {
                    duration_seconds: duration,
                    session_type: 'final'
                });
            }
        });
    }

    // 5. Scroll Depth Tracking
    if (settings.trackScroll) {
        window.addEventListener('scroll', throttle(() => {
            const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);

            if (scrollPercent > maxScroll) {
                maxScroll = scrollPercent;
                if (maxScroll >= 25 && maxScroll < 26) trackEvent('scroll_25');
                if (maxScroll >= 50 && maxScroll < 51) trackEvent('scroll_50');
                if (maxScroll >= 75 && maxScroll < 76) trackEvent('scroll_75');
                if (maxScroll >= 90 && maxScroll < 91) trackEvent('scroll_90');
            }
        }, 500));
    }

    // 6. Error Tracking
    window.addEventListener('error', (e) => {
        trackEvent('javascript_error', {
            message: e.message,
            filename: e.filename,
            lineno: e.lineno,
            colno: e.colno
        });
    });

    console.log('[APEX Tracking] Auto-Tracking Active');
}

/**
 * Universal Event Dispatcher
 * Sends events to all initialized analytics providers (GA4, Clarity, Mixpanel, PostHog, etc.)
 */
function trackEvent(eventName, properties = {}) {
    const projectInfo = window.SITE_CONFIG?.project || {};

    const eventData = {
        ...properties,
        project: projectInfo.name || 'unknown_project',
        category: projectInfo.category || 'utility',
        timestamp: new Date().toISOString(),
        url: window.location.href,
        viewport: `${window.innerWidth}x${window.innerHeight}`
    };

    // Google Analytics 4
    if (typeof window.gtag === 'function') {
        window.gtag('event', eventName, eventData);
    }

    // Microsoft Clarity
    if (typeof window.clarity === 'function') {
        window.clarity('event', eventName, eventData);
    }

    // Mixpanel
    if (window.mixpanel && typeof window.mixpanel.track === 'function') {
        window.mixpanel.track(eventName, eventData);
    }

    // PostHog
    if (window.posthog && typeof window.posthog.capture === 'function') {
        window.posthog.capture(eventName, eventData);
    }

    // Amplitude
    if (window.amplitude && typeof window.amplitude.logEvent === 'function') {
        window.amplitude.logEvent(eventName, eventData);
    }

    // Log to console in debug mode
    // console.log(`[Event] ${eventName}`, eventData);
}

// Helper: Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}
