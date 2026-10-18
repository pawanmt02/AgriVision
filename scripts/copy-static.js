const fs = require('fs');
const path = require('path');

function copyFile(src, dest) {
  if (fs.existsSync(src)) {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(src, dest);
    console.log(`Copied ${src} -> ${dest}`);
  }
}

function copyDir(src, dest) {
  if (fs.existsSync(src)) {
    fs.mkdirSync(dest, { recursive: true });
    const entries = fs.readdirSync(src, { withFileTypes: true });
    for (const entry of entries) {
      const srcPath = path.join(src, entry.name);
      const destPath = path.join(dest, entry.name);
      if (entry.isDirectory()) {
        copyDir(srcPath, destPath);
      } else {
        fs.copyFileSync(srcPath, destPath);
      }
    }
    console.log(`Copied directory ${src} -> ${dest}`);
  }
}

// 1. Copy index.html into public
const appIndex = path.join(__dirname, '..', '.next', 'server', 'app', 'index.html');
const publicIndex = path.join(__dirname, '..', 'public', 'index.html');
copyFile(appIndex, publicIndex);

// 2. Copy 404.html into public
const appNotFound = path.join(__dirname, '..', '.next', 'server', 'app', '_not-found.html');
const public404 = path.join(__dirname, '..', 'public', '404.html');
copyFile(appNotFound, public404);

console.log('Static fallback HTML prepared successfully in public/');

