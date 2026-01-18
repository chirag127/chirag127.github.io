/**
 * Part 4: Engagement - Comments
 * ENABLED for community building
 * @module config/engagement/comments
 */

export const comments = {
    // Disqus - The standard
    // Feature: Huge network, spam filtering included
    // Free Limit: Free with Ads
    disqus: { shortname: 'chirag127', enabled: false },

    // Giscus - GitHub Discussions
    // Feature: Zero ads, no tracking, uses GitHub API
    // Free Limit: 100% Free (Open Source)
    giscus: { repo: '', repoId: '', category: '', categoryId: '', enabled: false },

    // Utterances - GitHub Issues
    // Feature: Lightweight, stores comments as Issues
    // Free Limit: 100% Free (Open Source)
    utterances: { repo: '', enabled: false },

    // Hyvor Talk
    // Feature: Privacy-focused, no ads
    // Free Limit: Paid only (Trial available)
    hyvorTalk: { websiteId: '', enabled: false },

    // Facebook Comments
    // Feature: Social proof via real profiles
    // Free Limit: 100% Free
    facebook: { appId: '', enabled: false }
};

export const comments_priority = ['giscus'];
