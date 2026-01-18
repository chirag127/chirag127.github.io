/**
 * Part 4: Engagement - Reviews / Social Proof
 * Display reviews and testimonials
 * @module config/engagement/reviews
 */

export const reviews = {
    // Trustpilot
    // Feature: The most trusted review platform
    // Free Limit: 50 review invitations/month
    trustpilot: { businessId: '', enabled: true },

    // Google Reviews (via Widget)
    // Feature: Embed Google Maps reviews
    // Free Limit: Depends on widget provider (e.g., Elfsight 200 views)
    google_reviews: { placeId: '', enabled: false },

    // Yelp Reviews (via Widget)
    // Feature: Embed Yelp reviews
    // Free Limit: Depends on widget provider
    yelp_reviews: { businessId: '', enabled: false }
};

export const reviews_priority = ['trustpilot', 'google_reviews'];
