const fs = require('fs');
const path = require('path');
const fsPromises = fs.promises;

async function copyDir(src, dest, filter = () => true) {
    await fsPromises.mkdir(dest, { recursive: true });
    const entries = await fsPromises.readdir(src, { withFileTypes: true });

    for (let entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);

        if (!filter(srcPath)) continue;

        if (entry.isDirectory()) {
            await copyDir(srcPath, destPath, filter);
        } else {
            await fsPromises.copyFile(srcPath, destPath);
        }
    }
}

async function emptyDir(dir) {
    if (!fs.existsSync(dir)) return;
    const entries = await fsPromises.readdir(dir, { withFileTypes: true });
    for (let entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
            await fsPromises.rm(fullPath, { recursive: true, force: true });
        } else {
            await fsPromises.unlink(fullPath);
        }
    }
}

async function build() {
    const projectRoot = process.cwd();
    const distRoot = path.join(projectRoot, 'dist');
    const engineRoot = path.join(projectRoot, 'node_modules', 'reveal.js');
    const inputsDir = path.join(projectRoot, 'inputs');

    const targetFolder = process.argv[2]; // Target a specific folder if provided

    console.log(`🚀 Starting ${targetFolder ? 'targeted' : 'full'} build process...`);

    // 1. Clean dist directory
    try {
        if (!targetFolder) {
            if (fs.existsSync(distRoot)) {
                await emptyDir(distRoot);
                console.log('🧹 Cleaned dist directory (Full Build).');
            } else {
                await fsPromises.mkdir(distRoot, { recursive: true });
            }
        } else {
            const targetDist = path.join(distRoot, targetFolder);
            if (fs.existsSync(targetDist)) {
                await fsPromises.rm(targetDist, { recursive: true, force: true });
                console.log(`🧹 Cleaned target dist: ${targetFolder}`);
            }
            await fsPromises.mkdir(targetDist, { recursive: true });
        }
    } catch (err) {
        console.error('❌ Error cleaning dist:', err);
    }

    // 2. Copy Shared Reveal.js Engine
    console.log('📦 Copying shared Reveal.js engine...');
    const engineFolders = ['dist', 'plugin', 'css'];
    for (const folder of engineFolders) {
        const src = path.join(engineRoot, folder);
        const dest = path.join(distRoot, folder);
        if (fs.existsSync(src)) {
            await copyDir(src, dest, (srcPath) => !srcPath.includes('desktop.ini') && !srcPath.includes('.git'));
            console.log(`   ✅ Copied ${folder}/`);
        } else {
            console.warn(`   ⚠️  Warning: ${folder} not found in ${engineRoot}`);
        }
    }

    // 2.5 Copy Shared Assets (Root images/)
    console.log('🖼️  Copying shared global assets (root images/)...');
    const rootImages = path.join(projectRoot, 'images');
    const distImages = path.join(distRoot, 'images');
    if (fs.existsSync(rootImages)) {
        await copyDir(rootImages, distImages, (srcPath) => !srcPath.includes('desktop.ini'));
        console.log('   ✅ Copied root images/');
    }

    // 3. Aggregate Presentations
    console.log('📂 Aggregating presentations from inputs/...');
    const lessons = [];
    
    // If targeted, only look at that folder. Otherwise, look at all.
    const folders = targetFolder ? [targetFolder] : await fsPromises.readdir(inputsDir);

    for (const folder of folders) {
        const lessonPath = path.join(inputsDir, folder);
        if (!fs.existsSync(lessonPath)) {
            console.warn(`   ⚠️  Warning: Lesson folder not found: ${folder}`);
            continue;
        }
        
        const stat = await fsPromises.stat(lessonPath);
        if (!stat.isDirectory()) continue;

        let presentationSrc = path.join(lessonPath, 'published');
        if (!fs.existsSync(path.join(presentationSrc, 'index.html'))) {
            presentationSrc = lessonPath;
        }

        const indexHtml = path.join(presentationSrc, 'index.html');
        if (fs.existsSync(indexHtml)) {
            console.log(`   ✨ Processing lesson: ${folder}`);
            const destLessonDir = path.join(distRoot, folder);
            await fsPromises.mkdir(destLessonDir, { recursive: true });

            let content = await fsPromises.readFile(indexHtml, 'utf-8');

            // --- PATH FIXING LOGIC ---
            // Ensure assets reference the shared root engine at ../dist/ and ../plugin/
            content = content.replace(/(href|src)=["']dist\//g, '$1="../dist/');
            content = content.replace(/(href|src)=["']plugin\//g, '$1="../plugin/');
            content = content.replace(/(href|src)=["']\/dist\//g, '$1="../dist/');
            content = content.replace(/(href|src)=["']\/plugin\//g, '$1="../plugin/');

            await fsPromises.writeFile(path.join(destLessonDir, 'index.html'), content);

            for (const assetFolder of ['images', 'audio']) {
                const srcAsset = path.join(presentationSrc, assetFolder);
                const destAsset = path.join(destLessonDir, assetFolder);
                if (fs.existsSync(srcAsset)) {
                    await copyDir(srcAsset, destAsset, (srcPath) => {
                        if (srcPath.includes('desktop.ini') || srcPath.includes('.git')) return false;
                        const ext = path.extname(srcPath).toLowerCase();
                        if (['.mp4', '.webm', '.mov', '.avi'].includes(ext)) return false;
                        try {
                            const stats = fs.statSync(srcPath);
                            if (stats.isFile() && stats.size > 1024 * 1024) return false;
                        } catch (e) { return false; }
                        return true;
                    });
                }
            }

            const titleMatch = content.match(/<title>(.*?)<\/title>/);
            const title = titleMatch ? titleMatch[1] : folder;
            lessons.push({ folder: folder, title: title });
        }
    }

    // 4. Generate/Update Dashboard
    // In a targeted build, we should ideally read the existing dist folders to keep the dashboard full
    console.log('📊 Updating dashboard...');
    const allDistFolders = await fsPromises.readdir(distRoot);
    const dashboardLessons = [];
    
    for (const folder of allDistFolders) {
        const lessonIndex = path.join(distRoot, folder, 'index.html');
        if (fs.existsSync(lessonIndex) && folder !== 'dist' && folder !== 'plugin' && folder !== 'css' && folder !== 'images') {
            const content = await fsPromises.readFile(lessonIndex, 'utf-8');
            const titleMatch = content.match(/<title>(.*?)<\/title>/);
            dashboardLessons.push({
                folder: folder,
                title: titleMatch ? titleMatch[1] : folder
            });
        }
    }

    const dashboardHtml = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bell Language Centre | Presentations Library</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1a1a1a; color: white; padding: 40px; }
        h1 { color: #8B1538; border-bottom: 2pt solid #8B1538; padding-bottom: 10px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 30px; }
        .card { background: #2a2a2a; border-radius: 8px; padding: 20px; transition: transform 0.2s; border: 1px solid #444; text-decoration: none; color: white; display: block; }
        .card:hover { transform: translateY(-5px); border-color: #8B1538; }
        .card h3 { margin-top: 0; color: #FFD700; }
        .card p { font-size: 0.9em; color: #ccc; }
    </style>
</head>
<body>
    <h1>📚 Presentations Library</h1>
    <div class="grid">
        ${dashboardLessons.map(l => `
            <a href="${l.folder}/" class="card">
                <h3>${l.title}</h3>
                <p>${l.folder}</p>
            </a>
        `).join('')}
    </div>
</body>
</html>
    `;
    await fsPromises.writeFile(path.join(distRoot, 'index.html'), dashboardHtml);

    console.log(`🏁 ${targetFolder ? 'Targeted' : 'Full'} build complete!`);
}

build().catch(err => {
    console.error('💥 Build failed:', err);
    process.exit(1);
});
