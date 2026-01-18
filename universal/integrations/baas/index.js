/**
 * BaaS Integrations Master Index
 * @module integrations/baas
 */
import { cms } from './cms/index.js';
import { database } from './database/index.js';
import { email } from './email/index.js';
import { file_upload } from './file_upload/index.js';
import { forms } from './forms/index.js';

export const baas = {
    cms,
    database,
    email,
    file_upload,
    forms
};
