# 📋 ADIM ADIM CANLIYA ALMA REHBERİ

Bu rehber, projenizi canlıya almak için yapmanız gereken her şeyi adım adım anlatır.

---

## 🎯 HANGİ YÖNTEMİ SEÇMELİSİNİZ?

### Seçenek A: Kendi Sunucunuz (VPS/Dedicated Server) - ÖNERİLEN
- ✅ Tam kontrol
- ✅ Daha ucuz (uzun vadede)
- ✅ Özel domain kullanabilirsiniz
- ⚠️ Sunucu yönetimi gerekir

### Seçenek B: Cloud Platform (Railway, Render, Heroku)
- ✅ Kolay kurulum
- ✅ Otomatik scaling
- ⚠️ Daha pahalı
- ⚠️ Her API için ayrı service gerekir

**Bu rehber Seçenek A (Kendi Sunucunuz) için hazırlanmıştır.**

---

## 📦 ADIM 1: HAZIRLIK AŞAMASI

### 1.1 Sunucu Gereksinimleri
- Ubuntu 20.04+ veya Debian 11+ (Linux)
- En az 4GB RAM (8GB önerilir - modeller büyük)
- En az 20GB disk alanı
- Python 3.10+
- Node.js 18+
- Domain adınız (opsiyonel ama önerilir)

### 1.2 Lokal Test (Kendi Bilgisayarınızda)
Önce her şeyin çalıştığından emin olun:

```powershell
# Windows PowerShell'de:

# 1. Backend API'leri test et
cd "C:\Users\MONSTER\Desktop\sesleAI Proje Web Sitesi\backend\api"
conda activate voice_env
$env:W2V_CLASSIFIER_PATH="C:\Users\MONSTER\Desktop\sesleAI Proje Web Sitesi\backend\models\wav2vec2_model.h5"
$env:W2V_LABELS_PATH="C:\Users\MONSTER\Desktop\sesleAI Proje Web Sitesi\backend\models\classes.npy"
uvicorn main:app --host 0.0.0.0 --port 8000

# Yeni bir terminal açın ve:
uvicorn wav2vec_emotion_api:app --host 0.0.0.0 --port 8001

# 3. Frontend'i test et (başka bir terminal)
cd "C:\Users\MONSTER\Desktop\sesleAI Proje Web Sitesi\frontend"
npm install
npm run dev
```

Eğer her şey çalışıyorsa, devam edin.

---

## 🚀 ADIM 2: SUNUCUYA BAĞLANMA VE TEMEL KURULUM

### 2.1 Sunucuya SSH ile Bağlanın
```bash
ssh kullanici_adi@sunucu_ip_adresi
```

### 2.2 Sistem Güncellemesi
```bash
sudo apt update
sudo apt upgrade -y
```

### 2.3 Temel Araçları Kurun
```bash
# Python ve pip
sudo apt install python3.10 python3-pip python3-venv -y

# Node.js 18+ (NodeSource repository'den)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# ffmpeg (ses işleme için kritik!)
sudo apt install ffmpeg -y

# Nginx (reverse proxy için)
sudo apt install nginx -y

# PM2 (process manager)
sudo npm install -g pm2

# Git (projeyi çekmek için)
sudo apt install git -y
```

### 2.4 Versiyonları Kontrol Edin
```bash
python3 --version  # 3.10+ olmalı
node --version     # 18+ olmalı
npm --version
ffmpeg -version   # Kurulu olmalı
pm2 --version
nginx -v
```

---

## 📁 ADIM 3: PROJEYİ SUNUCUYA YÜKLEME

### 3.1 Proje Klasörü Oluşturun
```bash
sudo mkdir -p /var/www/sesleai
sudo chown $USER:$USER /var/www/sesleai
cd /var/www/sesleai
```

### 3.2 Projeyi Yükleyin

