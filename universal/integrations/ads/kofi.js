/**
 * Ko-fi Donation Widget Provider
 * @module ads/kofi
 */

export const name = 'kofi';
export const configKey = 'kofi';

export function init(config, loadScript) {
    if (!config.username || !config.enabled) return;

    // Create Ko-fi button
    const btn = document.createElement('div');
    btn.innerHTML = `
        <script type='text/javascript' src='https://storage.ko-fi.com/cdn/widget/Widget_2.js'></script>
        <script type='text/javascript'>kofiwidget2.init('Support Me on Ko-fi', '${config.color || '#29abe0'}', '${config.username}');kofiwidget2.draw();</script>
    `;
    document.body.appendChild(btn);
}
