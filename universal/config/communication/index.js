/**
 * Part 4: Communication - Index
 * @module config/communication
 */
import { live_chat } from './live_chat.js';
import { feedback_surveys } from './feedback_surveys.js';

export const communication = { ...live_chat, ...feedback_surveys };

export const communication_priorities = {
    live_chat: ['tawk', 'crisp', 'tidio'],
    feedback_surveys: ['typeform', 'googleForms']
};

export { live_chat, feedback_surveys };