**Seçenek 1: Git ile (eğer GitHub'da varsa)**
```bash
git clone https://github.com/kullanici_adi/sesleai-proje.git .
```

**Seçenek 2: SCP ile (kendi bilgisayarınızdan)**
Kendi bilgisayarınızda (Windows PowerShell):
```powershell
# Projeyi zip'leyin veya direkt SCP ile gönderin
scp -r "C:\Users\MONSTER\Desktop\sesleAI Proje Web Sitesi" kullanici_adi@sunucu_ip:/var/www/sesleai/
```

**Seçenek 3: Manuel Upload**
- FileZilla, WinSCP gibi bir FTP/SFTP client kullanın
- Tüm proje klasörünü `/var/www/sesleai` klasörüne yükleyin

### 3.3 Klasör Yapısını Kontrol Edin
```bash
cd /var/www/sesleai
ls -la
# Şunları görmelisiniz:
# - backend/
# - frontend/
# - models/ (veya backend/models/)
# - nginx.conf
# - ecosystem.config.js
```

---

## 🐍 ADIM 4: PYTHON ORTAMINI KURMA

### 4.1 Virtual Environment Oluşturun
```bash
cd /var/www/sesleai/backend
python3 -m venv venv
source venv/bin/activate
```

### 4.2 Python Bağımlılıklarını Yükleyin
```bash
# requirements.txt dosyası varsa:
pip install --upgrade pip
pip install -r requirements.txt

# Yoksa manuel yükleyin (zaten requirements.txt oluşturuldu):
pip install fastapi uvicorn torch torchaudio transformers speechbrain tensorflow keras librosa soundfile pydub numpy scikit-learn scipy
```

### 4.3 Model Dosyalarını Kontrol Edin
```bash
# Model dosyalarının yerinde olduğundan emin olun
ls -la /var/www/sesleai/backend/models/
# Şunları görmelisiniz:
# - wav2vec2_model.h5
# - classes.npy
# - speaker_classifier.pth (varsa)
```

---

## 🌐 ADIM 5: FRONTEND'I BUILD ETME

### 5.1 Node Bağımlılıklarını Yükleyin
```bash
cd /var/www/sesleai/frontend
npm install
```

### 5.2 Environment Variables Ayarlayın
```bash
# .env.production dosyası oluşturun
nano .env.production
```

İçine şunları yazın (kendi domain'inizi yazın):
```
VITE_SPEAKER_API_URL=https://yourdomain.com/api/speaker
VITE_EMOTION_API_URL=https://yourdomain.com/api/emotion
```

**Not:** Eğer henüz domain yoksa, IP adresini kullanın:
```
VITE_SPEAKER_API_URL=http://sunucu_ip:8000
VITE_EMOTION_API_URL=http://sunucu_ip:8001
```

### 5.3 Frontend'i Build Edin
```bash
npm run build
```

Build başarılı olursa `frontend/dist` klasörü oluşur.

---

## ⚙️ ADIM 6: BACKEND API'LERİNİ BAŞLATMA (PM2 İLE)

### 6.1 PM2 Config Dosyasını Güncelleyin
```bash
cd /var/www/sesleai
nano ecosystem.config.js
```

`cwd` ve `env` kısımlarını kendi yollarınıza göre güncelleyin:
```javascript
cwd: '/var/www/sesleai/backend/api',
env: {
  PYTHONPATH: '/var/www/sesleai/backend/api',
  W2V_CLASSIFIER_PATH: '/var/www/sesleai/backend/models/wav2vec2_model.h5',
  W2V_LABELS_PATH: '/var/www/sesleai/backend/models/classes.npy',
  CORS_ORIGINS: 'https://yourdomain.com,http://yourdomain.com'
}
```

### 6.2 Logs Klasörü Oluşturun
```bash
mkdir -p /var/www/sesleai/logs
```

### 6.3 PM2 ile API'leri Başlatın
```bash
cd /var/www/sesleai
pm2 start ecosystem.config.js
```

### 6.4 Durumu Kontrol Edin
```bash
pm2 status
pm2 logs
```

Her iki API de "online" görünmeli.

### 6.5 PM2'yi Sistem Açılışında Başlat
```bash
pm2 startup
# Çıkan komutu çalıştırın (sudo ile)
pm2 save
```

---

## 🔧 ADIM 7: NGINX REVERSE PROXY KURULUMU

### 7.1 Nginx Config Dosyasını Kopyalayın
```bash
sudo cp /var/www/sesleai/nginx.conf /etc/nginx/sites-available/sesleai
sudo ln -s /etc/nginx/sites-available/sesleai /etc/nginx/sites-enabled/
```

### 7.2 Nginx Config'i Düzenleyin
```bash
sudo nano /etc/nginx/sites-available/sesleai
```

**Önemli değişiklikler:**
1. `server_name` satırını bulun ve domain'inizi yazın:
   ```
   server_name yourdomain.com www.yourdomain.com;
   ```
   Domain yoksa IP kullanın veya `_` bırakın.

2. Frontend path'ini kontrol edin:
   ```
   root /var/www/sesleai/frontend/dist;
   ```

3. Domain yoksa, `server_name` yerine `_` kullanabilirsiniz.

### 7.3 Frontend Dosyalarını Doğru Yere Kopyalayın
```bash
sudo mkdir -p /var/www/sesleai/frontend/dist
sudo cp -r /var/www/sesleai/frontend/dist/* /var/www/sesleai/frontend/dist/
```

### 7.4 Nginx'i Test Edin
```bash
sudo nginx -t
```

"Syntax OK" görünmeli.

### 7.5 Nginx'i Başlatın
```bash
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### 7.6 Firewall Ayarları
```bash
# UFW kullanıyorsanız:
sudo ufw allow 'Nginx Full'
sudo ufw allow 8000/tcp  # Speaker API (opsiyonel, Nginx üzerinden erişilecekse gerekmez)
sudo ufw allow 8001/tcp  # Emotion API (opsiyonel)
sudo ufw reload
```

---

## 🔒 ADIM 8: SSL/HTTPS KURULUMU (OPSİYONEL AMA ÖNERİLİR)

### 8.1 Let's Encrypt Kurulumu
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 8.2 SSL Sertifikası Alın
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Sertifika otomatik olarak kurulur ve Nginx config güncellenir.

### 8.3 Otomatik Yenileme Testi
```bash
sudo certbot renew --dry-run
```

---

## ✅ ADIM 9: TEST VE KONTROL

### 9.1 API'lerin Çalıştığını Kontrol Edin
```bash
# PM2 durumu
pm2 status

# Logları kontrol
pm2 logs speaker-api
pm2 logs emotion-api

# API endpoint'lerini test et
curl http://localhost:8000/
curl http://localhost:8001/
```

### 9.2 Nginx'in Çalıştığını Kontrol Edin
```bash
sudo systemctl status nginx
curl http://localhost/
```

### 9.3 Frontend'i Test Edin
Tarayıcıda şu adresi açın:
- `http://sunucu_ip` (domain yoksa)
- `https://yourdomain.com` (domain varsa)

### 9.4 API Endpoint'lerini Test Edin
```bash
# Speaker API
curl https://yourdomain.com/api/speaker/

# Emotion API
curl https://yourdomain.com/api/emotion/
```

---

## 🐛 ADIM 10: SORUN GİDERME

### API'ler Başlamıyor
```bash
# Logları kontrol
pm2 logs

# Manuel başlatmayı deneyin
cd /var/www/sesleai/backend/api
source ../../venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

### CORS Hatası
```bash
# ecosystem.config.js'de CORS_ORIGINS'i kontrol edin
# main.py'de CORS ayarlarını kontrol edin
```

### Model Dosyaları Bulunamıyor
```bash
# Dosya yollarını kontrol
ls -la /var/www/sesleai/backend/models/
# Environment variable'ları kontrol
pm2 env 0  # speaker-api için
pm2 env 1  # emotion-api için
```

### Nginx 502 Bad Gateway
```bash
# API'lerin çalıştığını kontrol
pm2 status
curl http://localhost:8000/
curl http://localhost:8001/

# Nginx error log
sudo tail -f /var/log/nginx/error.log
```

---

## 📊 ADIM 11: MONİTÖRİNG VE BAKIM

### 11.1 PM2 Monitoring
```bash
pm2 monit  # Gerçek zamanlı monitoring
pm2 list   # Process listesi
pm2 info speaker-api  # Detaylı bilgi
```

### 11.2 Log Yönetimi
```bash
# Logları görüntüle
pm2 logs --lines 100

# Logları temizle
pm2 flush
```

### 11.3 Otomatik Backup (Önerilir)
Model dosyalarınızı düzenli olarak yedekleyin:
```bash
# Basit backup script
#!/bin/bash
tar -czf /backup/sesleai-models-$(date +%Y%m%d).tar.gz /var/www/sesleai/backend/models/
```

---

## 🎉 TAMAMLANDI!

Artık projeniz canlıda! 

### Erişim URL'leri:
- **Frontend:** `https://yourdomain.com`
- **Speaker API:** `https://yourdomain.com/api/speaker/`
- **Emotion API:** `https://yourdomain.com/api/emotion/`

### Önemli Komutlar:
```bash
# API'leri durdur
pm2 stop all

# API'leri başlat
pm2 start all

# API'leri yeniden başlat
pm2 restart all

# Nginx'i yeniden başlat
sudo systemctl restart nginx
```

---

## 📞 YARDIM

Sorun yaşarsanız:
1. Logları kontrol edin: `pm2 logs` ve `sudo tail -f /var/log/nginx/error.log`
2. Process durumunu kontrol edin: `pm2 status`
3. Portları kontrol edin: `sudo netstat -tulpn | grep 8000`

**Başarılar! 🚀**


