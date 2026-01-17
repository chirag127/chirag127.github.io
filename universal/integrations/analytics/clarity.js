/**
 * Microsoft Clarity Provider
 * @module analytics/clarity
 */

export const name = 'clarity';
export const configKey = 'clarity';

export function init(config, loadScript) {
    if (!config.id) return;

    (function(c, l, a, r, i, t, y) {
        c[a] = c[a] || function() { (c[a].q = c[a].q || []).push(arguments); };
        t = l.createElement(r);
        t.async = 1;
        t.src = "https://www.clarity.ms/tag/" + i;
        y = l.getElementsByTagName(r)[0];
        y.parentNode.insertBefore(t, y);
    })(window, document, "clarity", "script", config.id);
}
