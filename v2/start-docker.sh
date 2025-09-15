#!/bin/bash

# Script'in doğru dizinden çalıştırıldığından emin ol
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🐳 OZUchedule V2 - Docker ile Başlatılıyor..."
echo "=============================================="

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Local IP adresini al
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "localhost")

echo -e "${BLUE}🌐 Local IP Adresi: $LOCAL_IP${NC}"

# .env dosyasını güncelle
echo "# Environment variables for Docker Compose" > .env
echo "# This file is automatically updated by start-docker.sh" >> .env
echo "HOST_IP=$LOCAL_IP" >> .env
echo -e "${GREEN}✅ .env dosyası güncellendi (HOST_IP=$LOCAL_IP)${NC}"

# Fonksiyon: Docker kontrolü
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker bulunamadı. Lütfen Docker'ı yükleyin.${NC}"
        echo -e "${YELLOW}💡 İndirme adresi: https://www.docker.com/products/docker-desktop${NC}"
        exit 1
    fi

    if ! docker info >/dev/null 2>&1; then
        echo -e "${RED}❌ Docker çalışmıyor. Lütfen Docker'ı başlatın.${NC}"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo -e "${RED}❌ Docker Compose bulunamadı.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Docker ve Docker Compose hazır!${NC}"
}

# Fonksiyon: Port kontrolü
check_ports() {
    echo -e "${BLUE}🔍 Port kontrolü yapılıyor...${NC}"
    
    # Port 3000 kontrolü
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port 3000 zaten kullanımda!${NC}"
        echo -e "${YELLOW}   Mevcut süreçleri sonlandırılıyor...${NC}"
        lsof -ti:3000 | xargs kill -9 2>/dev/null
        sleep 2
    fi
    
    # Port 8001 kontrolü
    if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port 8001 zaten kullanımda!${NC}"
        echo -e "${YELLOW}   Mevcut süreçleri sonlandırılıyor...${NC}"
        lsof -ti:8001 | xargs kill -9 2>/dev/null
        sleep 2
    fi
    
    echo -e "${GREEN}✅ Portlar temizlendi!${NC}"
}

# Fonksiyon: Temizlik
cleanup() {
    echo -e "\n${YELLOW}🛑 Docker servisleri kapatılıyor...${NC}"
    
    # Docker Compose servislerini durdur
    docker-compose down --remove-orphans > /dev/null 2>&1
    
    # Orphan container'ları temizle
    docker container prune -f > /dev/null 2>&1
    
    echo -e "${GREEN}🎉 Docker servisleri temizlendi!${NC}"
    exit 0
}

# Fonksiyon: Docker build ve başlatma
start_docker_services() {
    echo -e "\n${PURPLE}🏗️  Docker imajları oluşturuluyor...${NC}"
    
    # Eski container'ları durdur ve kaldır
    echo -e "${YELLOW}🧹 Eski container'lar temizleniyor...${NC}"
    docker-compose down --remove-orphans > /dev/null 2>&1
    
    # Build ve başlat
    echo -e "${BLUE}🔨 Build işlemi başlatılıyor...${NC}"
    docker-compose up --build -d
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Docker servisleri başarıyla başlatıldı!${NC}"
        return 0
    else
        echo -e "${RED}❌ Docker servisleri başlatılamadı!${NC}"
        return 1
    fi
}

# Fonksiyon: Servis sağlık kontrolü
check_services_health() {
    echo -e "\n${CYAN}🏥 Servis sağlık kontrolleri yapılıyor...${NC}"
    
    # Backend sağlık kontrolü
    echo -e "${YELLOW}⏳ Backend başlatılıyor, lütfen bekleyin...${NC}"
    local backend_ready=false
    for i in {1..30}; do
        if curl -s http://localhost:8001/health > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Backend sağlıklı ve hazır!${NC}"
            backend_ready=true
            break
        fi
        sleep 2
    done
    
    if [ "$backend_ready" = false ]; then
        echo -e "${RED}❌ Backend başlatılamadı!${NC}"
        echo -e "${YELLOW}💡 Backend loglarını kontrol edin: docker-compose logs ozuchedule-backend${NC}"
        return 1
    fi
    
    # Frontend sağlık kontrolü
    echo -e "${YELLOW}⏳ Frontend başlatılıyor, lütfen bekleyin...${NC}"
    local frontend_ready=false
    for i in {1..30}; do
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Frontend sağlıklı ve hazır!${NC}"
            frontend_ready=true
            break
        fi
        sleep 3
    done
    
    if [ "$frontend_ready" = false ]; then
        echo -e "${RED}❌ Frontend başlatılamadı!${NC}"
        echo -e "${YELLOW}💡 Frontend loglarını kontrol edin: docker-compose logs ozuchedule-frontend${NC}"
        return 1
    fi
    
    return 0
}

# Signal yakalama
trap cleanup SIGINT SIGTERM

# Ana işlem
main() {
    echo -e "${BLUE}🔍 Sistem kontrolü yapılıyor...${NC}"
    
    # Docker kontrolü
    check_docker
    
    # Port kontrolü
    check_ports
    
    # Docker servisleri başlat
    if ! start_docker_services; then
        echo -e "${RED}❌ Docker servisleri başlatılamadı!${NC}"
        exit 1
    fi
    
    # Servis sağlık kontrolü
    if ! check_services_health; then
        echo -e "${RED}❌ Servisler sağlıklı başlatılamadı!${NC}"
        echo -e "${YELLOW}� Logları kontrol etmek için: docker-compose logs${NC}"
        exit 1
    fi
    
    # Başarı mesajı
    echo -e "\n${GREEN}🎉 OZUchedule V2 Docker'da Başarıyla Başlatıldı!${NC}"
    echo "=================================================="
    echo -e "${GREEN}🌐 Local Frontend:   http://localhost:3000${NC}"
    echo -e "${GREEN}🌍 Network Frontend: http://$LOCAL_IP:3000${NC}"
    echo -e "${GREEN}� Local Backend:    http://localhost:8001${NC}"
    echo -e "${GREEN}🔧 Network Backend:  http://$LOCAL_IP:8001${NC}"
    echo -e "${GREEN}📚 API Docs:         http://$LOCAL_IP:8001/docs${NC}"
    echo "=================================================="
    echo -e "${CYAN}🐳 Docker Container Durumu:${NC}"
    docker-compose ps
    echo "=================================================="
    echo -e "${YELLOW}📱 Diğer cihazlardan erişim için: http://$LOCAL_IP:3000${NC}"
    echo -e "${YELLOW}💡 Durdurmak için Ctrl+C tuşlayın${NC}"
    echo -e "${YELLOW}📋 Loglar: docker-compose logs [servis-adı]${NC}"
    echo -e "${YELLOW}🔍 Detaylı log: docker-compose logs -f${NC}"
    echo ""
    
    # QR kod önerisi
    echo -e "${BLUE}💡 İpucu: Mobil cihazlardan kolay erişim için QR kod:${NC}"
    echo -e "${BLUE}   https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=http://$LOCAL_IP:3000${NC}"
    echo ""
    
    # Docker Compose loglarını takip et
    echo -e "${CYAN}📜 Canlı logları izlemek için Docker Compose logs başlatılıyor...${NC}"
    echo -e "${YELLOW}   (Logları durdurmak için Ctrl+C, uygulamayı kapatmak için tekrar Ctrl+C)${NC}"
    echo ""
    
    # Logları takip et
    docker-compose logs -f
}

# Script'i çalıştır
main "$@"
