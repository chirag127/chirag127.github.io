/**
 * Part 3: BaaS - File Upload
 * Client-side file upload widgets
 * @module config/baas/file_upload
 */

export const file_upload = {
    // Cloudinary - Media Management
    // Feature: Image/Video optimization, transformation API
    // Free Limit: 25 credits/mo (~25GB storage or bandwidth)
    cloudinary: { cloudName: '', uploadPreset: '', enabled: false },

    // Uploadcare - File Uploader
    // Feature: Smart CDN, Image processing
    // Free Limit: 3000 uploads/mo, 3GB traffic, 300MB storage
    uploadcare: { publicKey: '', enabled: false },

    // Filestack - File Uploader
    // Feature: Connects to Google Drive, FB, Insta, etc.
    // Free Limit: 100 uploads/mo, 1GB bandwidth
    filestack: { apiKey: '', enabled: false }
};

export const file_upload_priority = ['cloudinary', 'uploadcare'];
