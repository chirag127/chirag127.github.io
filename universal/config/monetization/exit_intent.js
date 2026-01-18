/**
 * Part 1: Monetization - Exit Intent
 * Popup when mouse leaves window
 * @module config/monetization/exit_intent
 */

export const exit_intent = {
    // Ouibounce
    // Feature: Library to detect exit intent
    // Cost: Open Source (Free)
    ouibounce: { enabled: false },  // Library

    // Poptin Exit
    // Feature: Smart exit popup builder
    // Cost: Free tier available
    poptin_exit: { siteKey: '', enabled: false }
};

export const exit_intent_priority = ['ouibounce', 'poptin_exit'];
