#!/bin/bash

echo "🚀 OZUchedule V2 - Tam Stack Uygulama Başlatılıyor..."
echo "=================================================="

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonksiyon: Port kontrolü
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${YELLOW}⚠️  Port $port zaten kullanımda!${NC}"
        echo -e "${YELLOW}   Mevcut süreçleri sonlandırılıyor...${NC}"
        lsof -ti:$port | xargs kill -9 2>/dev/null
        sleep 2
    fi
}

# Fonksiyon: Backend başlatma
start_backend() {
    echo -e "\n${BLUE}🔧 Backend Başlatılıyor...${NC}"
    echo "=================================="
    
    # Port 8001 kontrolü
    check_port 8001
    
    # Backend dizinine git
    cd backend
    
    # Sanal ortam kontrolü
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}📦 Sanal ortam oluşturuluyor...${NC}"
        python3 -m venv venv
    fi
    
    # Sanal ortamı aktifleştir
    echo -e "${YELLOW}🔧 Sanal ortam aktifleştiriliyor...${NC}"
    source venv/bin/activate
    
    # Bağımlılıkları yükle
    echo -e "${YELLOW}📥 Bağımlılıklar yükleniyor...${NC}"
    pip install -r requirements.txt > /dev/null 2>&1
    
    # Backend'i arka planda başlat
    echo -e "${GREEN}🌟 FastAPI uygulaması başlatılıyor...${NC}"
    echo -e "${GREEN}📍 Backend: http://localhost:8001${NC}"
    echo -e "${GREEN}📚 API Docs: http://localhost:8001/docs${NC}"
    
    uvicorn main:app --reload --host 0.0.0.0 --port 8001 > backend.log 2>&1 &
    BACKEND_PID=$!
    
    # Backend'in başlamasını bekle
    echo -e "${YELLOW}⏳ Backend başlatılıyor, lütfen bekleyin...${NC}"
    sleep 5
    
    # Backend sağlık kontrolü
    if curl -s http://localhost:8001/health > /dev/null; then
        echo -e "${GREEN}✅ Backend başarıyla başlatıldı!${NC}"
    else
        echo -e "${RED}❌ Backend başlatılamadı! Logları kontrol edin: backend.log${NC}"
        return 1
    fi
    
    cd ..
}

# Fonksiyon: Frontend başlatma
start_frontend() {
    echo -e "\n${BLUE}🎨 Frontend Başlatılıyor...${NC}"
    echo "=================================="
    
    # Port 3000 kontrolü
    check_port 3000
    
    # Frontend dizinine git
    cd frontend
    
    # Node modules kontrolü
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}📦 Node.js bağımlılıkları yükleniyor...${NC}"
        npm install > /dev/null 2>&1
    fi
    
    # Frontend'i arka planda başlat
    echo -e "${GREEN}🌟 React uygulaması başlatılıyor...${NC}"
    echo -e "${GREEN}📍 Frontend: http://localhost:3000${NC}"
    echo -e "${GREEN}🔗 Backend API: http://localhost:8001${NC}"
    
    npm start > frontend.log 2>&1 &
    FRONTEND_PID=$!
    
    # Frontend'in başlamasını bekle
    echo -e "${YELLOW}⏳ Frontend başlatılıyor, lütfen bekleyin...${NC}"
    sleep 10
    
    # Frontend sağlık kontrolü
    if curl -s http://localhost:3000 > /dev/null; then
        echo -e "${GREEN}✅ Frontend başarıyla başlatıldı!${NC}"
    else
        echo -e "${RED}❌ Frontend başlatılamadı! Logları kontrol edin: frontend.log${NC}"
        return 1
    fi
    
    cd ..
}

# Fonksiyon: Temizlik
cleanup() {
    echo -e "\n${YELLOW}🛑 Uygulamalar kapatılıyor...${NC}"
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo -e "${GREEN}✅ Backend kapatıldı${NC}"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo -e "${GREEN}✅ Frontend kapatıldı${NC}"
    fi
    
    # Port'ları temizle
    lsof -ti:8001 | xargs kill -9 2>/dev/null
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    
    echo -e "${GREEN}🎉 Tüm süreçler temizlendi!${NC}"
    exit 0
}

# Signal yakalama
trap cleanup SIGINT SIGTERM

# Ana işlem
main() {
    echo -e "${BLUE}🔍 Sistem kontrolü yapılıyor...${NC}"
    
    # Python kontrolü
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 bulunamadı! Lütfen Python3 yükleyin.${NC}"
        exit 1
    fi
    
    # Node.js kontrolü
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js bulunamadı! Lütfen Node.js yükleyin.${NC}"
        exit 1
    fi
    
    # npm kontrolü
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}❌ npm bulunamadı! Lütfen npm yükleyin.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Tüm gereksinimler karşılanıyor!${NC}"
    
    # Backend başlat
    if ! start_backend; then
        echo -e "${RED}❌ Backend başlatılamadı!${NC}"
        exit 1
    fi
    
    # Frontend başlat
    if ! start_frontend; then
        echo -e "${RED}❌ Frontend başlatılamadı!${NC}"
        cleanup
        exit 1
    fi
    
    # Başarı mesajı
    echo -e "\n${GREEN}🎉 OZUchedule V2 Başarıyla Başlatıldı!${NC}"
    echo "=================================================="
    echo -e "${GREEN}🌐 Frontend: http://localhost:3000${NC}"
    echo -e "${GREEN}🔧 Backend:  http://localhost:8001${NC}"
    echo -e "${GREEN}📚 API Docs: http://localhost:8001/docs${NC}"
    echo "=================================================="
    echo -e "${YELLOW}💡 Durdurmak için Ctrl+C tuşlayın${NC}"
    echo -e "${YELLOW}📋 Loglar: backend.log ve frontend.log dosyalarında${NC}"
    echo ""
    
    # Süreçleri bekle
    wait
}

# Script'i çalıştır
main "$@"
