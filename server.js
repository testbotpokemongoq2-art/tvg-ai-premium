const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.PNG': 'image/png',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.webp': 'image/webp',
  '.mp4': 'video/mp4'
};

http.createServer((req, res) => {
  let urlPath = req.url.split('?')[0];
  let filePath = path.join(__dirname, urlPath === '/' ? 'index.html' : urlPath);
  const ext = path.extname(filePath);
  const contentType = MIME[ext] || 'application/octet-stream';

  fs.readFile(filePath, (err, data) => {
    if (err) {
      fs.readFile(path.join(__dirname, 'index.html'), (e, d) => {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(d);
      });
    } else if (req.headers.range && ext === '.mp4') {
      // video: trả từng đoạn (Range) để iPhone/Safari phát và tua được
      const m = /bytes=(\d*)-(\d*)/.exec(req.headers.range) || [];
      const start = m[1] ? parseInt(m[1]) : 0, end = m[2] ? Math.min(parseInt(m[2]), data.length - 1) : data.length - 1;
      res.writeHead(206, { 'Content-Type': contentType, 'Content-Range': `bytes ${start}-${end}/${data.length}`, 'Accept-Ranges': 'bytes', 'Content-Length': end - start + 1 });
      res.end(data.subarray(start, end + 1));
    } else {
      res.writeHead(200, { 'Content-Type': contentType, ...(ext === '.mp4' ? { 'Accept-Ranges': 'bytes' } : {}) });
      res.end(data);
    }
  });
}).listen(PORT, () => console.log('TVG AI Premium running on port ' + PORT));
