# 🐳 RAILWAY DOCKER DEPLOYMENT REHBERİ

Railway'da Docker kullanarak deployment yapma adımları:

---

## 📋 HAZIRLIK

### 1. Dockerfile'ları Kontrol Edin

Projede 3 Dockerfile var:
- `backend/api/Dockerfile.speaker` - Speaker Recognition API
- `backend/api/Dockerfile.emotion` - Wav2Vec Emotion API  
- `frontend/Dockerfile` - React Frontend

---

## 🚀 RAILWAY'DA DOCKER DEPLOYMENT

### ADIM 1: Speaker API Service Oluşturma

1. **Railway Dashboard** > **New Project** > **Empty Project**

2. **Add Service** > **GitHub Repo** (veya **Empty Service**)

3. **Settings** > **Root Directory:** `backend/api`

4. **Settings** > **Dockerfile Path:** `Dockerfile.speaker`

5. **Variables** ekleyin:
   ```
   PORT = ${{PORT}}
   CORS_ORIGINS = https://your-frontend.railway.app
   ```

6. **Settings** > **Deploy** > **Deploy Now**

---

### ADIM 2: Emotion API Service Oluşturma

1. **Aynı Project** içinde **Add Service** > **GitHub Repo**

2. **Settings** > **Root Directory:** `backend/api`

3. **Settings** > **Dockerfile Path:** `Dockerfile.emotion`

4. **Variables** ekleyin:
   ```
   PORT = ${{PORT}}
   W2V_CLASSIFIER_PATH = /app/backend/models/wav2vec2_model.h5
   W2V_LABELS_PATH = /app/backend/models/classes.npy
   MODEL_DOWNLOAD_URL = https://drive.google.com/uc?export=download&id=YOUR_FILE_ID
   LABEL_DOWNLOAD_URL = https://drive.google.com/uc?export=download&id=YOUR_FILE_ID
   ```

5. **Settings** > **Deploy** > **Deploy Now**

---

### ADIM 3: Frontend Service Oluşturma

1. **Aynı Project** içinde **Add Service** > **GitHub Repo**

2. **Settings** > **Root Directory:** `frontend`

3. **Settings** > **Dockerfile Path:** `Dockerfile`

4. **Variables** ekleyin:
   ```
   VITE_SPEAKER_API_URL = https://your-speaker-api.railway.app
   VITE_EMOTION_API_URL = https://your-emotion-api.railway.app
   ```

5. **Settings** > **Deploy** > **Deploy Now**

---

## 🔧 DOCKERFILE DÜZELTMELERİ

### Problem: COPY komutları yanlış path'lerde

Railway'da Root Directory `backend/api` olduğunda, COPY komutları düzeltilmeli:

**Dockerfile.speaker ve Dockerfile.emotion için:**

```dockerfile
# Backend kodunu kopyala
COPY . /app/backend/api/

# Models klasörünü kopyala (eğer varsa)
# Not: Models runtime'da indirilecek, bu yüzden bu satır opsiyonel
# COPY ../models /app/backend/models
```

**Daha iyi çözüm:** Root Directory'yi proje root'una almak:

1. **Settings** > **Root Directory:** `.` (proje root)

2. **Dockerfile Path:** `backend/api/Dockerfile.speaker`

3. Dockerfile'da:
```dockerfile
WORKDIR /app

# Requirements kopyala
COPY backend/api/requirements.txt /app/backend/api/

# Python bağımlılıklarını yükle
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/backend/api/requirements.txt

# Backend kodunu kopyala
COPY backend/api/ /app/backend/api/
COPY backend/models/ /app/backend/models/

WORKDIR /app/backend/api
```

---

## 📝 GÜNCELLENMİŞ DOCKERFILE'LAR

### backend/api/Dockerfile.speaker (Root Directory: `.`)

```dockerfile
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Requirements
COPY backend/api/requirements.txt /app/backend/api/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/backend/api/requirements.txt

# Backend code
COPY backend/api/ /app/backend/api/
COPY backend/models/ /app/backend/models/

WORKDIR /app/backend/api

EXPOSE $PORT

CMD python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
```

### backend/api/Dockerfile.emotion (Root Directory: `.`)

```dockerfile
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Requirements
COPY backend/api/requirements.txt /app/backend/api/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/backend/api/requirements.txt

# Backend code
COPY backend/api/ /app/backend/api/
RUN mkdir -p /app/backend/models

WORKDIR /app/backend/api

EXPOSE $PORT

CMD python -m uvicorn wav2vec_emotion_api:app --host 0.0.0.0 --port ${PORT:-8001}
```

### frontend/Dockerfile (Root Directory: `frontend`)

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## ✅ KONTROL LİSTESİ

### Speaker API:
- [ ] Root Directory: `.` (proje root)
- [ ] Dockerfile Path: `backend/api/Dockerfile.speaker`
- [ ] Variables: `PORT`, `CORS_ORIGINS`
- [ ] Deploy başarılı mı?
- [ ] Health check çalışıyor mu?

### Emotion API:
- [ ] Root Directory: `.` (proje root)
- [ ] Dockerfile Path: `backend/api/Dockerfile.emotion`
- [ ] Variables: `PORT`, `W2V_CLASSIFIER_PATH`, `W2V_LABELS_PATH`, `MODEL_DOWNLOAD_URL`, `LABEL_DOWNLOAD_URL`
- [ ] Deploy başarılı mı?
- [ ] Health check çalışıyor mu?
- [ ] Modeller indirildi mi?

### Frontend:
- [ ] Root Directory: `frontend`
- [ ] Dockerfile Path: `Dockerfile`
- [ ] Variables: `VITE_SPEAKER_API_URL`, `VITE_EMOTION_API_URL`
- [ ] Deploy başarılı mı?
- [ ] Frontend çalışıyor mu?

---

## 🆘 SORUN GİDERME

### Build Hatası: "COPY failed: file not found"

**Çözüm:** Root Directory ve Dockerfile Path'i kontrol edin.

### Port Hatası: "Address already in use"

**Çözüm:** CMD'de `${PORT}` kullanıldığından emin olun.

### Model Dosyaları Bulunamıyor

**Çözüm:** 
- `MODEL_DOWNLOAD_URL` ve `LABEL_DOWNLOAD_URL` doğru mu?
- Google Drive link'leri "Anyone with the link" olarak paylaşılmış mı?

---

## 🎯 HIZLI BAŞLANGIÇ

1. **GitHub'a push yapın**
2. **Railway'da 3 service oluşturun** (yukarıdaki adımlar)
3. **Variables'ları ekleyin**
4. **Deploy edin**
5. **Public domain'leri alın**
6. **Test edin!**

**Başarılar! 🚀**

