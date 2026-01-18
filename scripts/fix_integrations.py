import os
import re

ROOT_DIR = r"c:\AM\GitHub\chirag127.github.io\universal\integrations"

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find: import { something } from './something.js';
    # And replace with: import * as something from './something.js';

    # We only want to match imports where the imported name matches the filename (without ext)
    # pattern: import { (\w+) } from '\./\1\.js';

    new_content = re.sub(
        r"import\s+\{\s+(\w+)\s+\}\s+from\s+'\./\1\.js';",
        r"import * as \1 from './\1.js';",
        content
    )

    if content != new_content:
        print(f"Fixing {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

count = 0
for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file == "index.js":
            if fix_file(os.path.join(root, file)):
                count += 1

print(f"Fixed {count} files.")
