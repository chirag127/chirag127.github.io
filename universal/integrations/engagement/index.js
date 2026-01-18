/**
 * Engagement Integrations Master Index
 * @module integrations/engagement
 */
import { ab_testing } from './ab_testing/index.js';
import { social_share } from './social_share/index.js';
import { comments } from './comments/index.js';
import { email_capture } from './email_capture/index.js';
import { push_marketing } from './push_marketing/index.js';
import { faq } from './faq/index.js';
import { notification_bells } from './notification_bells/index.js';
import { popups } from './popups/index.js';
import { rewards } from './rewards/index.js';
import { scheduling } from './scheduling/index.js';
import { social_feeds } from './social_feeds/index.js';

export const engagement = {
    ab_testing,
    social_share,
    comments,
    email_capture,
    push_marketing,
    faq,
    notification_bells,
    popups,
    rewards,
    scheduling,
    social_feeds
};
