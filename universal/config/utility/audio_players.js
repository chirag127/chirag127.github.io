/**
 * Part 3: Utility - Audio Players
 * Embed audio content
 * @module config/utility/audio_players
 */

export const audio_players = {
    // ============================================================================
    // HOWLER.JS - The Audio Standard
    // ============================================================================
    // Description:
    // Modern Web Audio library. Defaults to Web Audio API and falls back to HTML5 Audio.
    //
    // License:
    // - MIT (100% Free).
    //
    howler: { enabled: true },

    // ============================================================================
    // SOUNDCLOUD - Embeds
    // ============================================================================
    // Description:
    // Audio hosting & embedding.
    //
    soundcloud: { enabled: true },

    // ============================================================================
    // SPOTIFY - Streaming Embeds
    // ============================================================================
    // Description:
    // Music streaming embeds.
    // Limits: 30s preview for non-logged users.
    //
    spotify: { enabled: true }
};

export const audio_players_priority = ['howler', 'spotify', 'soundcloud'];
