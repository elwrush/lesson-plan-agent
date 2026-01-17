const fs = require('fs');
const path = require('path');

const DIST_DIR = path.join(__dirname, '..', 'dist');
const PROJECT_ROOT = path.join(__dirname, '..');

// Files and folders to copy (Whitelist)
const INCLUDES = [
    'index.html',
    'live.html',
    'link.html',
    'js',
    'images',
    'audio',
    'videos'
];

// Ensure dist exists
if (fs.existsSync(DIST_DIR)) {
    fs.rmSync(DIST_DIR, { recursive: true, force: true });
}
fs.mkdirSync(DIST_DIR);

console.log(`Building to ${DIST_DIR}...`);

INCLUDES.forEach(item => {
    const src = path.join(PROJECT_ROOT, item);
    const dest = path.join(DIST_DIR, item);

    if (fs.existsSync(src)) {
        const stats = fs.statSync(src);
        if (stats.isDirectory()) {
            fs.cpSync(src, dest, { recursive: true });
            console.log(`Copied dir: ${item}`);
        } else {
            fs.copyFileSync(src, dest);
            console.log(`Copied file: ${item}`);
        }
    } else {
        console.warn(`Warning: Source item not found: ${item}`);
    }
});

console.log('Build complete.');
