/**
 * BaaS Provider: uploadcare
 * Category: file_upload
 */

export const name = 'uploadcare';
export const configKey = 'uploadcare';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing file_upload/uploadcare');

    // Setting global config before loading script
    window.UPLOADCARE_PUBLIC_KEY = config.publicKey;

    loadScript('https://ucarecdn.com/libs/widget/3.x/uploadcare.full.min.js', 'uploadcare-widget')
        .then(() => {
            console.log('[BaaS] Uploadcare Widget loaded');
        });
}
