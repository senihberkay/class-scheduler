#!/bin/bash

echo "🐳 OZUchedule V2 Docker ile Başlatılıyor..."

# Docker kontrolü
if ! command -v docker &> /dev/null; then
    echo "❌ Docker bulunamadı. Lütfen Docker'ı yükleyin."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose bulunamadı. Lütfen Docker Compose'u yükleyin."
    exit 1
fi

echo "🔧 Docker Compose ile servisler başlatılıyor..."
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Durdurmak için Ctrl+C tuşlayın"
echo ""

# Docker Compose ile başlat
docker-compose up --build
