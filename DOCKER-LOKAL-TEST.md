# 🐳 DOCKER LOKAL TEST REHBERİ

Docker ile lokal test yapma adımları:

---

## 📋 ÖN HAZIRLIK

### 1. Docker Desktop Kurulu Olmalı
- Windows: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Kurulumdan sonra Docker Desktop'ı başlatın

### 2. Model Dosyaları Kontrolü
- `backend/models/` klasöründe model dosyaları var mı?
  - `wav2vec2_model.h5`
  - `classes.npy`
  - `pretrained-ecapa/` klasörü (speaker recognition için)

---

## 🚀 HIZLI BAŞLANGIÇ

### Tek Komutla Başlatma

```bash
docker-compose up --build
```

Bu komut:
- İki API'yi build eder
- Container'ları başlatır
- Logları gösterir

### Arka Planda Çalıştırma

```bash
docker-compose up -d --build
```

### Logları İzleme

```bash
# Tüm servislerin logları
docker-compose logs -f

# Sadece speaker-api logları
docker-compose logs -f speaker-api

# Sadece emotion-api logları
docker-compose logs -f emotion-api
```

---

## ✅ TEST ETME

### 1. Health Check

**Speaker API:**
```bash
curl http://localhost:8000/
```

Beklenen response:
```json
{"message": "Ses Kimlik Tespiti API'si çalışıyor."}
```

**Emotion API:**
```bash
curl http://localhost:8001/
```

Beklenen response:
```json
{
  "message": "🎤 Wav2Vec2 Emotion Recognition API",
  "status": "healthy",
  "models": {
    "wav2vec_loaded": true,
    "classifier_loaded": true,
    "label_encoder_loaded": true
  }
}
```

### 2. Browser'da Test

- Speaker API: http://localhost:8000/
- Emotion API: http://localhost:8001/

---

## 🛠️ SORUN GİDERME

### Container'lar Başlamıyor

**1. Port'lar kullanımda mı kontrol edin:**
```bash
# Windows PowerShell
netstat -ano | findstr :8000
netstat -ano | findstr :8001
```

**2. Container'ları durdurun ve yeniden başlatın:**
```bash
docker-compose down
docker-compose up --build
```

### Build Hatası

**1. Cache'i temizleyin:**
```bash
docker-compose build --no-cache
```

**2. Eski image'ları silin:**
```bash
docker system prune -a
```

### Model Dosyaları Bulunamıyor

**Emotion API için:**
- `MODEL_DOWNLOAD_URL` ve `LABEL_DOWNLOAD_URL` environment variable'larını `.env` dosyasına ekleyin:

```env
MODEL_DOWNLOAD_URL=https://drive.google.com/uc?export=download&id=YOUR_FILE_ID
LABEL_DOWNLOAD_URL=https://drive.google.com/uc?export=download&id=YOUR_FILE_ID
```

Veya docker-compose.yml'de direkt belirtin:
```yaml
environment:
  - MODEL_DOWNLOAD_URL=https://...
  - LABEL_DOWNLOAD_URL=https://...
```

### API'ler Çalışmıyor

**1. Container loglarını kontrol edin:**
```bash
docker-compose logs speaker-api
docker-compose logs emotion-api
```

**2. Container içine girip test edin:**
```bash
# Speaker API container'ına gir
docker exec -it speaker-api bash

# Container içinde test
curl http://localhost:8000/
```

**3. Python modüllerini kontrol edin:**
```bash
docker exec -it speaker-api python -c "import uvicorn; print('OK')"
docker exec -it emotion-api python -c "import uvicorn; print('OK')"
```

---

## 📝 YARARLI KOMUTLAR

### Container'ları Durdurma
```bash
docker-compose down
```

### Container'ları Durdurma (Volume'ları da sil)
```bash
docker-compose down -v
```

### Container'ları Yeniden Başlatma
```bash
docker-compose restart
```

### Container Durumunu Kontrol
```bash
docker-compose ps
```

### Container'ları Sil ve Yeniden Build Et
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 🎯 SONRAKI ADIMLAR

Lokal test başarılı olduktan sonra:

1. **Railway'a deploy edin** (RAILWAY-DOCKER-HIZLI-BASLANGIC.md'ye bakın)
2. **Frontend'i de test edin** (frontend/Dockerfile ile)
3. **Production environment variable'larını ayarlayın**

---

**Başarılar! 🚀**

