# OZUchedule Deployment Rehberi

## 🚀 Render.com ile Deployment (ÖNERİLEN)

### Backend Deployment:

1. **Render.com'a git** ve GitHub hesabınla giriş yap
2. **New Web Service** oluştur
3. **GitHub repo'nu seç** (class-scheduler)
4. **Ayarları yap:**
   - Name: `ozuchedule-backend`
   - Runtime: `Python 3`
   - Build Command: `cd v2/backend && pip install -r requirements.txt`
   - Start Command: `cd v2/backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Plan: `Free`

### Frontend Deployment:

1. **New Static Site** oluştur
2. **GitHub repo'nu seç** (class-scheduler)
3. **Ayarları yap:**
   - Name: `ozuchedule-frontend`
   - Build Command: `cd v2/frontend && npm install && npm run build`
   - Publish Directory: `v2/frontend/build`
   - Environment Variables:
     - `REACT_APP_API_URL`: `https://your-backend-url.onrender.com`

### 📝 Notlar:
- Backend URL'ini frontend environment variable'a ekle
- Free tier'da 750 saat/ay limit var
- İlk deployment 10-15 dakika sürebilir

---

## 🌐 Alternatif: Netlify + Railway/Heroku

### Netlify (Frontend):
1. Netlify.com'a git
2. GitHub repo'yu bağla
3. `netlify.toml` dosyası otomatik algılanır

### PythonAnywhere (Backend):
1. PythonAnywhere.com'a kaydol (ücretsiz)
2. Files bölümünden projeyi upload et
3. Web app oluştur

---

## 🐳 Dockerfile Yaklaşımı

Eğer Docker kullanmak istersen:

```dockerfile
# Backend Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY v2/backend/requirements.txt .
RUN pip install -r requirements.txt
COPY v2/backend/ .
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

# Frontend Dockerfile  
FROM node:18-alpine
WORKDIR /app
COPY v2/frontend/package*.json ./
RUN npm install
COPY v2/frontend/ .
RUN npm run build
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
EXPOSE 80
```

Bu dosyalar oluşturuldu:
- `render.yaml` - Render.com için
- `netlify.toml` - Netlify için
- Bu README dosyası

En kolay yol Render.com kullanmak!
