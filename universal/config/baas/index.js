/**
 * Part 3: BaaS - Index
 * @module config/baas
 */

import { forms, forms_priority } from './forms.js';
import { database, database_priority } from './database.js';
import { file_upload, file_upload_priority } from './file_upload.js';
import { email, email_priority } from './email.js';
import { cms, cms_priority } from './cms.js';

export const baas = {
    ...forms, ...database, ...file_upload, ...email, ...cms
};

export const baas_priorities = {
    forms: forms_priority, database: database_priority,
    file_upload: file_upload_priority, email: email_priority, cms: cms_priority
};

export { forms, database, file_upload, email, cms };
