# 🚀 CANLIYA ALMA - HIZLI BAŞLANGIÇ

Lokal test başarılı! Şimdi canlıya alma zamanı. Size 3 seçenek sunuyorum:

---

## 🎯 HANGİ YÖNTEMİ SEÇMELİSİNİZ?

### ⭐ Seçenek 1: Railway.app (EN KOLAY - ÖNERİLEN)

**Avantajlar:**
- ✅ 5 dakikada kurulum
- ✅ Otomatik HTTPS
- ✅ Ücretsiz deneme (aylık $5 kredi)
- ✅ GitHub entegrasyonu
- ✅ Otomatik deploy

**Dezavantajlar:**
- ⚠️ Her API için ayrı service (2 service = 2x maliyet)
- ⚠️ Uyku modu (kullanılmadığında kapanır)

**Maliyet:** ~$10-20/ay (2 API + Frontend)

---

### 🔧 Seçenek 2: Render.com

**Avantajlar:**
- ✅ Ücretsiz plan mevcut (yavaş ama çalışır)
- ✅ Otomatik HTTPS
- ✅ Kolay kurulum

**Dezavantajlar:**
- ⚠️ Ücretsiz planda uyku modu
- ⚠️ Her API için ayrı service

**Maliyet:** Ücretsiz (yavaş) veya $7-14/ay (hızlı)

---

### 🖥️ Seçenek 3: Kendi Sunucunuz (VPS)

**Avantajlar:**
- ✅ Tam kontrol
- ✅ En ucuz (uzun vadede)
- ✅ Özel domain
- ✅ Sınırsız kaynak

**Dezavantajlar:**
- ⚠️ Sunucu yönetimi gerekir
- ⚠️ Kurulum daha uzun sürer

**Maliyet:** $5-10/ay (DigitalOcean, Hetzner, vb.)

---

## 🚀 SEÇENEK 1: RAILWAY.APP İLE CANLIYA ALMA (ÖNERİLEN)

### Adım 1: Railway'a Kayıt Olun

1. https://railway.app adresine gidin
2. "Start a New Project" tıklayın
3. GitHub ile giriş yapın (önerilir)

### Adım 2: Projeyi GitHub'a Yükleyin

**Eğer projeniz GitHub'da yoksa:**

```powershell
# Git repository oluştur
cd "C:\Users\MONSTER\Desktop\sesleAI Proje Web Sitesi"

# .gitignore oluştur (eğer yoksa)
# node_modules/, venv/, __pycache__, *.pyc, .env dosyalarını ignore edin

# Git başlat
git init
git add .
git commit -m "Initial commit"

# GitHub'da yeni repo oluşturun, sonra:
git remote add origin https://github.com/kullanici_adi/sesleai-proje.git
git branch -M main
git push -u origin main
```

### Adım 3: Speaker API'yi Deploy Edin

1. Railway dashboard'da "New Project" > "Deploy from GitHub repo"
2. Reponuzu seçin
3. **Service 1: Speaker API**
   - **Root Directory:** `backend/api`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:**
     ```
     W2V_CLASSIFIER_PATH=/app/backend/models/wav2vec2_model.h5
     W2V_LABELS_PATH=/app/backend/models/classes.npy
     CORS_ORIGINS=https://your-frontend-domain.railway.app
     ```

### Adım 4: Emotion API'yi Deploy Edin

