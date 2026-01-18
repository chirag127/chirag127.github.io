/**
 * Base URL Configuration for Multi-Platform Deployment
 *
 * Automatically detects the hosting platform and sets the correct base path.
 * This ensures the site works correctly on GitHub Pages, Netlify, Vercel,
 * Cloudflare Pages, and any other static hosting platform.
 */

(function() {
    'use strict';

    const hostname = window.location.hostname;
    const pathname = window.location.pathname;

    // Platform detection rules
    const PLATFORM_RULES = {
        // GitHub Pages - user site (serves from root)
        'chirag127.github.io': '',

        // GitHub Pages - project site (serves from /repo-name/)
        // Add project sites here if needed:
        // 'chirag127.github.io/project-name': '/project-name',

        // Netlify (custom domain or subdomain)
        '.netlify.app': '',

        // Vercel
        '.vercel.app': '',

        // Cloudflare Pages
        '.pages.dev': '',

        // Surge.sh
        '.surge.sh': '',

        // Render
        '.onrender.com': '',

        // Firebase Hosting
        '.web.app': '',
        '.firebaseapp.com': '',

        // Neocities
        '.neocities.org': '',

        // Deno Deploy
        '.deno.dev': '',

        // GitLab Pages
        '.gitlab.io': '',

        // Codeberg Pages
        '.codeberg.page': '',

        // Railway
        '.railway.app': '',

        // Fly.io
        '.fly.dev': '',

        // Local development
        'localhost': '',
        '127.0.0.1': '',
    };

    /**
     * Detect the base URL based on current hostname
     */
    function detectBaseUrl() {
        // Check exact hostname match first
        if (PLATFORM_RULES.hasOwnProperty(hostname)) {
            return PLATFORM_RULES[hostname];
        }

        // Check suffix matches (for subdomains)
        for (const [suffix, basePath] of Object.entries(PLATFORM_RULES)) {
            if (suffix.startsWith('.') && hostname.endsWith(suffix)) {
                return basePath;
            }
        }

        // Custom domain - assume root
        return '';
    }

    /**
     * Get absolute URL from a root-relative path
     */
    function getAssetUrl(path) {
        const base = detectBaseUrl();
        // Ensure path starts with /
        const normalizedPath = path.startsWith('/') ? path : '/' + path;
        return base + normalizedPath;
    }

    /**
     * Get the current platform name (for debugging)
     */
    function getPlatformName() {
        if (hostname === 'localhost' || hostname === '127.0.0.1') return 'Local Development';
        if (hostname === 'chirag127.github.io') return 'GitHub Pages';
        if (hostname.endsWith('.netlify.app')) return 'Netlify';
        if (hostname.endsWith('.vercel.app')) return 'Vercel';
        if (hostname.endsWith('.pages.dev')) return 'Cloudflare Pages';
        if (hostname.endsWith('.surge.sh')) return 'Surge.sh';
        if (hostname.endsWith('.onrender.com')) return 'Render';
        if (hostname.endsWith('.web.app') || hostname.endsWith('.firebaseapp.com')) return 'Firebase';
        if (hostname.endsWith('.neocities.org')) return 'Neocities';
        if (hostname.endsWith('.deno.dev')) return 'Deno Deploy';
        if (hostname.endsWith('.gitlab.io')) return 'GitLab Pages';
        if (hostname.endsWith('.codeberg.page')) return 'Codeberg Pages';
        return 'Custom Domain';
    }

    // Export to global scope
    window.SiteConfig = window.SiteConfig || {};
    window.SiteConfig.BASE_URL = detectBaseUrl();
    window.SiteConfig.getAssetUrl = getAssetUrl;
    window.SiteConfig.getPlatformName = getPlatformName;
    window.SiteConfig.hostname = hostname;

    // Log platform detection in development
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        console.log(`[SiteConfig] Platform: ${getPlatformName()}, BASE_URL: "${detectBaseUrl()}"`);
    }
})();
