/**
 * Yandex Metrica Provider
 * @module analytics/yandex
 */

export const name = 'yandex';
export const configKey = 'yandex';

export function init(config, loadScript) {
    if (!config.id) return;

    (function(m, e, t, r, i, k, a) {
        m[i] = m[i] || function() { (m[i].a = m[i].a || []).push(arguments); };
        m[i].l = 1 * new Date();
        for (var j = 0; j < document.scripts.length; j++) {
            if (document.scripts[j].src === r) return;
        }
        k = e.createElement(t);
        a = e.getElementsByTagName(t)[0];
        k.async = 1;
        k.src = r;
        a.parentNode.insertBefore(k, a);
    })(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

    ym(config.id, "init", {
        clickmap: config.clickmap !== false,
        trackLinks: config.trackLinks !== false,
        accurateTrackBounce: config.accurateTrackBounce !== false,
        webvisor: config.webvisor !== false
    });
}
