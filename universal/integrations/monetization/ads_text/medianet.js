/**
 * Media.net Contextual Ads Provider
 * @module ads/medianet
 */

export const name = 'medianet';
export const configKey = 'mediaNet';

export function init(config, loadScript) {
    if (!config.siteId || !config.enabled) return;

    window._mNHandle = window._mNHandle || {};
    window._mNHandle.queue = window._mNHandle.queue || [];
    medianet_versionId = "3121199";

    loadScript(`//contextual.media.net/dmedianet.js?cid=${config.siteId}`);
}
