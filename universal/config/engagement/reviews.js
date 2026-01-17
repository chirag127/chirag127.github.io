/**
 * Part 4: Engagement - Reviews / Social Proof
 * Display reviews and testimonials
 * @module config/engagement/reviews
 */

export const reviews = {
    trustpilot: { businessUnitId: '', enabled: true },
    googleReviews: { placeId: '', enabled: true },  // Via Elfsight
    yelpReviews: { businessId: '', enabled: false }
};

export const reviews_priority = ['trustpilot', 'googleReviews'];
