/**
 * Part 2: Tracking - Attribution & Deep Linking
 * GROWTH FOCUS: Understanding where your users came from
 * @module config/tracking/attribution
 */

export const attribution = {
    // ============================================================================
    // BRANCH.IO - Deep Linking Leader
    // ============================================================================
    // Description:
    // Turns web visitors into app users with seamless links.
    //
    // Key Features:
    // - Cross-platform attribution.
    // - Persona-based deep linking.
    //
    // Free Limits (2025 - "Launch" Plan):
    // - **10,000 Monthly Active Users (MAUs)**.
    // - Unlimited Deep Linking.
    //
    branch: { key: '', enabled: false },

    // ============================================================================
    // JITSU (Formerly EventNative) - Open Source CDP
    // ============================================================================
    // Description:
    // Collect events and sync them to your data warehouse.
    //
    // Free Limits:
    // - **10,000 Events / month** (Cloud).
    // - **Unlimited (Self-hosted)**.
    //
    jitsu: { writeKey: '', enabled: false },

    // ============================================================================
    // SEGMENT (Twilio) - The Original CDP
    // ============================================================================
    // Description:
    // Standard API for collecting data and sending it to 100+ destinations.
    //
    // Free Limits (2025):
    // - **1,000 Monthly Tracked Users (MTUs)**.
    // - 2 Destinations.
    //
    segment: { writeKey: '', enabled: false }
};

export const attribution_priority = ['segment', 'branch', 'jitsu'];
