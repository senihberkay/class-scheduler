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
│   (Port 3000)   │    │   (Port 8000)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Hızlı Başlangıç

### Gereksinimler

- **Backend**: Python 3.10+
- **Frontend**: Node.js 18+
- **Docker**: (Opsiyonel)

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
uvicorn main:app --reload --host 0.0.0.0 --port 8000
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

```bash
# Tüm servisleri başlat
docker-compose up --build

# Arka planda çalıştır
docker-compose up -d --build
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
└── README.md               # Bu dosya
```

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
curl http://localhost:8000/courses

# Çakışma kontrolü
curl -X POST http://localhost:8000/check-conflicts \
  -H "Content-Type: application/json" \
  -d '{"courses": ["MAT101", "PHY101"]}'

# Program oluştur
curl -X POST http://localhost:8000/generate-schedule \
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
uvicorn main:app --host 0.0.0.0 --port 8000
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

1. **CORS Hatası**: Backend CORS ayarlarını kontrol edin
2. **Port Çakışması**: 3000 ve 8000 portlarının boş olduğundan emin olun
3. **Veri Yükleme Hatası**: CSV dosyasının doğru konumda olduğunu kontrol edin

### Log Kontrolü

```bash
# Backend logları
docker-compose logs backend

# Frontend logları
docker-compose logs frontend
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
