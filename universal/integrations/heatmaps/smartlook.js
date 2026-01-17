/**
 * Smartlook Session Recording Provider
 * @module heatmaps/smartlook
 */

export const name = 'smartlook';
export const configKey = 'smartlook';

export function init(config, loadScript) {
    if (!config.projectKey || !config.enabled) return;

    window.smartlook||(function(d) {
        var o=smartlook=function(){ o.api.push(arguments)},h=d.getElementsByTagName('head')[0];
        var c=d.createElement('script');o.api=new Array();c.async=true;c.type='text/javascript';
        c.charset='utf-8';c.src='https://web-sdk.smartlook.com/recorder.js';h.appendChild(c);
    })(document);
    smartlook('init', config.projectKey, { region: 'eu' });
}
