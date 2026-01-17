/**
 * Social Sharing & Engagement Configuration
 * Share buttons, comments, social proof
 *
 * @module config/engagement
 */

export const engagementConfig = {

    // =========================================================================
    // SOCIAL SHARE BUTTONS
    // =========================================================================

    // -------------------------------------------------------------------------
    // ADDTHIS - Classic share buttons
    // -------------------------------------------------------------------------
    // HOW TO GET: https://www.addthis.com/
    // 1. Sign up
    // 2. Create tool (share buttons)
    // 3. Get profile ID (ra-XXXXXXXX)
    addThis: {
        profileId: '',
        enabled: true
    },

    // -------------------------------------------------------------------------
    // SHARETHIS - Floating share bars
    // -------------------------------------------------------------------------
    // HOW TO GET: https://sharethis.com/
    // 1. Sign up
    // 2. Configure buttons
    // 3. Get property ID
    shareThis: {
        propertyId: '',
        enabled: false  // Fallback to AddThis
    },

    // -------------------------------------------------------------------------
    // ADDTOANY - Lightweight universal
    // -------------------------------------------------------------------------
    // HOW TO GET: https://www.addtoany.com/
    // 1. Get code directly from website
    // 2. No signup required
    addToAny: {
        enabled: false  // Fallback
    },

    // =========================================================================
    // COMMENT SYSTEMS
    // =========================================================================

    // -------------------------------------------------------------------------
    // DISQUS - Most popular comment system
    // -------------------------------------------------------------------------
    // HOW TO GET: https://disqus.com/
    // 1. Sign up
    // 2. Create site
    // 3. Get shortname
    // TIP: Can enable ads within Disqus for additional revenue
    disqus: {
        shortname: '',
        enabled: true
    },

    // -------------------------------------------------------------------------
    // GRAPHCOMMENT - Visual comments
    // -------------------------------------------------------------------------
    // HOW TO GET: https://graphcomment.com/
    // 1. Sign up
    // 2. Add website
    // 3. Get website ID
    graphComment: {
        websiteId: '',
        enabled: false  // Fallback
    },

    // -------------------------------------------------------------------------
    // FACEBOOK COMMENTS - FB integration
    // -------------------------------------------------------------------------
    // HOW TO GET: https://developers.facebook.com/
    // 1. Create Facebook App
    // 2. Get App ID
    facebookComments: {
        appId: '',
        enabled: false
    },

    // -------------------------------------------------------------------------
    // HYVOR TALK - Privacy focused
    // -------------------------------------------------------------------------
    // HOW TO GET: https://talk.hyvor.com/
    // 1. Sign up (paid with trial)
    // 2. Add website
    // 3. Get website ID
    hyvorTalk: {
        websiteId: '',
        enabled: false
    },

    // =========================================================================
    // EMAIL CAPTURE / LEAD GEN
    // =========================================================================

    // -------------------------------------------------------------------------
    // MAILCHIMP - Email marketing
    // -------------------------------------------------------------------------
    // HOW TO GET: https://mailchimp.com/
    // 1. Sign up (free tier)
    // 2. Create audience
    // 3. Create embedded form
    mailchimp: {
        formAction: '',  // Form action URL
        enabled: true
    },

    // -------------------------------------------------------------------------
    // SUMO - Email capture bar
    // -------------------------------------------------------------------------
    // HOW TO GET: https://sumo.com/
    // 1. Sign up (free tier)
    // 2. Install script
    // 3. Get site ID
    sumo: {
        siteId: '',
        enabled: false
    },

    // -------------------------------------------------------------------------
    // HELLOBAR - Top notification bar
    // -------------------------------------------------------------------------
    // HOW TO GET: https://www.hellobar.com/
    // 1. Sign up
    // 2. Create bar
    // 3. Get script
    helloBar: {
        scriptId: '',
        enabled: false
    },

    // -------------------------------------------------------------------------
    // CONVERTKIT - Creator email
    // -------------------------------------------------------------------------
    // HOW TO GET: https://convertkit.com/
    // 1. Sign up (free tier)
    // 2. Create form
    // 3. Get form ID
    convertKit: {
        formId: '',
        enabled: false
    }
};

// Share buttons priority
export const shareButtonsPriority = ['addThis', 'shareThis', 'addToAny'];

// Comments priority
export const commentsPriority = ['disqus', 'graphComment', 'facebookComments', 'hyvorTalk'];
