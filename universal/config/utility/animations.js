/**
 * Part 3: Utility - Animation Libraries
 * @module config/utility/animations
 */

export const animations = {
    // LottieFiles
    // Feature: Lightweight JSON animations
    // Limit: Free tier sufficient for most
    lottie: { enabled: true },  // LottieFiles - JSON animations

    // Anime.js
    // Feature: Simple JavaScript animation library
    // Limit: Open Source (Free)
    animejs: { enabled: true }  // Anime.js - DOM animations
};

export const animations_priority = ['lottie', 'animejs'];
