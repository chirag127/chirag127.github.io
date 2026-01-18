/**
 * Part 3: Engagement - Comments & Community
 * @module config/engagement/comments
 */

export const comments = {
    // ============================================================================
    // GISCUS - The Best Free Choice for Tech Sites
    // ============================================================================
    // Description:
    // A commenting system powered by GitHub Discussions.
    //
    // Key Features:
    // - **100% Free** (No ads, no tracking).
    // - Uses GitHub for authentication.
    // - Markdown support.
    //
    // Requirements:
    // - Users NEED a GitHub account to comment.
    // - Public GitHub repository required.
    //
    // Best For:
    // - Developer tools, documentation, and technical hubs.
    //
    giscus: { repoId: '', categoryId: '', enabled: true },

    // ============================================================================
    // DISQUS - The Industry Standard
    // ============================================================================
    // Description:
    // Most popular commenting widget on the web.
    //
    // ⚠️ FREE TIER NOTE (2025):
    // - **Includes Ads** (Disqus "Reveal" system).
    // - Tracks user data across the web.
    // - Ad-free plans start at ~$18/month (Plus).
    //
    // Best For:
    // - Sites wanting the lower friction of general social login.
    //
    disqus: { shortname: '', enabled: false },

    // ============================================================================
    // COMMENTO - Privacy First
    // ============================================================================
    // Description:
    // Lightweight, fast, and no-tracking comments.
    //
    // Free Limits:
    // - **Unlimited (Self-hosted)**.
    // - Cloud version is paid ($10+/mo).
    //
    commento: { siteId: '', enabled: false }
};

export const comments_priority = ['giscus', 'disqus'];
