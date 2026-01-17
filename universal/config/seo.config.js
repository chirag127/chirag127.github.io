/**
 * SEO Tracking Configuration
 * Search engine optimization tools
 *
 * @module config/seo
 */

export const seoConfig = {

    // =========================================================================
    // GOOGLE SEARCH CONSOLE - Essential
    // =========================================================================
    // HOW TO GET: https://search.google.com/search-console
    // 1. Sign in with Google
    // 2. Add property (URL or domain)
    // 3. Verify ownership (HTML tag, DNS, file, etc.)
    // NOTE: No script needed - verification meta tag only
    googleSearchConsole: {
        verificationTag: '',  // <meta name="google-site-verification" content="XXX">
        enabled: true
    },

    // =========================================================================
    // BING WEBMASTER TOOLS - Essential
    // =========================================================================
    // HOW TO GET: https://www.bing.com/webmasters
    // 1. Sign in with Microsoft
    // 2. Add site
    // 3. Verify ownership
    bingWebmaster: {
        verificationTag: '',  // <meta name="msvalidate.01" content="XXX">
        enabled: true
    },

    // =========================================================================
    // YANDEX WEBMASTER - For Russian traffic
    // =========================================================================
    // HOW TO GET: https://webmaster.yandex.com/
    // 1. Sign in with Yandex
    // 2. Add site
    // 3. Verify
    yandexWebmaster: {
        verificationTag: '',  // <meta name="yandex-verification" content="XXX">
        enabled: false
    },

    // =========================================================================
    // BAIDU WEBMASTER - For Chinese traffic
    // =========================================================================
    // HOW TO GET: https://ziyuan.baidu.com/
    // 1. Create Baidu account
    // 2. Add site
    // 3. Verify
    baiduWebmaster: {
        verificationTag: '',
        enabled: false
    },

    // =========================================================================
    // PINTEREST - For image-heavy sites
    // =========================================================================
    // HOW TO GET: https://www.pinterest.com/
    // 1. Business account
    // 2. Claim website
    // 3. Get verification tag
    pinterest: {
        verificationTag: '',
        enabled: false
    }
};

// Additional SEO meta tags to include
export const seoMetaTags = {
    // Open Graph (Facebook/LinkedIn)
    openGraph: {
        enabled: true,
        defaultImage: '/og-image.png'
    },
    // Twitter Cards
    twitterCard: {
        enabled: true,
        site: '@chirag127',
        card: 'summary_large_image'
    },
    // Schema.org structured data
    schemaOrg: {
        enabled: true,
        type: 'WebSite'
    }
};
