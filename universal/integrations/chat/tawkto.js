/**
 * Tawk.to Chat Provider
 * @module chat/tawkto
 */

export const name = 'tawkto';
export const configKey = 'tawk';

export function init(config, loadScript) {
    if (!config.src) return;

    loadScript(config.src, { crossorigin: '*' });
}
