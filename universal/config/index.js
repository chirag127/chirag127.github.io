/**
 * UNIVERSAL CONFIG MASTER INDEX
 * Aggregates all 5 stacks from their respective folders
 * @module config
 */

import { monetization, monetization_priorities } from './monetization/index.js';
import { tracking, tracking_priorities } from './tracking/index.js';
import { engagement, engagement_priorities } from './engagement/index.js';
import { communication, communication_priorities } from './communication/index.js';
import { utility, utility_priorities } from './utility/index.js';

export const SITE_CONFIG = { ...monetization, ...tracking, ...engagement, ...communication, ...utility };

export const priorities = {
    ...monetization_priorities, ...tracking_priorities, ...engagement_priorities,
    ...communication_priorities, ...utility_priorities
};

export { monetization, tracking, engagement, communication, utility };

if (typeof window !== 'undefined') {
    window.SITE_CONFIG = SITE_CONFIG;
    window.CONFIG_PRIORITIES = priorities;
}

export function getFirstEnabled(priorityList, config = SITE_CONFIG) {
    for (const key of priorityList) {
        if (config[key]?.enabled) return { key, config: config[key] };
    }
    return null;
}
