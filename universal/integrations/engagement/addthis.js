/**
 * Social Share Buttons - AddThis Provider
 * @module engagement/addthis
 */

export const name = 'addthis';
export const configKey = 'addThis';

export function init(config, loadScript) {
    if (!config.profileId || !config.enabled) return;

    // AddThis configuration
    window.addthis_config = window.addthis_config || {};
    window.addthis_share = window.addthis_share || {};

    // Load AddThis
    loadScript(`//s7.addthis.com/js/300/addthis_widget.js#pubid=${config.profileId}`);
}
