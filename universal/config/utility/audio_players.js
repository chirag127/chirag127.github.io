/**
 * Part 3: Utility - Audio Players
 * Embed audio content
 * @module config/utility/audio_players
 */

export const audio_players = {
    // SoundCloud
    // Feature: Audio hosting & embedding
    // Limit: Free uploads restricted
    soundcloud: { enabled: true },  // Embed supported

    // Spotify
    // Feature: Music streaming embeds
    // Limit: 30s preview for non-logged users
    spotify: { enabled: true }
};

export const audio_players_priority = ['spotify', 'soundcloud'];
