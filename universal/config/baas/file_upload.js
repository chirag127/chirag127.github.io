/**
 * Part 3: BaaS - File Upload
 * Client-side file upload widgets with CDN delivery and image optimization
 * @module config/baas/file_upload
 */

export const file_upload = {
    // ============================================================================
    // CLOUDINARY - Media Management Platform
    // ============================================================================
    // What it does:
    // - Image and video upload, storage, and delivery via CDN
    // - Automatic image optimization (format, quality, size)
    // - On-the-fly image transformations (resize, crop, filters)
    // - Video transcoding and adaptive streaming
    // - AI-powered auto-tagging and content moderation
    // - Responsive images with automatic format selection (WebP, AVIF)
    // - Face detection and smart cropping
    //
    // What it doesn't do:
    // - No document storage (PDFs, Word files) - images/videos only
    // - No file versioning or backup features
    // - No built-in authentication (use with your auth system)
    //
    // Free Tier Limits (Free Plan):
    // - 25 credits per month (1 credit = 1GB storage OR 1GB bandwidth)
    // - Approximately 25GB total usage (storage + bandwidth combined)
    // - Unlimited transformations
    // - 10,000 images
    // - 2 users
    // - Community support
    //
    // Best for: Image-heavy sites, e-commerce, portfolios, social media apps
    // Website: https://cloudinary.com
    // Note: Most generous for image optimization and transformations
    cloudinary: { cloudName: '', uploadPreset: '', enabled: false },

    // ============================================================================
    // UPLOADCARE - File Uploader with Smart CDN
    // ============================================================================
    // What it does:
    // - File upload widget with drag-and-drop interface
    // - Image processing and optimization
    // - Upload from URL, camera, social media, cloud storage
    // - Adaptive delivery based on device and network
    // - Image recognition and smart cropping
    // - Document preview generation
    // - Video encoding and thumbnails
    //
    // What it doesn't do:
    // - Limited video processing compared to Cloudinary
    // - No advanced AI features in free tier
    // - Storage limits are stricter
    //
    // Free Tier Limits (Free Plan):
    // - 3,000 uploads per month
    // - 3GB traffic (bandwidth)
    // - 300MB storage
    // - Basic image operations
    // - 1 project
    // - Community support
    //
    // Best for: Simple file uploads, document handling, multi-source uploads
    // Website: https://uploadcare.com
    // Note: Good for mixed content (images + documents)
    uploadcare: { publicKey: '', enabled: false },

    // ============================================================================
    // FILESTACK - Universal File Uploader
    // ============================================================================
    // What it does:
    // - Upload files from 20+ sources (Google Drive, Dropbox, Instagram, etc.)
    // - Image transformations and filters
    // - Document conversion (PDF, Office files)
    // - Video transcoding
    // - Virus scanning and content moderation
    // - Intelligent cropping and face detection
    //
    // What it doesn't do:
    // - Very limited free tier compared to competitors
    // - No permanent storage in free tier (files expire)
    // - Advanced features require paid plans
    //
    // Free Tier Limits (Free Plan):
    // - 100 uploads per month
    // - 1GB bandwidth
    // - 250MB storage
    // - Files stored for 30 days only
    // - Basic transformations
    //
    // Best for: Apps needing social media integration, temporary file storage
    // Website: https://www.filestack.com
    // Note: Limited free tier - consider Cloudinary or Uploadcare for better limits
    filestack: { apiKey: '', enabled: false }
};

export const file_upload_priority = ['cloudinary', 'uploadcare'];

// Made with Bob
