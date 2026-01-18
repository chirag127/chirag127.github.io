/**
 * BaaS Provider: cloudinary
 * Category: file_upload
 */

export const name = 'cloudinary';
export const configKey = 'cloudinary';

export function init(config, loadScript) {
    if (!config.enabled) return;
    console.log('[BaaS] Initializing file_upload/cloudinary');

    loadScript('https://upload-widget.cloudinary.com/global/all.js', 'cloudinary-widget')
        .then(() => {
            console.log('[BaaS] Cloudinary Upload Widget loaded. Use window.cloudinary.createUploadWidget()');
        });
}
