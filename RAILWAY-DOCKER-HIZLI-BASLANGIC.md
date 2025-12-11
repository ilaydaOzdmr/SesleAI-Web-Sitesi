# 🚀 RAILWAY DOCKER HIZLI BAŞLANGIÇ

Railway'da Docker ile 3 service'i deploy etme (5 dakika):

---

## 📋 ADIM ADIM

### 1️⃣ Speaker API Service

1. **Railway Dashboard** > **New Project** > **Empty Project**

2. **Add Service** > **GitHub Repo** > Repo'nuzu seçin

3. **Settings:**
   - **Root Directory:** `.` (nokta - proje root)
   - **Dockerfile Path:** `backend/api/Dockerfile.speaker`

4. **Variables:**
   ```
   PORT = ${{PORT}}
   CORS_ORIGINS = https://your-frontend.railway.app
   ```

5. **Deploy** > **Deploy Now**

6. **Settings** > **Generate Domain** > Public domain alın

---

### 2️⃣ Emotion API Service

1. **Aynı Project** > **Add Service** > **GitHub Repo**

2. **Settings:**
   - **Root Directory:** `.`
   - **Dockerfile Path:** `backend/api/Dockerfile.emotion`

3. **Variables:**
   ```
   PORT = ${{PORT}}
   W2V_CLASSIFIER_PATH = /app/backend/models/wav2vec2_model.h5
   W2V_LABELS_PATH = /app/backend/models/classes.npy
   MODEL_DOWNLOAD_URL = https://drive.google.com/uc?export=download&id=YOUR_FILE_ID
   LABEL_DOWNLOAD_URL = https://drive.google.com/uc?export=download&id=YOUR_FILE_ID
   ```

4. **Deploy** > **Deploy Now**

5. **Settings** > **Generate Domain** > Public domain alın

---

### 3️⃣ Frontend Service

1. **Aynı Project** > **Add Service** > **GitHub Repo**

2. **Settings:**
   - **Root Directory:** `frontend`
   - **Dockerfile Path:** `Dockerfile`

3. **Variables:**
   ```
   VITE_SPEAKER_API_URL = https://your-speaker-api.railway.app
   VITE_EMOTION_API_URL = https://your-emotion-api.railway.app
   ```

4. **Deploy** > **Deploy Now**

5. **Settings** > **Generate Domain** > Public domain alın

---

## ✅ KONTROL

### Health Check:
- Speaker API: `https://your-speaker-api.railway.app/`
- Emotion API: `https://your-emotion-api.railway.app/`
- Frontend: `https://your-frontend.railway.app/`

### Beklenen Response:
- Speaker API: `{"message": "Ses Kimlik Tespiti API'si çalışıyor."}`
- Emotion API: `{"message": "🎤 Wav2Vec2 Emotion Recognition API", "status": "healthy", ...}`
- Frontend: React uygulaması açılmalı

---

## 🆘 SORUN GİDERME

### Build Hatası: "COPY failed"
- Root Directory doğru mu? (Speaker/Emotion: `.`, Frontend: `frontend`)
- Dockerfile Path doğru mu?

### Port Hatası
- Variables'da `PORT = ${{PORT}}` var mı?

### Model Dosyaları Bulunamıyor
- `MODEL_DOWNLOAD_URL` ve `LABEL_DOWNLOAD_URL` doğru mu?
- Google Drive link'leri "Anyone with the link" olarak paylaşılmış mı?

---

**Başarılar! 🚀**

