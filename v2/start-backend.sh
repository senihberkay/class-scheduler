#!/bin/bash

echo "🚀 OZUchedule V2 Backend Başlatılıyor..."

# Backend dizinine git
cd backend

# Sanal ortam kontrolü
if [ ! -d "venv" ]; then
    echo "📦 Sanal ortam oluşturuluyor..."
    python3 -m venv venv
fi

# Sanal ortamı aktifleştir
echo "🔧 Sanal ortam aktifleştiriliyor..."
source venv/bin/activate

# Bağımlılıkları yükle
echo "📥 Bağımlılıklar yükleniyor..."
pip install -r requirements.txt

# Uygulamayı başlat
echo "🌟 FastAPI uygulaması başlatılıyor..."
echo "📍 Backend: http://localhost:8001"
echo "📚 API Docs: http://localhost:8001/docs"
echo ""
echo "Durdurmak için Ctrl+C tuşlayın"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8001
