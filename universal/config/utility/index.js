/**
 * Part 3: Utility - Index
 * @module config/utility
 */

import { cookie_consent, cookie_consent_priority } from './cookie_consent.js';
import { captcha, captcha_priority } from './captcha.js';
import { fonts, fonts_priority } from './fonts.js';
import { icons, icons_priority } from './icons.js';
import { video_players, video_players_priority } from './video_players.js';
import { maps, maps_priority } from './maps.js';
import { search, search_priority } from './search.js';
import { translation, translation_priority } from './translation.js';
import { reviews as utility_reviews } from './reviews.js';
import { audio_players, audio_players_priority } from './audio_players.js';
import { animations, animations_priority } from './animations.js';
import { geolocation, geolocation_priority } from './geolocation.js';

export const utility = {
    ...cookie_consent, ...captcha, ...fonts, ...icons, ...video_players,
    ...maps, ...search, ...translation, ...utility_reviews,
    ...audio_players, ...animations, ...geolocation
};

export const utility_priorities = {
    cookie_consent: cookie_consent_priority, captcha: captcha_priority,
    fonts: fonts_priority, icons: icons_priority, video_players: video_players_priority,
    maps: maps_priority, search: search_priority, translation: translation_priority,
    audio_players: audio_players_priority, animations: animations_priority,
    geolocation: geolocation_priority
};

export { cookie_consent, captcha, fonts, icons, video_players, maps, search, translation, audio_players, animations, geolocation };
