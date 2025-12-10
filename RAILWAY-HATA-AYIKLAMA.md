# 🔍 RAILWAY HATA AYIKLAMA REHBERİ

"Application failed to respond" veya modeller çalışmıyor hatası için adım adım kontrol:

---

## ✅ YAPILAN İYİLEŞTİRMELER

1. ✅ **Google Drive Download Düzeltildi**
   - Büyük dosyalar için özel download fonksiyonu
   - Virus scan sayfası bypass
   - Progress logging

2. ✅ **Startup Event Handler Güvenli Hale Getirildi**
   - Her model yükleme ayrı try-except ile korunuyor
   - Hata olsa bile API başlamaya devam ediyor
   - Detaylı error logging

3. ✅ **Health Check Endpoint Geliştirildi**
   - Model durumlarını gösteriyor
   - API'nin çalışıp çalışmadığını kontrol edebilirsiniz

---

## 🔍 ADIM ADIM HATA AYIKLAMA

### 1. Railway Deploy Loglarını Kontrol Edin

**Railway Dashboard** > **Your Service** > **Deployments** > **Latest** > **View Logs**

#### ✅ Başarılı Log Örneği:
```
🚀 Starting Wav2Vec2 Emotion Recognition API
📥 Downloading model from https://...
✅ File downloaded successfully: /app/backend/models/wav2vec2_model.h5
✅ Wav2Vec2 models loaded successfully
✅ Wav2Vec2 classifier loaded successfully
✅ Label encoder loaded: ['angry' 'calm' ...]
✅ API startup completed (some models may not be loaded)
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:XXXX (Press CTRL+C to quit)
```

#### ❌ Hata Log Örnekleri:

**Model Download Hatası:**
```
❌ Failed to download from https://...: HTTPError: 403 Forbidden
⚠️ Model download failed, but continuing startup...
⚠️ Model file not found at /app/backend/models/wav2vec2_model.h5
```

**Çözüm:** Google Drive link'lerini kontrol edin:
- Link "Anyone with the link" olarak paylaşılmış mı?
- File ID doğru mu?

**Model Yükleme Hatası:**
```
❌ Failed to load Wav2Vec2 models: ConnectionError: ...
```

**Çözüm:** HuggingFace bağlantısı sorunu. Railway'ın internet bağlantısını kontrol edin.

**Port Hatası:**
```
ERROR:    [Errno 98] Address already in use
```

**Çözüm:** Start Command'da `--port $PORT` kullanıldığından emin olun.

---

### 2. Health Check Endpoint'ini Test Edin

API URL'nizi tarayıcıda açın:
```
https://your-emotion-api.railway.app/
```

#### ✅ Başarılı Response:
```json
{
  "message": "🎤 Wav2Vec2 Emotion Recognition API",
  "status": "healthy",
  "models": {
    "wav2vec_loaded": true,
    "classifier_loaded": true,
    "label_encoder_loaded": true
  },
  "models_loaded": ["Wav2Vec2"]
}
```

#### ⚠️ Degraded Response (Modeller yüklenmemiş):
```json
{
  "message": "🎤 Wav2Vec2 Emotion Recognition API",
  "status": "degraded",
  "models": {
    "wav2vec_loaded": false,
    "classifier_loaded": false,
    "label_encoder_loaded": false
  },
  "models_loaded": []
}
```

**Çözüm:** Deploy loglarını kontrol edin, hangi model yüklenemedi?

---

### 3. Environment Variables Kontrolü

**Railway Dashboard** > **Your Service** > **Variables**

#### emotion-api için gerekli:
```
W2V_CLASSIFIER_PATH = /app/backend/models/wav2vec2_model.h5
W2V_LABELS_PATH = /app/backend/models/classes.npy
MODEL_DOWNLOAD_URL = https://drive.google.com/uc?export=download&id=YOUR_FILE_ID
LABEL_DOWNLOAD_URL = https://drive.google.com/uc?export=download&id=YOUR_FILE_ID
PORT = ${{PORT}}  (otomatik, elle eklemeyin)
```

**Önemli:** 
- `MODEL_DOWNLOAD_URL` ve `LABEL_DOWNLOAD_URL` **mutlaka** olmalı
- Google Drive link'leri "Anyone with the link" olarak paylaşılmış olmalı

---

### 4. Start Command Kontrolü

**Railway Dashboard** > **Your Service** > **Settings** > **Start Command**

#### ✅ Doğru:
```bash
python -m uvicorn wav2vec_emotion_api:app --host 0.0.0.0 --port $PORT
```

#### ❌ Yanlış:
```bash
uvicorn wav2vec_emotion_api:app --reload  # --reload production'da kullanılmamalı
uvicorn wav2vec_emotion_api:app --port 8001  # $PORT kullanılmalı
```

---

### 5. Build Command Kontrolü

**Railway Dashboard** > **Your Service** > **Settings** > **Build Command**

#### ✅ Doğru:
```bash
pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
```

---

### 6. Root Directory Kontrolü

**Railway Dashboard** > **Your Service** > **Settings** > **Root Directory**

#### ✅ Doğru:
```
backend/api
```

---

## 🆘 YAYGIN HATALAR VE ÇÖZÜMLERİ

### Hata: "Application failed to respond"

**Nedenler:**
1. API başlamıyor (startup hatası)
2. Port yanlış ayarlanmış
3. Uvicorn çalışmıyor

**Çözüm:**
1. Deploy loglarını kontrol edin
2. Health check endpoint'ini test edin
3. Start Command'ı kontrol edin

### Hata: "Model file not found"

**Nedenler:**
1. Model dosyası indirilemedi
2. `MODEL_DOWNLOAD_URL` yanlış veya eksik
3. Google Drive link'i erişilebilir değil

**Çözüm:**
1. `MODEL_DOWNLOAD_URL` ve `LABEL_DOWNLOAD_URL` environment variable'larını kontrol edin
2. Google Drive link'lerini tarayıcıda test edin
3. Link'lerin "Anyone with the link" olarak paylaşıldığından emin olun

### Hata: "Wav2Vec2 models could not be loaded"

**Nedenler:**
1. HuggingFace bağlantı sorunu
2. Transformers kütüphanesi eksik
3. Internet bağlantısı yok

**Çözüm:**
1. Deploy loglarında HuggingFace hatalarını kontrol edin
2. `requirements.txt`'de `transformers>=4.57.1` olduğundan emin olun
3. Railway'ın internet bağlantısını kontrol edin

---

## 📋 KONTROL LİSTESİ

- [ ] Deploy loglarında "✅ API startup completed" görünüyor mu?
- [ ] Health check endpoint'i çalışıyor mu?
- [ ] Environment variables doğru mu?
- [ ] Start Command doğru mu?
- [ ] Build Command doğru mu?
- [ ] Root Directory doğru mu?
- [ ] Google Drive link'leri erişilebilir mi?

---

## 🚀 HIZLI TEST

1. **Health Check:**
   ```bash
   curl https://your-emotion-api.railway.app/
   ```

2. **Predict Test (modeller yüklüyse):**
   ```bash
   curl -X POST https://your-emotion-api.railway.app/predict \
     -F "file=@test_audio.wav"
   ```

---

**Başarılar! 🚀**

