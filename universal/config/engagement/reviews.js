/**
 * Part 4: Engagement - Reviews / Social Proof
 * Display reviews and testimonials
 * @module config/engagement/reviews
 */

export const reviews = {
    // Trustpilot
    // Feature: High trust signal, automated invites
    // Free Limit: 100 invites/month, Review Box widget
    trustpilot: { businessUnitId: '', enabled: true },

    // Google Reviews (via Elfsight/Widget)
    // Feature: Displays your G-Business reviews
    // Free Limit: Managed by Elfsight (200 views) or Free API
    googleReviews: { placeId: '', enabled: true },  // Via Elfsight

    // Yelp Reviews
    // Feature: Restaurant/Local service focus
    // Free Limit: Embeds are free
    yelpReviews: { businessId: '', enabled: false }
};

export const reviews_priority = ['trustpilot', 'googleReviews', 'yelpReviews'];
