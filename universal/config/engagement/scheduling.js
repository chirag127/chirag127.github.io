/**
 * Part 3: Engagement - Scheduling & Calendar
 * @module config/engagement/scheduling
 */

export const scheduling = {
    // ============================================================================
    // CALENDLY - The Standard for Booking
    // ============================================================================
    // Description:
    // Simple, intuitive booking platform for meetings.
    //
    // Free Limits (2025):
    // - **1 Meeting Type** (e.g. 15-min call).
    // - Unlimited bookings.
    // - Integration with Google/Outlook calendars.
    //
    calendly: { username: '', enabled: false },

    // ============================================================================
    // TYDYCAL - Lifetime Free Choice
    // ============================================================================
    tidycal: { username: '', enabled: false }
};

export const scheduling_priority = ['calendly', 'tidycal'];
