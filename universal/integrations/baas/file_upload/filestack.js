/**
 * BaaS Provider: filestack
 * Category: file_upload
 */

export const name = 'filestack';
export const configKey = 'filestack';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing file_upload/filestack');

    loadScript('https://static.filestackapi.com/filestack-js/3.x.x/filestack.min.js', 'filestack-js')
        .then(() => {
            if (window.filestack) {
                window.filestackClient = window.filestack.init(config.apiKey);
                console.log('[BaaS] Filestack client ready as window.filestackClient');
            }
        });
}
