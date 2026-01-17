/**
 * Part 4: Engagement - Index
 * @module config/engagement
 */

import { ab_testing, ab_testing_priority } from './ab_testing.js';
import { social_share, social_share_priority } from './social_share.js';
import { comments, comments_priority } from './comments.js';
import { email_capture, email_capture_priority } from './email_capture.js';
import { push_marketing, push_marketing_priority } from './push_marketing.js';
import { social_feeds, social_feeds_priority } from './social_feeds.js';
import { reviews, reviews_priority } from './reviews.js';
import { popups, popups_priority } from './popups.js';
import { rewards, rewards_priority } from './rewards.js';
import { scheduling, scheduling_priority } from './scheduling.js';
import { faq, faq_priority } from './faq.js';
import { notification_bells, notification_bells_priority } from './notification_bells.js';

export const engagement = {
    ...ab_testing, ...social_share, ...comments, ...email_capture, ...push_marketing,
    ...social_feeds, ...reviews, ...popups, ...rewards, ...scheduling, ...faq, ...notification_bells
};

export const engagement_priorities = {
    ab_testing: ab_testing_priority, social_share: social_share_priority,
    comments: comments_priority, email_capture: email_capture_priority,
    push_marketing: push_marketing_priority, social_feeds: social_feeds_priority,
    reviews: reviews_priority, popups: popups_priority, rewards: rewards_priority,
    scheduling: scheduling_priority, faq: faq_priority, notification_bells: notification_bells_priority
};

export { ab_testing, social_share, comments, email_capture, push_marketing, social_feeds, reviews, popups, rewards, scheduling, faq, notification_bells };
