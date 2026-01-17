/**
 * Part 3: Engagement - Index
 * @module config/engagement
 */
import { ab_testing } from './ab_testing.js';
import { social_share } from './social_share.js';
import { comments } from './comments.js';
import { email_capture } from './email_capture.js';
import { push_marketing } from './push_marketing.js';

export const engagement = { ...ab_testing, ...social_share, ...comments, ...email_capture, ...push_marketing };

export const engagement_priorities = {
    ab_testing: ['vwo', 'crazyegg'], social_share: ['addThis', 'shareThis'],
    comments: ['disqus'], email_capture: ['mailchimp', 'sumo'], push_marketing: ['oneSignal']
};

export { ab_testing, social_share, comments, email_capture, push_marketing };
