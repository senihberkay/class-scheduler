#!/bin/bash

# Script'in doğru dizinden çalıştırıldığından emin ol
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🛑 OZUchedule V2 Docker Servisleri Kapatılıyor..."
echo "=============================================="

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonksiyon: Docker servislerini durdur
stop_docker_services() {
    echo -e "${BLUE}🐳 Docker Compose servisleri durduruluyor...${NC}"
    
    # Servisleri durdur
    docker-compose down --remove-orphans
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Docker servisleri başarıyla durduruldu!${NC}"
    else
        echo -e "${YELLOW}⚠️  Bazı servisler durdurulurken sorun yaşandı${NC}"
    fi
}

# Fonksiyon: Temizlik seçenekleri
cleanup_options() {
    echo -e "\n${YELLOW}🧹 Temizlik seçenekleri:${NC}"
    echo "1) Sadece servisleri durdur (varsayılan)"
    echo "2) Servisleri durdur + kullanılmayan container'ları sil"
    echo "3) Servisleri durdur + kullanılmayan imajları sil"
    echo "4) Tam temizlik (container + imaj + volume + network)"
    echo ""
    
    read -p "Seçiminizi yapın (1-4) [1]: " choice
    choice=${choice:-1}
    
    case $choice in
        1)
            echo -e "${GREEN}📦 Sadece servisler durduruluyor...${NC}"
            ;;
        2)
            echo -e "${YELLOW}🗑️  Kullanılmayan container'lar siliniyor...${NC}"
            docker container prune -f
            ;;
        3)
            echo -e "${YELLOW}🗑️  Kullanılmayan imajlar siliniyor...${NC}"
            docker container prune -f
            docker image prune -f
            ;;
        4)
            echo -e "${RED}🧨 TAM TEMİZLİK - Tüm Docker kaynakları siliniyor...${NC}"
            echo -e "${YELLOW}⚠️  Bu işlem geri alınamaz! 5 saniye bekleniyor...${NC}"
            sleep 5
            
            docker-compose down --volumes --remove-orphans
            docker container prune -f
            docker image prune -af
            docker volume prune -f
            docker network prune -f
            
            echo -e "${GREEN}✅ Tam temizlik tamamlandı!${NC}"
            ;;
        *)
            echo -e "${RED}❌ Geçersiz seçim. Varsayılan olarak sadece servisler durduruluyor.${NC}"
            ;;
    esac
}

# Ana işlem
main() {
    # Docker kontrolü
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker bulunamadı.${NC}"
        exit 1
    fi

    # Çalışan servisleri kontrol et
    if ! docker-compose ps | grep -q "Up"; then
        echo -e "${YELLOW}⚠️  Çalışan Docker servisi bulunamadı.${NC}"
        echo -e "${BLUE}💡 Mevcut durumu kontrol etmek için: docker-compose ps${NC}"
    else
        echo -e "${BLUE}📋 Çalışan servisler:${NC}"
        docker-compose ps
        echo ""
    fi
    
    # Servisleri durdur
    stop_docker_services
    
    # Temizlik seçenekleri
    cleanup_options
    
    # Port kontrolü
    echo -e "\n${BLUE}🔍 Port durumu kontrol ediliyor...${NC}"
    
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port 3000 hala kullanımda${NC}"
    else
        echo -e "${GREEN}✅ Port 3000 boş${NC}"
    fi
    
    if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port 8001 hala kullanımda${NC}"
    else
        echo -e "${GREEN}✅ Port 8001 boş${NC}"
    fi
    
    echo -e "\n${GREEN}🎉 OZUchedule V2 Docker servisleri başarıyla kapatıldı!${NC}"
    echo "=============================================="
    echo -e "${BLUE}💡 Tekrar başlatmak için: ./start-docker.sh${NC}"
    echo -e "${BLUE}💡 Normal modda başlatmak için: ./start.sh${NC}"
}

# Script'i çalıştır
main "$@"
