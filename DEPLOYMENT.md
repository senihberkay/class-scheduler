# 🚀 OZUchedule V2 - Ücretsiz Deployment Rehberi

Bu rehber, OZUchedule V2 uygulamasını ücretsiz olarak canlıya almanız için hazırlanmıştır.

## 📋 Deployment Stratejisi

**Frontend**: Vercel (Ücretsiz)  
**Backend**: Railway (Ücretsiz $5 kredi)

## 🎯 Adım Adım Deployment

### 1. GitHub Repository Hazırlığı

✅ Proje zaten GitHub'da mevcut!

### 2. Backend Deployment (Railway)

1. **Railway'e kaydolun**: https://railway.app/
2. **GitHub ile giriş yapın**
3. **"New Project"** butonuna tıklayın
4. **"Deploy from GitHub repo"** seçin
5. **Bu repository'yi seçin**: `class-scheduler`
6. **Root directory** olarak: `/v2/backend` belirtin
7. **Deploy** butonuna tıklayın

**Önemli Ayarlar:**
- Service Name: `ozuchedule-backend`
- Environment Variables:
  ```
  PYTHONPATH=/app
  ```

### 3. Frontend Deployment (Vercel)

1. **Vercel'e kaydolun**: https://vercel.com/
2. **GitHub ile giriş yapın**
3. **"New Project"** butonuna tıklayın
4. **Bu repository'yi import edin**: `class-scheduler`
5. **Root directory** olarak: `/v2/frontend` belirtin
6. **Environment Variables** ekleyin:
   ```
   REACT_APP_API_URL=https://[RAILWAY_BACKEND_URL]
   ```
7. **Deploy** butonuna tıklayın

### 4. Son Ayarlar

#### Backend URL'sini alın:
- Railway dashboard'dan backend service'inizi açın
- URL'yi kopyalayın (örn: `https://ozuchedule-backend-production.up.railway.app`)

#### Frontend'i güncelleyin:
- Vercel dashboard'dan frontend project'inizi açın
- Settings > Environment Variables
- `REACT_APP_API_URL` değerini Railway backend URL'si ile güncelleyin
- Redeploy edin

## 🎉 Sonuç

Deployment tamamlandıktan sonra:

- **Frontend URL**: https://[PROJECT_NAME].vercel.app
- **Backend URL**: https://[SERVICE_NAME].up.railway.app

## 💡 Alternatif Seçenekler

### Netlify + Render
- **Frontend**: Netlify (Ücretsiz)
- **Backend**: Render (Ücretsiz 750 saat/ay)

### GitHub Pages + PythonAnywhere
- **Frontend**: GitHub Pages (Sadece static)
- **Backend**: PythonAnywhere (Sınırlı ücretsiz)

## 🔧 Troubleshooting

### CORS Hatası Alırsanız:
Backend'de CORS ayarlarına frontend URL'nizi ekleyin:
```python
allow_origins=[
    "https://your-frontend-url.vercel.app"
]
```

### Build Hatası Alırsanız:
- `package.json` dependencies'lerini kontrol edin
- Node.js versiyon uyumluluğunu kontrol edin

## 📞 Destek

Deployment sırasında sorun yaşarsanız:
1. Railway/Vercel loglarını kontrol edin
2. Environment variables'ları doğrulayın
3. CORS ayarlarını kontrol edin

---

**Not**: Bu rehber projenin mevcut yapısını bozmadan deployment yapmanızı sağlar. Tüm özellikler korunacaktır.
