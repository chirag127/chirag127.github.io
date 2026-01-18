
import fs from 'fs';
import path from 'path';

const BASE_DIR = 'universal/integrations/baas';

async function verify() {
    console.log('Verifying BaaS files...');
    const categories = ['cms', 'database', 'email', 'file_upload', 'forms'];

    for (const cat of categories) {
        const dir = path.join(BASE_DIR, cat);
        const files = fs.readdirSync(dir);

        for (const file of files) {
            if (!file.endsWith('.js')) continue;

            try {
                // Dynamic import to check syntax
                const modulePath = path.resolve(dir, file);
                const fileUrl = 'file:///' + modulePath.replace(/\\/g, '/');
                await import(fileUrl);
                console.log(`✅ Verified: ${cat}/${file}`);
            } catch (err) {
                console.error(`❌ Error in ${cat}/${file}:`, err.message);
                process.exit(1);
            }
        }
    }
    console.log('All files verified successfully.');
}

verify();
