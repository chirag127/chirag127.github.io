/**
 * Carbon Ads Provider
 * @module ads/carbon
 */

export const name = 'carbon';
export const configKey = 'carbon';

export function init(config, loadScript) {
    if (!config.serve || !config.placement) return;

    const scriptUrl = `//cdn.carbonads.com/carbon.js?serve=${config.serve}&placement=${config.placement}`;

    loadScript(scriptUrl, {
        id: '_carbonads_js'
    });
}
