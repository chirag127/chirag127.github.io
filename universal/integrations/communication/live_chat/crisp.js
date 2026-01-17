/**
 * Crisp Chat Provider
 * @module chat/crisp
 */

export const name = 'crisp';
export const configKey = 'crisp';

export function init(config, loadScript) {
    if (!config.websiteId) return;

    window.$crisp = [];
    window.CRISP_WEBSITE_ID = config.websiteId;

    (function() {
        const d = document;
        const s = d.createElement("script");
        s.src = "https://client.crisp.chat/l.js";
        s.async = 1;
        d.getElementsByTagName("head")[0].appendChild(s);
    })();
}
