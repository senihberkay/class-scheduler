#!/bin/bash

echo "🎨 OZUchedule V2 Frontend Başlatılıyor..."

# Frontend dizinine git
cd frontend

# Node modules kontrolü
if [ ! -d "node_modules" ]; then
    echo "📦 Node.js bağımlılıkları yükleniyor..."
    npm install
fi

# Uygulamayı başlat
echo "🌟 React uygulaması başlatılıyor..."
echo "📍 Frontend: http://localhost:3000"
echo "🔗 Backend API: http://localhost:8000"
echo ""
echo "Durdurmak için Ctrl+C tuşlayın"
echo ""

npm start
