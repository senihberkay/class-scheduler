#!/bin/bash

# OZUchedule V2 - Docker Hızlı Başlatma
# Tek komutla Docker'da çalıştır

cd "$(dirname "$0")"

echo "🚀 OZUchedule V2 - Hızlı Docker Başlatma"
echo "======================================"

# Renk kodları
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Local IP
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "localhost")

echo -e "${BLUE}🐳 Docker Compose ile başlatılıyor...${NC}"

# Eski container'ları temizle ve yeni başlat
docker-compose down --remove-orphans > /dev/null 2>&1
docker-compose up --build -d

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✅ Başarıyla başlatıldı!${NC}"
    echo "========================="
    echo -e "${GREEN}🌐 Frontend: http://localhost:3000${NC}"
    echo -e "${GREEN}🔧 Backend:  http://localhost:8001${NC}"
    echo -e "${GREEN}📚 API:      http://localhost:8001/docs${NC}"
    echo -e "${GREEN}🌍 Network:  http://$LOCAL_IP:3000${NC}"
    echo "========================="
    echo -e "${BLUE}💡 Durdurmak için: ./stop-docker.sh${NC}"
    echo -e "${BLUE}📜 Loglar için: docker-compose logs -f${NC}"
else
    echo "❌ Başlatma başarısız!"
    exit 1
fi
