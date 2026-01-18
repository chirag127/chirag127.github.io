/**
 * Part 4: Engagement - Appointment Scheduling
 * @module config/engagement/scheduling
 */

export const scheduling = {
    // Cal.com
    // Feature: Open source, developer friendly
    // Free Limit: Unlimited event types for individuals (Generous)
    calcom: { username: '', enabled: true },

    // Calendly
    // Feature: The scheduling standard, very reliable
    // Free Limit: 1 Event Type, unlimited meetings
    calendly: { username: '', enabled: false }
};

export const scheduling_priority = ['calcom', 'calendly'];
