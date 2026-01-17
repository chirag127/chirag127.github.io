/**
 * Buy Me a Coffee Donation Widget
 * @module ads/buymeacoffee
 */

export const name = 'buymeacoffee';
export const configKey = 'buyMeACoffee';

export function init(config, loadScript) {
    if (!config.username || !config.enabled) return;

    // Create BMC widget script
    const script = document.createElement('script');
    script.setAttribute('data-name', 'BMC-Widget');
    script.setAttribute('data-cfasync', 'false');
    script.src = 'https://cdnjs.buymeacoffee.com/1.0.0/widget.prod.min.js';
    script.setAttribute('data-id', config.username);
    script.setAttribute('data-description', config.message || 'Support this project!');
    script.setAttribute('data-message', 'Thank you for visiting!');
    script.setAttribute('data-color', config.color || '#5F7FFF');
    script.setAttribute('data-position', 'Right');
    script.setAttribute('data-x_margin', '18');
    script.setAttribute('data-y_margin', '18');
    script.async = true;

    document.head.appendChild(script);
}
