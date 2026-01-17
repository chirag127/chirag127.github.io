/**
 * Part 3: BaaS - File Upload
 * Client-side file upload widgets
 * @module config/baas/file_upload
 */

export const file_upload = {
    // Cloudinary - Popular, generous free tier
    cloudinary: { cloudName: '', uploadPreset: '', enabled: false },
    uploadcare: { publicKey: '', enabled: false },
    filestack: { apiKey: '', enabled: false }
};

export const file_upload_priority = ['cloudinary', 'uploadcare'];
