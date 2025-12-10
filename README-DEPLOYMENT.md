# 🚀 Canlıya Alma Özeti

Projeniz için deployment hazırlıkları tamamlandı! İşte yapılan değişiklikler ve kullanım kılavuzu.

## ✅ Yapılan Değişiklikler

### 1. **Frontend Güncellemeleri**
- ✅ Hardcoded API URL'leri environment variable'lara taşındı
- ✅ `vite.config.js` güncellendi (env variable desteği)
- ✅ Tüm frontend dosyaları dinamik API URL kullanıyor

### 2. **Backend Güncellemeleri**
- ✅ CORS ayarları production için güncellendi
- ✅ Environment variable desteği eklendi

### 3. **Deployment Dosyaları**
- ✅ `nginx.conf` - Reverse proxy konfigürasyonu
- ✅ `docker-compose.yml` - Docker deployment
- ✅ `Dockerfile.backend` - Backend container
- ✅ `ecosystem.config.js` - PM2 process manager
- ✅ `start-apis.sh` / `start-apis.ps1` - Başlatma scriptleri
- ✅ `requirements.txt` - Python bağımlılıkları
- ✅ `DEPLOYMENT.md` - Detaylı deployment rehberi

---

## 🎯 Hızlı Başlangıç

### Lokal Test (Windows)
```powershell
# 1. Backend API'leri başlat
.\start-apis.ps1

# 2. Frontend'i build et ve başlat
cd frontend
npm install
npm run build
npm run preview
```

### Production Deployment (Nginx ile)

1. **Frontend Build**
```bash
cd frontend
VITE_SPEAKER_API_URL=https://yourdomain.com/api/speaker \
VITE_EMOTION_API_URL=https://yourdomain.com/api/emotion \
npm run build
```

2. **Nginx Config'i Güncelle**
- `nginx.conf` dosyasındaki `yourdomain.com` kısmını değiştir
- Frontend build dosyalarını `/var/www/sesleai/frontend/dist` klasörüne kopyala

3. **Backend API'leri Başlat (PM2 ile)**
```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

4. **Nginx'i Başlat**
```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

## 📁 Dosya Yapısı

```
sesleAI Proje Web Sitesi/
├── backend/
│   ├── api/
│   │   ├── main.py (Speaker API - Port 8000)
│   │   ├── wav2vec_emotion_api.py (Emotion API - Port 8001)
│   │   └── speaker_api.py
│   ├── models/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   └── vite.config.js (güncellendi)
├── nginx.conf (YENİ)
├── docker-compose.yml (YENİ)
├── ecosystem.config.js (YENİ)
├── start-apis.sh (YENİ)
├── start-apis.ps1 (YENİ)
└── DEPLOYMENT.md (YENİ - Detaylı rehber)
```

---

## 🔧 Environment Variables

### Frontend (.env.production)
```bash
VITE_SPEAKER_API_URL=https://yourdomain.com/api/speaker
VITE_EMOTION_API_URL=https://yourdomain.com/api/emotion
```

### Backend (Sistem veya .env)
```bash
W2V_CLASSIFIER_PATH=/path/to/wav2vec2_model.h5
W2V_LABELS_PATH=/path/to/classes.npy
CORS_ORIGINS=https://yourdomain.com
```

---

## 🎨 Deployment Seçenekleri

### 1. **Nginx Reverse Proxy** (Önerilen - Production)
- Tek domain altında iki API
- SSL/HTTPS desteği
- Detaylar: `DEPLOYMENT.md` dosyasına bakın

### 2. **Docker Compose** (Kolay - Development/Production)
```bash
docker-compose up -d
```

### 3. **PM2** (Process Management)
```bash
pm2 start ecosystem.config.js
```

### 4. **Cloud Platform** (Railway, Render, Heroku)
- Her API için ayrı service
- Environment variable'ları platform üzerinden ayarla

---

## 📝 Önemli Notlar

1. **Model Dosyaları**: `backend/models/` klasöründe olmalı
2. **ffmpeg**: Sistem seviyesinde kurulu olmalı
3. **Portlar**: 8000 (Speaker), 8001 (Emotion)
4. **CORS**: Production'da sadece kendi domain'inizi ekleyin

---

## 🆘 Sorun Giderme

### API'ler başlamıyor
- Portların kullanılabilir olduğundan emin olun
- Log dosyalarını kontrol edin: `pm2 logs` veya `docker-compose logs`

### CORS Hatası
- `CORS_ORIGINS` environment variable'ını kontrol edin
- Nginx config'de CORS header'ları doğru mu?

### Model Dosyaları Bulunamıyor
- `W2V_CLASSIFIER_PATH` ve `W2V_LABELS_PATH` değişkenlerini kontrol edin
- Dosya yollarının mutlak (absolute) olduğundan emin olun

---

## 📚 Daha Fazla Bilgi

Detaylı deployment rehberi için `DEPLOYMENT.md` dosyasına bakın.

---

**Hazırlayan:** AI Assistant  
**Tarih:** 2025-11-25  
**Versiyon:** 1.0


