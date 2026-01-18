const fs = require('fs');
const path = require('path');

const PROJECT_ROOT = path.join(__dirname, '..');
const DIST_DIR = path.join(PROJECT_ROOT, 'dist');

// Define which presentations to include in the build
// We are using the validated source from inputs/QAD-Fight-or-Flight
const presentations = [
    { source: 'inputs/QAD-Fight-or-Flight', target: '18-01-26_Fight-or-Flight' }
];

// Ensure dist exists and is clean
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

        // CHECK: Ensure brain_alarm exists in the destination
        if (fs.existsSync(path.join(destPath, 'images/brain_alarm.png'))) {
            console.log("Verified: brain_alarm.png present in dist.");
        } else {
            console.error("FAILURE: brain_alarm.png missing from dist!");
            process.exit(1);
        }
    } else {
        console.error(`Error: Source directory not found: ${srcPath}`);
        process.exit(1);
    }
});

// Also copy shared skills assets
const skillsJs = path.join(PROJECT_ROOT, 'skills/creating-html-presentation/js');
if (fs.existsSync(skillsJs)) {
    const destJs = path.join(DIST_DIR, 'skills/creating-html-presentation/js');
    fs.mkdirSync(destJs, { recursive: true });
    fs.cpSync(skillsJs, destJs, { recursive: true });
}

console.log('Build complete.');
