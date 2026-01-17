/**
 * Part 4: Engagement - Comments
 * ENABLED for community building
 * @module config/engagement/comments
 */

export const comments = {
    // GISCUS - GitHub-based, best for dev audience
    giscus: {
        repo: 'chirag127/chirag127.github.io',
        repoId: '',
        category: 'Announcements',
        categoryId: '',
        enabled: true
    },
    disqus: { shortname: '', enabled: false },  // Has ads
    hyvorTalk: { websiteId: '', enabled: false },
    commentbox: { projectId: '', enabled: false }
};

export const comments_priority = ['giscus'];
