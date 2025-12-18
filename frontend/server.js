const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();
const PORT = process.env.PORT || 3000;

// API 프록시 (백엔드로)
app.use('/coordinates', createProxyMiddleware({ target: 'http://localhost:8000', changeOrigin: true }));

// 정적 파일 서빙
app.use(express.static(path.join(__dirname)));

// 기본 라우트
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Frontend server running on http://0.0.0.0:${PORT}`);
});