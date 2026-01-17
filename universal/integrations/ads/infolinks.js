/**
 * Infolinks In-Text Advertising Provider
 * @module ads/infolinks
 */

export const name = 'infolinks';
export const configKey = 'infolinks';

export function init(config, loadScript) {
    if (!config.publisherId || !config.websiteId || !config.enabled) return;

    // Infolinks configuration
    window.infolinks_pid = config.publisherId;
    window.infolinks_wsid = config.websiteId;

    // Load Infolinks
    loadScript('//resources.infolinks.com/js/infolinks_main.js');
}
