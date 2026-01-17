/**
 * Part 5: Utility - Index
 * @module config/utility
 */
import { cookie_consent } from './cookie_consent.js';
import { captcha } from './captcha.js';
import { fonts } from './fonts.js';
import { icons } from './icons.js';
import { video_players } from './video_players.js';
import { maps } from './maps.js';
import { search } from './search.js';
import { translation } from './translation.js';
import { reviews } from './reviews.js';

export const utility = {
    ...cookie_consent, ...captcha, ...fonts, ...icons,
    ...video_players, ...maps, ...search, ...translation, ...reviews
};

export const utility_priorities = {
    cookie_consent: ['cookiebot'], captcha: ['turnstile', 'hcaptcha', 'recaptcha'],
    fonts: ['googleFonts'], icons: ['fontAwesome'], maps: ['openStreetMap']
};

export { cookie_consent, captcha, fonts, icons, video_players, maps, search, translation, reviews };
