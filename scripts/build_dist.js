const fs = require('fs');
const path = require('path');

const PROJECT_ROOT = path.join(__dirname, '..');
const DIST_DIR = path.join(PROJECT_ROOT, 'dist');

// We will use a unique folder name to bypass any persistent server-side caching
const presentations = [
    { source: 'inputs/QAD-Fight-or-Flight', target: 'red-alert-slides' }
];

if (fs.existsSync(DIST_DIR)) {
    fs.rmSync(DIST_DIR, { recursive: true, force: true });
}
fs.mkdirSync(DIST_DIR);

presentations.forEach(pres => {
    const srcPath = path.join(PROJECT_ROOT, pres.source);
    const destPath = path.join(DIST_DIR, pres.target);

    if (fs.existsSync(srcPath)) {
        console.log(`Building ${pres.source} to dist/${pres.target}...`);
        fs.mkdirSync(destPath, { recursive: true });
        fs.cpSync(srcPath, destPath, { recursive: true });
    }
});

// Shared assets
const skillsJs = path.join(PROJECT_ROOT, 'skills/creating-html-presentation/js');
if (fs.existsSync(skillsJs)) {
    const destJs = path.join(DIST_DIR, 'skills/creating-html-presentation/js');
    fs.mkdirSync(destJs, { recursive: true });
    fs.cpSync(skillsJs, destJs, { recursive: true });
}

console.log('Build complete.');
