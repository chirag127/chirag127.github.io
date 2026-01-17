/**
 * Push Notification Monetization Configuration
 * Users subscribe to receive push notifications with ads
 *
 * PRIVACY: User must explicitly consent (browser prompt)
 * REVENUE: Passive income after subscription
 *
 * @module config/ads/push
 */

export const pushAdsConfig = {

    // =========================================================================
    // ONESIGNAL - Best free tier, not just for ads
    // =========================================================================
    // HOW TO GET: https://onesignal.com/
    // 1. Sign up at https://onesignal.com/
    // 2. Create new app (Web Push)
    // 3. Configure your domain
    // 4. Get App ID
    // PAYOUT: This is for YOUR notifications, not monetization
    // TIP: Use for re-engagement, combine with push ad networks
    onesignal: {
        enabled: true,
        appId: '',  // Your OneSignal App ID
        safari_web_id: ''  // For Safari support
    },

    // =========================================================================
    // PUSHENGAGE - Commercial push monetization
    // =========================================================================
    // HOW TO GET: https://www.pushengage.com/
    // 1. Sign up at https://www.pushengage.com/
    // 2. Add your website
    // 3. Get API key and site key
    // PAYOUT: Revenue share on ad pushes
    pushengage: {
        enabled: false,
        siteKey: ''
    },

    // =========================================================================
    // EVADAV - Push notification specialist
    // =========================================================================
    // HOW TO GET: https://evadav.com/
    // 1. Register at https://evadav.com/
    // 2. Add website as publisher
    // 3. Get integration code
    // PAYOUT: $25 minimum
    evadav: {
        enabled: true,
        publisherId: '',
        siteId: ''
    },

    // =========================================================================
    // RICHADS - Push and pop network
    // =========================================================================
    // HOW TO GET: https://richads.com/
    // 1. Sign up as publisher
    // 2. Add your domain
    // 3. Install service worker
    // PAYOUT: $10 minimum
    richads: {
        enabled: false,
        publisherId: ''
    },

    // =========================================================================
    // PUSH.HOUSE - Monetize push subscribers
    // =========================================================================
    // HOW TO GET: https://push.house/
    // 1. Register at https://push.house/
    // 2. Verify website
    // 3. Get code
    // PAYOUT: Various options
    pushHouse: {
        enabled: false,
        publisherId: ''
    },

    // =========================================================================
    // TACOLOCO - Push monetization
    // =========================================================================
    // HOW TO GET: https://tacoloco.com/
    // 1. Sign up
    // 2. Add site
    // PAYOUT: Varies
    tacoloco: {
        enabled: false,
        publisherId: ''
    }
};

// Priority order for push networks
export const pushAdsPriority = [
    'onesignal',   // Use for your own notifications first
    'evadav',      // Then monetize
    'pushengage',
    'richads',
    'pushHouse',
    'tacoloco'
];
