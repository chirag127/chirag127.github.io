/**
 * Disqus Comments Provider
 * @module engagement/disqus
 */

export const name = 'disqus';
export const configKey = 'disqus';

export function init(config, loadScript) {
    if (!config.shortname || !config.enabled) return;

    // Only load on pages with comment container
    const container = document.getElementById('disqus_thread');
    if (!container) return;

    // Disqus configuration
    window.disqus_config = function() {
        this.page.url = window.location.href;
        this.page.identifier = window.location.pathname;
    };

    // Load Disqus
    const s = document.createElement('script');
    s.src = `//${config.shortname}.disqus.com/embed.js`;
    s.setAttribute('data-timestamp', +new Date());
    (document.head || document.body).appendChild(s);
}
