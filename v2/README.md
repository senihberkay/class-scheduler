# OZUchedule V2 - Yeni Nesil Ders Programlama Uygulaması

🧭 **Proje Özeti**

OZUchedule V2, Özyeğin Üniversitesi öğrencilerinin ders programlarını kolayca oluşturabilmeleri için geliştirilen modern bir web uygulamasıdır. Bu versiyon, React.js frontend ve FastAPI backend ile geliştirilmiştir.

## 🎯 Özellikler

- **Modern UI/UX**: Tailwind CSS ile responsive tasarım
- **Gerçek Zamanlı Çakışma Kontrolü**: Ders çakışmalarını anında tespit
- **Arama ve Filtreleme**: Dersleri kolayca bulma
- **Renk Kodlu Görselleştirme**: Her ders için farklı renk
- **Mobil Uyumlu**: Tüm cihazlarda mükemmel deneyim
- **API Tabanlı**: Modüler ve genişletilebilir mimari

## 🏗️ Sistem Mimarisi

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React.js      │    │   FastAPI       │    │   JSON/CSV      │
│   Frontend      │◄──►│   Backend       │◄──►│   Veri Katmanı  │
│   (Port 3000)   │    │   (Port 8001)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Hızlı Başlangıç

### Gereksinimler

- **Backend**: Python 3.10+
- **Frontend**: Node.js 18+
- **Docker**: (Opsiyonel)

### 🎯 Tek Komutla Başlatma

#### Yerel Geliştirme Modunda
```bash
# Tüm uygulamayı başlat (Backend + Frontend)
./start.sh

# Uygulamaları durdur
./stop.sh
```

#### Docker Modunda (Önerilen)
```bash
# Docker ile detaylı başlatma (sağlık kontrolleri dahil)
./start-docker.sh

# Docker ile hızlı başlatma
./docker-quick.sh

# Docker servislerini durdur
./stop-docker.sh
```

### Yerel Geliştirme

#### 1. Backend Kurulumu

```bash
cd v2/backend

# Sanal ortam oluştur
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt

# Uygulamayı başlat
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

#### 2. Frontend Kurulumu

```bash
cd v2/frontend

# Bağımlılıkları yükle
npm install

# Uygulamayı başlat
npm start
```

### Docker ile Çalıştırma

#### 🚀 Hızlı Başlatma (Önerilen)
```bash
# En hızlı yol - tek komutla başlat
./docker-quick.sh

# Detaylı başlatma (sağlık kontrolleri ve log takibi ile)
./start-docker.sh

# Manuel Docker Compose
docker-compose up --build -d
```

#### 🛑 Durdurma ve Temizlik
```bash
# Akıllı durdurma (temizlik seçenekleri ile)
./stop-docker.sh

# Hızlı durdurma
docker-compose down

# Tam temizlik (container + image + volume)
docker-compose down --volumes --rmi all
```

#### 🔍 Docker Durum Kontrolü
```bash
# Container durumunu görüntüle
docker-compose ps

# Canlı logları izle
docker-compose logs -f

# Belirli servis logları
docker-compose logs -f ozuchedule-frontend
docker-compose logs -f ozuchedule-backend
```

## 📁 Proje Yapısı

```
v2/
├── backend/
│   ├── main.py              # FastAPI ana uygulama
│   ├── requirements.txt      # Python bağımlılıkları
│   └── Dockerfile           # Backend Docker yapılandırması
├── frontend/
│   ├── src/
│   │   ├── components/      # React bileşenleri
│   │   ├── App.js          # Ana uygulama
│   │   └── index.js        # Giriş noktası
│   ├── package.json         # Node.js bağımlılıkları
│   └── Dockerfile          # Frontend Docker yapılandırması
├── docker-compose.yml       # Docker Compose yapılandırması
├── start.sh                 # Yerel başlatma scripti
├── stop.sh                  # Yerel durdurma scripti
├── start-docker.sh          # Docker detaylı başlatma scripti
├── stop-docker.sh           # Docker durdurma scripti
├── docker-quick.sh          # Docker hızlı başlatma scripti
└── README.md               # Bu dosya
```

## 🐳 Docker Yapılandırması

### Özellikler

- **Health Checks**: Backend ve frontend için otomatik sağlık kontrolleri
- **Named Containers**: Kolay yönetim için özel container isimleri
- **Volume Management**: Log dosyaları için persistent storage
- **Network Isolation**: Güvenli container iletişimi
- **Dependency Management**: Frontend backend'in hazır olmasını bekler
- **Environment Variables**: Production-ready yapılandırma
- **Restart Policy**: Hata durumunda otomatik yeniden başlatma

### Docker Compose Servisleri

| Servis | Container | Port | Açıklama |
|--------|-----------|------|----------|
| ozuchedule-backend | ozuchedule-backend | 8001 | FastAPI Backend |
| ozuchedule-frontend | ozuchedule-frontend | 3000 | React Frontend |

### Docker Scriptleri

| Script | Açıklama |
|--------|----------|
| `start-docker.sh` | Detaylı başlatma (sağlık kontrolleri, log takibi) |
| `docker-quick.sh` | Hızlı başlatma (minimum output) |
| `stop-docker.sh` | Akıllı durdurma (temizlik seçenekleri) |

## 🔧 API Endpoints

### Backend API (FastAPI)

| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/` | GET | API durumu |
| `/courses` | GET | Tüm dersleri listele |
| `/courses/{code}` | GET | Belirli dersi getir |
| `/instructors` | GET | Öğretim üyelerini listele |
| `/check-conflicts` | POST | Çakışma kontrolü |
| `/generate-schedule` | POST | Program oluştur |
| `/health` | GET | Sağlık kontrolü |

### Örnek API Kullanımı

