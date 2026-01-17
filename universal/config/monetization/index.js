/**
 * Part 1: Monetization - Index
 * @module config/monetization
 */

import { ads_display, ads_display_priority } from './ads_display.js';
import { ads_crypto, ads_crypto_priority } from './ads_crypto.js';
import { ads_pop, ads_pop_priority, ads_pop_limits } from './ads_pop.js';
import { ads_push, ads_push_priority } from './ads_push.js';
import { ads_text, ads_text_priority } from './ads_text.js';
import { ads_native, ads_native_priority } from './ads_native.js';
import { ads_interstitial, ads_interstitial_priority } from './ads_interstitial.js';
import { ads_video, ads_video_priority } from './ads_video.js';
import { url_shortener, url_shortener_priority } from './url_shortener.js';
import { donation_fiat, donation_fiat_priority } from './donation_fiat.js';
import { donation_crypto, donation_crypto_priority } from './donation_crypto.js';
import { affiliates, affiliates_priority } from './affiliates.js';
import { offerwalls, offerwalls_priority } from './offerwalls.js';
import { smart_links, smart_links_priority } from './smart_links.js';
import { file_hosting, file_hosting_priority } from './file_hosting.js';
import { merch, merch_priority } from './merch.js';
import { sponsored_content, sponsored_content_priority } from './sponsored_content.js';
import { exit_intent, exit_intent_priority } from './exit_intent.js';
import { browser_mining, browser_mining_priority } from './browser_mining.js';
import { captcha_monetization, captcha_monetization_priority } from './captcha_monetization.js';

export const monetization = {
    ...ads_display, ...ads_crypto, ...ads_pop, ...ads_push, ...ads_text,
    ...ads_native, ...ads_interstitial, ...ads_video,
    ...url_shortener, ...donation_fiat, ...donation_crypto, ...affiliates,
    ...offerwalls, ...smart_links, ...file_hosting, ...merch, ...sponsored_content,
    ...exit_intent, ...browser_mining, ...captcha_monetization, ads_pop_limits
};

export const monetization_priorities = {
    ads_display: ads_display_priority, ads_crypto: ads_crypto_priority,
    ads_pop: ads_pop_priority, ads_push: ads_push_priority, ads_text: ads_text_priority,
    ads_native: ads_native_priority, ads_interstitial: ads_interstitial_priority,
    ads_video: ads_video_priority, url_shortener: url_shortener_priority,
    donation_fiat: donation_fiat_priority, donation_crypto: donation_crypto_priority,
    affiliates: affiliates_priority, offerwalls: offerwalls_priority,
    smart_links: smart_links_priority, file_hosting: file_hosting_priority,
    merch: merch_priority, sponsored_content: sponsored_content_priority,
    exit_intent: exit_intent_priority, browser_mining: browser_mining_priority,
    captcha_monetization: captcha_monetization_priority
};

export { ads_display, ads_crypto, ads_pop, ads_push, ads_text, ads_native, ads_interstitial, ads_video, url_shortener, donation_fiat, donation_crypto, affiliates, offerwalls, smart_links, file_hosting, merch, sponsored_content, exit_intent, browser_mining, captcha_monetization };
