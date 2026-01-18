/**
 * BaaS - File Upload Integrations
 * @module integrations/baas/file_upload
 */

import * as cloudinary from './cloudinary.js';
import * as uploadcare from './uploadcare.js';
import * as filestack from './filestack.js';

export const file_upload = {
    cloudinary, uploadcare, filestack
};