```bash
# Dersleri listele
curl http://localhost:8001/courses

# Çakışma kontrolü
curl -X POST http://localhost:8001/check-conflicts \
  -H "Content-Type: application/json" \
  -d '{"courses": ["MAT101", "PHY101"]}'

# Program oluştur
curl -X POST http://localhost:8001/generate-schedule \
  -H "Content-Type: application/json" \
  -d '{"selected_courses": ["MAT101", "PHY101"]}'
```

## 🎨 Frontend Bileşenleri

### Ana Bileşenler

- **Header**: Uygulama başlığı ve navigasyon
- **CourseList**: Ders listesi ve seçim paneli
- **ScheduleGrid**: Haftalık program görünümü
- **ConflictModal**: Çakışma uyarı modalı
- **LoadingSpinner**: Yükleme göstergesi

### Özellikler

- **Responsive Tasarım**: Mobil ve masaüstü uyumlu
- **Arama ve Filtreleme**: Dersleri hızlıca bulma
- **Renk Kodlaması**: Her ders için otomatik renk
- **Gerçek Zamanlı Güncelleme**: Anlık program değişiklikleri

## 📊 Veri Modeli

### JSON Formatı

```json
{
  "courses": [
    {
      "code": "MAT101",
      "name": "Matematik I",
      "sections": [
        {
          "section": "A1",
          "instructor": "Dr. Ahmet Yılmaz",
          "schedule": [
            {
              "day": "Pazartesi",
              "start": "09:40",
              "duration": 2,
              "room": "EF 210"
            }
          ]
        }
      ]
    }
  ]
}
```

## 🕐 Zaman Çizelgesi

| Saat | Aralık |
|------|--------|
| 1 | 08:40–09:30 |
| 2 | 09:40–10:30 |
| 3 | 10:40–11:30 |
| 4 | 11:40–12:30 |
| 5 | 12:40–13:30 |
| 6 | 13:40–14:30 |
| 7 | 14:40–15:30 |
| 8 | 15:40–16:30 |
| 9 | 16:40–17:30 |
| 10 | 17:40–18:30 |

## 🛠️ Geliştirme

### Backend Geliştirme

```bash
cd v2/backend

# Sanal ortamı aktifleştir
source venv/bin/activate

# Kod formatla
black main.py

# Lint kontrolü
flake8 main.py

# Test çalıştır
pytest
```

### Frontend Geliştirme

```bash
cd v2/frontend

# Kod formatla
npm run format

# Lint kontrolü
npm run lint

# Test çalıştır
npm test
```

## 🚀 Deployment

### Production Build

```bash
# Frontend build
cd v2/frontend
npm run build

# Backend production
cd v2/backend
uvicorn main:app --host 0.0.0.0 --port 8001
```

### Docker Deployment

```bash
# Production build
docker-compose -f docker-compose.prod.yml up --build

# Nginx ile reverse proxy
docker-compose -f docker-compose.nginx.yml up --build
```

## 🔍 Sorun Giderme

### Yaygın Sorunlar

#### Genel Sorunlar
1. **CORS Hatası**: Backend CORS ayarlarını kontrol edin
2. **Port Çakışması**: 3000 ve 8001 portlarının boş olduğundan emin olun
3. **Veri Yükleme Hatası**: CSV dosyasının doğru konumda olduğunu kontrol edin
4. **Script Çalışmıyor**: `chmod +x *.sh` ile scriptleri çalıştırılabilir yapın

#### Docker Sorunları
1. **Docker Çalışmıyor**: `docker info` ile Docker'ın çalıştığını kontrol edin
2. **Container Başlamıyor**: `docker-compose ps` ile container durumunu kontrol edin
3. **Port Erişimi**: `docker-compose logs [servis-adı]` ile logları kontrol edin
4. **Build Hatası**: `docker system prune -f` ile temizlik yapın ve tekrar deneyin
5. **Health Check Başarısız**: Backend `/health` endpoint'inin çalıştığını kontrol edin

### Log Kontrolü

#### Yerel Geliştirme
```bash
# Backend logları
tail -f v2/backend/backend.log

# Frontend logları
tail -f v2/frontend/frontend.log
```

#### Docker Logları
```bash
# Tüm servislerin logları
docker-compose logs -f

# Belirli servis logları
docker-compose logs -f ozuchedule-backend
docker-compose logs -f ozuchedule-frontend

# Son 100 satır log
docker-compose logs --tail=100 ozuchedule-backend
```

### Sistem Durumu Kontrolü

#### Docker Container Durumu
```bash
# Container durumları
docker-compose ps

# Sistem kaynak kullanımı
docker stats

# Container detayları
docker inspect ozuchedule-backend
docker inspect ozuchedule-frontend
```

#### Port ve Network Kontrolü
```bash
# Port kullanımı
lsof -i :3000
lsof -i :8001

# Docker network
docker network ls
docker network inspect ozuchedule-network
```

### Temizlik ve Reset

#### Docker Temizliği
```bash
# Hafif temizlik
docker-compose down
docker container prune -f

# Orta temizlik
docker-compose down --volumes
docker image prune -f

# Tam temizlik (DİKKAT: Tüm data silinir!)
./stop-docker.sh  # Seçenek 4'ü seçin
```

#### Sistem Reset
```bash
# Tüm local değişiklikleri sıfırla
git clean -fd
git reset --hard HEAD

# Dependency'leri yeniden yükle
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
```

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

- **Geliştirici**: SBA7
- **Email**: your-email@example.com
- **GitHub**: [GitHub Issues](https://github.com/your-repo/issues)

## 📞 İletişim

- **GitHub Issues**: Hata raporları ve özellik istekleri için
- **Email**: Doğrudan iletişim için

---

© 2025 SBA7 - OZUchedule V2 Tüm Hakları Saklıdır
