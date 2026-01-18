/**
 * Part 4: Engagement - Comments
 * ENABLED for community building
 * @module config/engagement/comments
 */

export const comments = {
    // Giscus - GitHub Discussions (RECOMMENDED)
    // Feature: No ads, no tracking, uses GitHub API, fully free
    // Free Limit: 100% FREE (Open Source)
    giscus: { repo: '', repoId: '', category: '', categoryId: '', enabled: true },

    // Utterances - GitHub Issues
    // Feature: Lightweight, stores comments as Issues
    // Free Limit: 100% FREE (Open Source)
    utterances: { repo: '', enabled: false },

    // Facebook Comments
    // Feature: Social proof via real profiles
    // Free Limit: 100% FREE
    facebook: { appId: '', enabled: false },

    // Disqus - The standard
    // Feature: Huge network, spam filtering included
    // Free Limit: Free with MANDATORY ADS (Paid to remove)
    disqus: { shortname: 'chirag127', enabled: false }
};

export const comments_priority = ['giscus', 'utterances', 'facebook', 'disqus'];
