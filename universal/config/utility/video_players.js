/**
 * Part 5: Utility - Video Players
 * @module config/utility/video_players
 */
export const video_players = {
    // ============================================================================
    // YOUTUBE
    // ============================================================================
    // Description:
    // Infinite hosting, massive reach.
    //
    youtube: { enabled: true },

    // ============================================================================
    // VIMEO
    // ============================================================================
    // Description:
    // Clean, professional player.
    // Limits: Basic ("Free") plan has strict weekly upload limits.
    //
    vimeo: { enabled: true },

    // ============================================================================
    // WISTIA
    // ============================================================================
    // Description:
    // Marketing video hosting.
    // Free Limits: 3 videos / channel.
    //
    wistia: { enabled: false }
};

export const video_players_priority = ['youtube', 'vimeo', 'wistia'];