1. Aynı project'te "New Service" > "GitHub Repo"
2. **Service 2: Emotion API**
   - **Root Directory:** `backend/api`
   - **Start Command:** `uvicorn wav2vec_emotion_api:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:**
     ```
     W2V_CLASSIFIER_PATH=/app/backend/models/wav2vec2_model.h5
     W2V_LABELS_PATH=/app/backend/models/classes.npy
     ```

### Adım 5: Model Dosyalarını Yükleyin

**Önemli:** Model dosyalarını Railway'a yüklemeniz gerekiyor.

**Seçenek A: Railway Volume (Önerilen)**
1. Her service'de "Volumes" sekmesine gidin
2. "Add Volume" tıklayın
3. `/app/backend/models` mount edin
4. Model dosyalarınızı buraya yükleyin

**Seçenek B: GitHub'a Yükleyin (Küçük dosyalar için)**
- Model dosyalarını repo'ya ekleyin (git LFS kullanın)

### Adım 6: Frontend'i Deploy Edin

1. **Service 3: Frontend**
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Start Command:** `npm run preview`
   - **Environment Variables:**
     ```
     VITE_SPEAKER_API_URL=https://speaker-api-url.railway.app
     VITE_EMOTION_API_URL=https://emotion-api-url.railway.app
     ```

### Adım 7: Domain Ayarları

1. Her service'de "Settings" > "Generate Domain"
2. Domain'leri kopyalayın
3. Frontend environment variable'larını güncelleyin
4. Redeploy edin

---

## 🔧 SEÇENEK 2: RENDER.COM İLE CANLIYA ALMA

### Adım 1: Render'a Kayıt Olun

1. https://render.com adresine gidin
2. GitHub ile giriş yapın

### Adım 2: Speaker API Deploy

1. "New" > "Web Service"
2. GitHub repo'nuzu seçin
3. **Ayarlar:**
   - **Name:** `speaker-api`
   - **Root Directory:** `backend/api`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r ../requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:**
     ```
     W2V_CLASSIFIER_PATH=/opt/render/project/src/backend/models/wav2vec2_model.h5
     W2V_LABELS_PATH=/opt/render/project/src/backend/models/classes.npy
     ```

### Adım 3: Emotion API Deploy

Aynı adımları tekrarlayın, sadece:
- **Name:** `emotion-api`
- **Start Command:** `uvicorn wav2vec_emotion_api:app --host 0.0.0.0 --port $PORT`

### Adım 4: Frontend Deploy

1. "New" > "Static Site"
2. **Ayarlar:**
   - **Build Command:** `cd frontend && npm install && npm run build`
   - **Publish Directory:** `frontend/dist`
   - **Environment Variables:**
     ```
     VITE_SPEAKER_API_URL=https://speaker-api.onrender.com
     VITE_EMOTION_API_URL=https://emotion-api.onrender.com
     ```

---

## 🖥️ SEÇENEK 3: KENDİ SUNUCUNUZ (VPS)

Detaylı rehber için `ADIM-ADIM-REHBER.md` dosyasına bakın.

**Hızlı özet:**
1. VPS satın alın (DigitalOcean, Hetzner, vb.)
2. SSH ile bağlanın
3. Nginx + PM2 kurun
4. Projeyi yükleyin
5. PM2 ile API'leri başlatın
6. Nginx reverse proxy ayarlayın

---

## 📋 HAZIRLIK CHECKLIST

Canlıya almadan önce:

- [ ] Proje GitHub'da mı? (Cloud platform için)
- [ ] Model dosyaları hazır mı? (`wav2vec2_model.h5`, `classes.npy`)
- [ ] `requirements.txt` dosyası var mı?
- [ ] Frontend `.env.production` hazır mı?
- [ ] Domain alındı mı? (Opsiyonel)

---

## 🎯 ÖNERİM

**Yeni başlayanlar için:** Railway.app (Seçenek 1)
- En kolay
- Hızlı kurulum
- Otomatik HTTPS

**Bütçe önemliyse:** Kendi sunucunuz (Seçenek 3)
- Uzun vadede daha ucuz
- Tam kontrol

**Hızlı test için:** Render.com (Seçenek 2)
- Ücretsiz plan
- Kolay kurulum

---

## 🆘 YARDIM

Hangi yöntemi seçerseniz seçin, adım adım yardımcı olabilirim. Sadece hangi yöntemi tercih ettiğinizi söyleyin!

**Başarılar! 🚀**


