#!/bin/bash

echo "🛑 OZUchedule V2 - Uygulamalar Kapatılıyor..."
echo "============================================="

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonksiyon: Port'taki süreçleri kapat
kill_port() {
    local port=$1
    local service_name=$2
    
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${YELLOW}🔍 $service_name (Port $port) kapatılıyor...${NC}"
        lsof -ti:$port | xargs kill -9 2>/dev/null
        sleep 1
        
        if ! lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
            echo -e "${GREEN}✅ $service_name başarıyla kapatıldı${NC}"
        else
            echo -e "${RED}❌ $service_name kapatılamadı${NC}"
        fi
    else
        echo -e "${BLUE}ℹ️  $service_name zaten kapalı${NC}"
    fi
}

# Ana işlem
main() {
    echo -e "${BLUE}🔍 Çalışan süreçler kontrol ediliyor...${NC}"
    
    # Backend'i kapat (Port 8001)
    kill_port 8001 "Backend"
    
    # Frontend'i kapat (Port 3000)
    kill_port 3000 "Frontend"
    
    # Ek temizlik - uvicorn ve react-scripts süreçleri
    echo -e "${YELLOW}🧹 Ek süreçler temizleniyor...${NC}"
    
    # uvicorn süreçleri
    if pgrep -f "uvicorn" > /dev/null; then
        pkill -f "uvicorn"
        echo -e "${GREEN}✅ Uvicorn süreçleri kapatıldı${NC}"
    fi
    
    # react-scripts süreçleri
    if pgrep -f "react-scripts" > /dev/null; then
        pkill -f "react-scripts"
        echo -e "${GREEN}✅ React-scripts süreçleri kapatıldı${NC}"
    fi
    
    # Log dosyalarını temizle
    if [ -f "backend.log" ]; then
        rm backend.log
        echo -e "${GREEN}✅ Backend log dosyası temizlendi${NC}"
    fi
    
    if [ -f "frontend.log" ]; then
        rm frontend.log
        echo -e "${GREEN}✅ Frontend log dosyası temizlendi${NC}"
    fi
    
    echo -e "\n${GREEN}🎉 Tüm OZUchedule V2 süreçleri başarıyla kapatıldı!${NC}"
    echo "============================================="
}

# Script'i çalıştır
main "$@"
