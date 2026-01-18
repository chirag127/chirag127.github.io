/**
 * Part 3: Utility - Animation Libraries
 * @module config/utility/animations
 */

export const animations = {
    // ============================================================================
    // ANIME.JS - The Lightweight King
    // ============================================================================
    // Description:
    // A lightweight JavaScript animation library with a simple, powerful API.
    // Works with CSS properties, SVG, DOM attributes and JavaScript Objects.
    //
    // License:
    // - MIT (100% Free Forever).
    // - No usage limits.
    //
    // Best For:
    // - UI animations, micro-interactions, complex sequences.
    //
    animejs: { enabled: true },

    // ============================================================================
    // LOTTIEFILES - Vector Animations
    // ============================================================================
    // Description:
    // Render After Effects animations natively on the web.
    //
    // Free Tier Limits (2024):
    // - Unlimited Public file uploads.
    // - 5 Private file uploads (Lifetime limit).
    // - 10 Downloads/month for public animations.
    // - Lottie Creator: 5 Exports.
    //
    // Best For:
    // - High-quality vector illustrations/animations.
    //
    lottie: { enabled: false }
};

export const animations_priority = ['animejs', 'lottie'];
