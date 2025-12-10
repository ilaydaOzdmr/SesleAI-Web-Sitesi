# 🚀 Deployment Rehberi - SesleAI Proje

Bu proje 2 ayrı backend API ve 1 frontend içerir. Canlıya alma için aşağıdaki seçeneklerden birini kullanabilirsiniz.

## 📋 İçindekiler

1. [Hızlı Başlangıç](#hızlı-başlangıç)
2. [Seçenek 1: Nginx Reverse Proxy (Önerilen)](#seçenek-1-nginx-reverse-proxy)
3. [Seçenek 2: Docker Compose](#seçenek-2-docker-compose)
4. [Seçenek 3: PM2 Process Manager](#seçenek-3-pm2-process-manager)
5. [Seçenek 4: Cloud Platform (Railway/Render)](#seçenek-4-cloud-platform)
6. [Environment Variables](#environment-variables)

---

## 🏃 Hızlı Başlangıç

### Gereksinimler
- Python 3.10+
- Node.js 18+
- ffmpeg (sistem PATH'inde)
- Conda/Virtualenv

### Lokal Test
```bash
# Backend API'leri başlat
# Windows:
.\start-apis.ps1

# Linux/Mac:
chmod +x start-apis.sh
./start-apis.sh

# Frontend'i başlat
cd frontend
npm install
npm run build
npm run preview
```

---

## 🔧 Seçenek 1: Nginx Reverse Proxy (Önerilen)

### Avantajlar
- ✅ Tek domain altında iki API
- ✅ SSL/HTTPS desteği kolay
- ✅ Production-ready
- ✅ Load balancing imkanı

### Adımlar

1. **Nginx Kurulumu (Ubuntu/Debian)**
```bash
sudo apt update
sudo apt install nginx
```

2. **Nginx Config Dosyasını Kopyala**
```bash
sudo cp nginx.conf /etc/nginx/sites-available/sesleai
sudo ln -s /etc/nginx/sites-available/sesleai /etc/nginx/sites-enabled/
```

3. **Domain'i Güncelle**
`nginx.conf` dosyasındaki `yourdomain.com` kısmını kendi domain'inizle değiştirin.

4. **Frontend Build**
```bash
cd frontend
npm install
npm run build
```

5. **Frontend Dosyalarını Kopyala**
```bash
sudo mkdir -p /var/www/sesleai/frontend
sudo cp -r frontend/dist/* /var/www/sesleai/frontend/
```

6. **Backend API'leri Başlat (PM2 veya systemd ile)**
```bash
# PM2 kullanarak:
pm2 start ecosystem.config.js

# veya systemd service olarak (detaylar aşağıda)
```

7. **Nginx'i Test Et ve Başlat**
```bash
sudo nginx -t
sudo systemctl restart nginx
```

### SSL/HTTPS (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 🐳 Seçenek 2: Docker Compose

### Avantajlar
- ✅ Kolay kurulum
- ✅ İzolasyon
- ✅ Otomatik restart

### Adımlar

1. **Docker ve Docker Compose Kurulumu**
```bash
# Ubuntu/Debian
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

2. **Backend için requirements.txt oluştur** (eğer yoksa)
```bash
cd backend
pip freeze > requirements.txt
```

3. **Docker Compose ile Başlat**
```bash
docker-compose up -d
```

4. **Logları Kontrol Et**
```bash
docker-compose logs -f
```

5. **Durdur**
```bash
docker-compose down
```

---

## ⚙️ Seçenek 3: PM2 Process Manager

### Avantajlar
- ✅ Process monitoring
- ✅ Otomatik restart
- ✅ Log yönetimi

### Adımlar

1. **PM2 Kurulumu**
```bash
npm install -g pm2
```

2. **API'leri Başlat**
```bash
pm2 start ecosystem.config.js
```

3. **Durum Kontrolü**
```bash
pm2 status
pm2 logs
```

4. **Otomatik Başlatma (Sistem açılışında)**
```bash
pm2 startup
pm2 save
```

---

## ☁️ Seçenek 4: Cloud Platform

### Railway.app

1. **Railway'a Giriş Yap**
2. **Yeni Proje Oluştur**
3. **GitHub Repo'yu Bağla**
4. **Environment Variables Ekle:**
   - `W2V_CLASSIFIER_PATH`
   - `W2V_LABELS_PATH`
   - `CORS_ORIGINS`
5. **Her API için ayrı service oluştur**

### Render.com

1. **Yeni Web Service Oluştur**
2. **Build Command:** `pip install -r backend/requirements.txt`
3. **Start Command:** `cd backend/api && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables Ekle**

---

## 🔐 Environment Variables

### Backend (.env veya sistem değişkenleri)

```bash
# Speaker API için
CORS_ORIGINS=http://localhost:5173,https://yourdomain.com

# Emotion API için
W2V_CLASSIFIER_PATH=/path/to/wav2vec2_model.h5
W2V_LABELS_PATH=/path/to/classes.npy
```

### Frontend (.env.production)

```bash
VITE_SPEAKER_API_URL=https://yourdomain.com/api/speaker
VITE_EMOTION_API_URL=https://yourdomain.com/api/emotion
```

**Not:** Frontend build sırasında environment variable'lar kullanılır. Production build için:
```bash
VITE_SPEAKER_API_URL=https://yourdomain.com/api/speaker \
VITE_EMOTION_API_URL=https://yourdomain.com/api/emotion \
npm run build
```

---

## 📝 Systemd Service (Opsiyonel)

`/etc/systemd/system/speaker-api.service`:
```ini
[Unit]
Description=Speaker Recognition API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/backend/api
Environment="W2V_CLASSIFIER_PATH=/path/to/wav2vec2_model.h5"
Environment="W2V_LABELS_PATH=/path/to/classes.npy"
ExecStart=/path/to/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Aynı şekilde `emotion-api.service` oluşturun.

---

## 🐛 Troubleshooting

### API'ler başlamıyor
- Portların kullanılabilir olduğundan emin olun: `netstat -tulpn | grep 8000`
- Log dosyalarını kontrol edin: `pm2 logs` veya `docker-compose logs`

### CORS Hatası
- `CORS_ORIGINS` environment variable'ını kontrol edin
- Nginx config'de CORS header'larının doğru olduğundan emin olun

### Model Dosyaları Bulunamıyor
- `W2V_CLASSIFIER_PATH` ve `W2V_LABELS_PATH` değişkenlerini kontrol edin
- Dosya yollarının mutlak (absolute) olduğundan emin olun

---

## 📞 Destek

Sorun yaşarsanız:
1. Log dosyalarını kontrol edin
2. Environment variable'ları doğrulayın
3. Port çakışmalarını kontrol edin


