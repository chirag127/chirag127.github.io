/**
 * Tidio Chat Provider
 * @module chat/tidio
 */

export const name = 'tidio';
export const configKey = 'tidio';

export function init(config, loadScript) {
    if (!config.publicKey || !config.enabled) return;

    loadScript(`//code.tidio.co/${config.publicKey}.js`);
}
