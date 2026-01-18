/**
 * Part 4: Engagement - Loyalty / Rewards
 * Contests and giveaways
 * @module config/engagement/rewards
 */

export const rewards = {
    // Gleam
    // Feature: The king of viral giveaways
    // Free Limit: Unlimited campaigns, 10 winners/campaign
    gleam: { campaignId: '', enabled: true },

    // RafflePress
    // Feature: WordPress focused (if using WP backend)
    // Free Limit: Lite version available (Basic features)
    rafflepress: { widgetId: '', enabled: false }
};

export const rewards_priority = ['gleam', 'rafflepress'];
